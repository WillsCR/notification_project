import pytest 
from notifications.models import Notification
from notifications.task import *



### TEST CELEY

@pytest.mark.django_db
def test_send_notification():
    userId = 1 
    notification_type = "info"
    message = "Test notification"
    result = send_notification.apply(args=(userId, notification_type, message)).get()
    notification = Notification.objects.get(userId=userId, notification_type=notification_type)
    assert notification.message == message
    assert notification.read is False
    assert result == f"Notificación enviada al usuario {userId} con el mensaje: {message}"

@pytest.mark.django_db
def test_mark_as_read():
    userId = 1
    Notification.objects.create(userId=userId, notification_type="info", message="Unread notification", read=False)
    result = mark_as_read.apply(args=(userId,)).get()
    notifications = Notification.objects.filter(userId=userId)
    assert all(n.read for n in notifications)
    assert result == f"Notifications for user {userId} marked as read"

@pytest.mark.django_db
def test_unread():
    userId = 1
    Notification.objects.create(userId=userId, notification_type="info", message="Unread notification", read=False)
    Notification.objects.create(userId=userId, notification_type="info", message="Read notification", read=True)
    result = unread.apply(args=(userId,)).get()
    assert len(result) == 1
    assert result[0]["message"] == "Unread notification"
    assert result[0]["read"] is False

@pytest.mark.django_db
def test_generate_report():
    Notification.objects.create(userId=1, notification_type="info", message="Unread notification", read=False)
    Notification.objects.create(userId=2, notification_type="info", message="Read notification", read=True)
    result = generate_report.apply().get()
    assert result["total"] == 2
    assert result["unread"] == 1
    assert result["read_percentage"] == 50.0

@pytest.mark.django_db
def test_send_daily_summary():
    userId = 1
    Notification.objects.create(userId=userId, notification_type="info", message="Notification 1", read=False)
    Notification.objects.create(userId=userId, notification_type="info", message="Notification 2", read=False)
    result = send_daily_summary.apply(args=(userId,)).get()
    assert "Notification 1" in result
    assert "Notification 2" in result
    assert result == f"Daily summary sent to user {userId}"
    
### TEST VIEWS