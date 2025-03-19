from fastapi_mail import FastMail, MessageSchema
from app.services.config import mail_config


async def send_reset_email(email: str, code: str):
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body=f"Your password reset code is: {code}\n\nPlease open the GymBuds app and enter this code.",
        subtype="html"
    )


    fm = FastMail(mail_config)
    await fm.send_message(message)
