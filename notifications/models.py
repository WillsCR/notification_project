from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    
    userId = models.IntegerField()

    NOTIFICATION_TYPES = [
        ('info', 'Información'),
        ('warning', 'Advertencia'),
        ('error', 'Error'),
        ('success', 'Éxito'),
    ]
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return  f"Notification for user {self.userId} - {self.notification_type}"

 
