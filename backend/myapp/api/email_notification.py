import smtplib
from dotenv import load_dotenv
import os
from email.message import EmailMessage
from .database import db


def send_notification(user_id):

    user_email = db.child("users").child(user_id).child("email").get().val()
    print(user_email)

    load_dotenv()
    gmail_password = os.environ.get('GMAIL_PASSWORD')

    try:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)

        smtp.starttls()
        smtp.login("coktailmaestro@gmail.com", gmail_password) # type: ignore

        msg = EmailMessage()
        msg['Subject'] = "Your Drink is Ready!"
        msg['From'] = "coktailmaestro@gmail.com"
        msg['To'] = user_email
        msg.set_content("")

        smtp.send_message(msg)
        smtp.quit()
        return {"message": "Email sent successfully!"}

    except Exception as ex:
        print('Email error!')
        return {"message": f"Something went wrong: {ex}"}
