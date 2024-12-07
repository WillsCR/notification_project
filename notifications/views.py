from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from notifications.task import mark_as_read, unread, send_notification  

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    
    def get_queryset(self):
        user_id = self.request.headers.get('userId')
        return Notification.objects.filter(userId=self.request.user.id)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.read = True
        notification.save()

        # Llamamos a la tarea asincrónica de Celery para marcar como leída
        mark_as_read.delay(self.request.user.id)

        return Response({'status': f'Notification {pk} marked as read'})

    
    @action(detail=False, methods=['post'])
    def unread2(self, request):
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"error": "user_id parameter is required in body"}, status=400)

        unread_notifications = Notification.objects.filter(userId=user_id, read=False)
        serializer = self.get_serializer(unread_notifications, many=True)

       
        unread.delay(user_id)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        user_id = self.request.headers.get('userId')
        unread_notifications = Notification.objects.filter(userId=user_id, read=False)
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_notification(self, request):
        user_id = self.request.headers.get('userId')
        message = request.data.get('message', 'No message provided')
        notification_type = request.data.get('notification_type', 'info')
        notification = Notification.objects.create(userId=user_id, message=message, notification_type=notification_type)
        notification.save()
        

        return Response({'status': 'Notification enqueued'})