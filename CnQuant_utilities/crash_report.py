import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def send_crash_email(error_message: str, sender: str, receivers: list[str], password: str, app_name: str):
    """Sends an email notification when an application crashes.

    Args:
        error_message (str): The error message or stack trace detailing the crash.
        sender (str): The email address sending the notification (e.g., 'your_email@gmail.com').
        receiver (list[str]): The list of email addresses receiving the notification.
        password (str): The password or app-specific password for the sender's email account.
        app_name (str): The name of the application that crashed, included in the email.

    Raises:
        Exception: If the email fails to send, an error is printed but not raised further.

    Notes:
        - Uses Gmail's SMTP server (smtp.gmail.com:587) with TLS encryption.
        - Requires the sender's email to allow less secure apps or an app-specific password.
        - Includes a timestamp in the format 'YYYY-MM-DD HH-MM-SS' in the subject and body.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    msg = MIMEText(f"{app_name} crashed with error:\n\n{error_message} on {timestamp}")
    msg["Subject"] = f"{app_name} crashed on {timestamp}"
    msg["From"] = sender
    msg["To"] = ", ".join(receivers)

    try:
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as server:
            server.starttls()
            server.login(user=sender, password=password)
            server.sendmail(from_addr=sender, to_addrs=receivers, msg=msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")