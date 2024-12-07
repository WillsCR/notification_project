from celery import shared_task
from notifications.models import Notification
@shared_task(name='notifications.tasks.send_notification')
def send_notification(userId, notification_type, message):
    Notification.objects.create(
        userId=userId,  
        notification_type=notification_type,
        message=message,
        read=False
    )
    return f"Notificación enviada al usuario {userId} con el mensaje: {message}"

@shared_task(name='notifications.tasks.mark_as_read')
def mark_as_read(userId):
    Notification.objects.filter(userId=userId, read=False).update(read=True)
    return f"Notifications for user {userId} marked as read"


@shared_task(name='notifications.tasks.unread')
def unread(userId):
    unread_notifications = Notification.objects.filter(userId=userId, read=False)
    result = [
        {"id": n.id, "message": n.message, "read": n.read}
        for n in unread_notifications
    ]
    return result


@shared_task(name='notifications.tasks.generate_report')
def generate_report():
    total_notifications = Notification.objects.count()
    unread_count = Notification.objects.filter(read=False).count()
    return {
        "total": total_notifications,
        "unread": unread_count,
        "read_percentage": 100 * (total_notifications - unread_count) / total_notifications if total_notifications else 0,
    }
    
@shared_task(name='notifications.tasks.send_daily_summary')
def send_daily_summary(userId):
    notifications = Notification.objects.filter(userId=userId, read=False)
    notification_messages = [notification.message for notification in notifications]
    summary_message = f"Daily summary sent to user {userId}. Notifications: " + ", ".join(notification_messages)
    return summary_message

