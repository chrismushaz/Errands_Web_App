from django.db import models
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Errand(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ASSIGNED', 'Assigned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_errands')
    tasker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasker_errands')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Temporarily comment out the payment_intent_id field until migration is applied
    # payment_intent_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.title

class Cancellation(models.Model):
    REFUND_STATUS_CHOICES = (
        ('N/A', 'Not Applicable'),
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )
    
    errand = models.OneToOneField(Errand, on_delete=models.CASCADE, related_name='cancellation')
    cancelled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cancellations')
    reason = models.TextField()
    cancelled_at = models.DateTimeField(auto_now_add=True)
    refund_status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='N/A')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refund_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Cancellation for {self.errand.title}"

class ErrandApplication(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )
    
    errand = models.ForeignKey(Errand, on_delete=models.CASCADE, related_name='applications')
    tasker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    proposal = models.TextField()
    proposed_budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.tasker.username} - {self.errand.title}"

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    
    errand = models.ForeignKey(Errand, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.reviewer.username} -> {self.reviewed.username} ({self.rating} stars)"
