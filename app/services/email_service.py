import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")


async def send_reset_email(email: str, code: str):
    message = Mail(
        from_email=SENDGRID_FROM_EMAIL,
        to_emails=email,
        subject="Password Reset Request",
        html_content=f"""
            <p>Your password reset code is:</p>
            <h2>{code}</h2>
            <p>Please open the GymBuds app and enter this code to reset your password.</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"SendGrid Response: {response.status_code}")
    except Exception as e:
        print("SendGrid error:", e)