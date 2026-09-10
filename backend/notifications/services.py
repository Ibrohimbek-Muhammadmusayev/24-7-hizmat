"""
Firebase Cloud Messaging (FCM) Push Notification Service
"""
try:
    import firebase_admin
    from firebase_admin import messaging, credentials
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

def send_push_notification(token, title, body, data=None):
    if not FIREBASE_AVAILABLE or not token:
        print(f"[Mock Push Notification] Title: '{title}', Body: '{body}', Token: '{token}'")
        return False

    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            token=token,
        )
        response = messaging.send(message)
        print("FCM message sent successfully:", response)
        return True
    except Exception as e:
        print("Error sending FCM push notification:", e)
        return False
