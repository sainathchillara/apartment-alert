import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Replace with your actual sender email & password
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"  # Use app-specific password if 2FA is enabled

def send_alert_email(recipient_email: str, alert_data: dict):
    subject = "New Apartment Alert Created"
    body = f"""
    Hi,

    Your new apartment alert has been created with the following details:

    Location: {alert_data.get("location")}
    Min Price: {alert_data.get("min_price")}
    Max Price: {alert_data.get("max_price")}
    Bedrooms: {alert_data.get("bedrooms")}

    Thank you!
    """

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
        print(f"✅ Email sent to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
