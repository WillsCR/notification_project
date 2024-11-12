from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'  #['id', 'user', 'notification_type', 'message', 'created_at', 'read']