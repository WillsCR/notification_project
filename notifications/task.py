from celery import shared_task
from notifications.models import Notification
import pika
import json 

#SE TIENE QUE ESPECIFICAR LA TAREA EN EL APIGATEWAY

@shared_task(name='notifications.tasks.send_notification')
def send_notification(user_id, notification_type, message):
    Notification.objects.create(
        user_id=user_id, 
        notification_type=notification_type,
        message=message,
        read=False
    )
    return f"Notification sent to user {user_id} with message: {message}"


@shared_task(name='notifications.tasks.mark_as_read')
def mark_as_read(user_id):
    Notification.objects.filter(user_id=user_id, read=False).update(read=True)
    return f"Notifications for user {user_id} marked as read"


@shared_task(name='notifications.tasks.unread')
def unread(user_id):
    unread_notifications = Notification.objects.filter(userId=user_id, read=False)
    result = [
        {"id": n.id, "message": n.message, "read": n.read}
        for n in unread_notifications
    ]
    return result