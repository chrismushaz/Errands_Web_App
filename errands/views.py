from django.shortcuts import render
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
try:
    import stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    print("Warning: Stripe package not installed. Payment functionality will be disabled.")
from .models import Category, Errand, ErrandApplication, Review, Cancellation
from .serializers import (
    CategorySerializer, ErrandSerializer, ErrandApplicationSerializer,
    ReviewSerializer, CancellationSerializer
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ErrandViewSet(viewsets.ModelViewSet):
    queryset = Errand.objects.all()
    serializer_class = ErrandSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CLIENT':
            return Errand.objects.filter(client=user)
        else:  # TASKER
            return Errand.objects.filter(
                Q(status='PENDING') | Q(tasker=user)
            )

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        errand = self.get_object()
        
        # Check if user is the client who created the errand
        if errand.client != request.user:
            return Response(
                {"detail": "Only the client who created the errand can cancel it."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if errand can be cancelled
        if errand.status not in ['PENDING', 'ASSIGNED']:
            return Response(
                {"detail": "Only pending or assigned errands can be cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get cancellation reason from request
        reason = request.data.get('reason', 'No reason provided')
        
        # Update errand status to CANCELLED
        errand.status = 'CANCELLED'
        errand.save()
        
        # Create cancellation record
        cancellation = Cancellation.objects.create(
            errand=errand,
            cancelled_by=request.user,
            reason=reason,
            refund_status='N/A'
        )
        
        # Handle refund if errand was assigned and has payment
        # Check if payment_intent_id attribute exists
        has_payment = hasattr(errand, 'payment_intent_id') and errand.payment_intent_id
        
        if errand.status == 'ASSIGNED' and has_payment:
            if STRIPE_AVAILABLE:
                try:
                    # Create refund using Stripe
                    refund = stripe.Refund.create(
                        payment_intent=errand.payment_intent_id,
                        reason='requested_by_customer'
                    )
                    
                    # Update cancellation record with refund details
                    cancellation.refund_status = 'COMPLETED'
                    cancellation.refund_amount = errand.budget
                    cancellation.refund_transaction_id = refund.id
                    cancellation.save()
                    
                    refund_status = 'COMPLETED'
                except stripe.error.StripeError as e:
                    # Log the error and update cancellation record
                    cancellation.refund_status = 'FAILED'
                    cancellation.save()
                    refund_status = 'FAILED'
                    # You might want to log this error for monitoring
            else:
                # Stripe is not available, mark refund as pending
                cancellation.refund_status = 'PENDING'
                cancellation.save()
                refund_status = 'PENDING (Stripe not available)'
        else:
            refund_status = 'N/A'
        
        # Send notification to tasker if assigned
        if errand.tasker:
            send_mail(
                subject=f'Errand Cancelled: {errand.title}',
                message=f'''
                The errand "{errand.title}" has been cancelled by the client.
                
                Reason: {reason}
                
                Errand Details:
                - Location: {errand.location}
                - Date: {errand.preferred_date}
                - Time: {errand.preferred_time}
                - Budget: ${errand.budget}
                
                Thank you for your understanding.
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[errand.tasker.email],
                fail_silently=True,
            )
        
        # Send notification to client
        send_mail(
            subject=f'Errand Cancelled: {errand.title}',
            message=f'''
                You have successfully cancelled the errand "{errand.title}".
                
                Reason: {reason}
                
                Errand Details:
                - Location: {errand.location}
                - Date: {errand.preferred_date}
                - Time: {errand.preferred_time}
                - Budget: ${errand.budget}
                
                Refund Status: {refund_status}
                
                Thank you for using ErrandMate.
                ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[errand.client.email],
            fail_silently=True,
        )
        
        # Update all related applications to REJECTED
        ErrandApplication.objects.filter(errand=errand).update(status='REJECTED')
        
        # Return serialized cancellation data
        cancellation_data = CancellationSerializer(cancellation).data
        
        return Response(
            {
                "detail": "Errand cancelled successfully.",
                "notifications_sent": True,
                "applications_updated": True,
                "cancellation": cancellation_data
            },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Only allow deletion if:
        # 1. User is the client who created the errand
        # 2. Errand is in PENDING status
        if instance.client != request.user:
            return Response(
                {"detail": "Only the client who created the errand can delete it."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if instance.status != 'PENDING':
            return Response(
                {"detail": "Only pending errands can be deleted."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ErrandApplicationViewSet(viewsets.ModelViewSet):
    queryset = ErrandApplication.objects.all()
    serializer_class = ErrandApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CLIENT':
            return ErrandApplication.objects.filter(errand__client=user)
        else:  # TASKER
            return ErrandApplication.objects.filter(tasker=user)

    def perform_create(self, serializer):
        serializer.save(tasker=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(
            Q(reviewer=user) | Q(reviewed=user)
        )

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

def errand_list(request):
    """View for listing all errands with optional filtering"""
    errands = Errand.objects.all().order_by('-created_at')
    
    # Filter by category if specified
    category_id = request.GET.get('category')
    if category_id:
        errands = errands.filter(category_id=category_id)
    
    # Filter by status if specified
    status = request.GET.get('status')
    if status:
        errands = errands.filter(status=status)
    
    # Filter by location if specified
    location = request.GET.get('location')
    if location:
        errands = errands.filter(location__icontains=location)
    
    # Get all categories for the filter form
    categories = Category.objects.all()
    
    context = {
        'errands': errands,
        'categories': categories,
        'selected_category': category_id,
        'selected_status': status,
        'selected_location': location,
    }
    
    return render(request, 'errands/errand_list.html', context)


def about_page(request):
    return render(request, 'about.html')

def help_page(request):
    return render(request, 'help.html')

login_required
def update_profile_picture(request):
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            request.user.profile_picture = profile_picture
            request.user.save()
            messages.success(request, "Profile picture updated successfully.")
        else:
            messages.error(request, "No file selected.")
    return redirect('accounts:profile')