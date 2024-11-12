from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    
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

 
