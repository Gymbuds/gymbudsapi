from fastapi_mail import FastMail, MessageSchema
from app.services.config import mail_config

async def send_reset_email(email: str, reset_token: str):
    reset_link = f"http://127.0.0.1:8000/docs#/auth/reset-password/{reset_token}"
    
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],  
        body=f"Click the link to reset your password: {reset_link}",
        subtype="html",
    )

    fm = FastMail(mail_config)
    await fm.send_message(message)
