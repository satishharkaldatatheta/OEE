from services.notification_generator import generate_notifications
from services.email_sender import send_user_notifications

if __name__ == "__main__":
    generate_notifications()
    send_user_notifications()
