from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('CLIENT', 'Client'),
        ('TASKER', 'Tasker'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CLIENT')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    profile_picture = models.ImageField(upload_to='errands/profile_pictures/', blank=True, null=True)
    
    def __str__(self):
        return self.username
