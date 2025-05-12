from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('ERAND_CREATED', 'New Errand Created'),
        ('ERAND_UPDATED', 'Errand Updated'),
        ('ERAND_CANCELLED', 'Errand Cancelled'),
        ('APPLICATION_RECEIVED', 'New Application Received'),
        ('APPLICATION_ACCEPTED', 'Application Accepted'),
        ('APPLICATION_REJECTED', 'Application Rejected'),
        ('MESSAGE_RECEIVED', 'New Message Received'),
        ('RATING_RECEIVED', 'New Rating Received'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} - {self.recipient.username}"

    def mark_as_read(self):
        self.is_read = True
        self.save() 