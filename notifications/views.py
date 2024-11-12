from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    #permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden ver las notificaciones
    
    #def get_queryset(self):
        # Filtrar las notificaciones solo para el usuario autenticado
       # return Notification.objects.filter(user=self.request.user)
