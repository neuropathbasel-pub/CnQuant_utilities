import smtplib
import traceback
from email.mime.text import MIMEText
from datetime import datetime

def send_crash_email(error_message: str, sender: str, receiver: str, password: str, app_name: str):
    timestamp = datetime.now().strftime(format='%Y-%m-%d %H-%M-%S')
    msg = MIMEText(f"{app_name} crashed with error:\n\n{error_message} on {timestamp}")
    msg["Subject"] = f"{app_name} crashed on {timestamp}"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as server:
            server.starttls()
            server.login(user=sender, password=password)
            server.sendmail(from_addr=sender, to_addrs=receiver, msg=msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")