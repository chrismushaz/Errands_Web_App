from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def notification_list(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications
    })

@login_required
def mark_notification_read(request, notification_id):
    try:
        notification = request.user.notifications.get(id=notification_id)
        notification.mark_as_read()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)

@login_required
def mark_all_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})

@login_required
def get_unread_count(request):
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'count': count}) 