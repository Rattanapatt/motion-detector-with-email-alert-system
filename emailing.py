import smtplib
import imghdr
from email.message import EmailMessage
import os
import glob
from threading import Thread

SENDER = os.getenv("EMAIL")
PASSWORD = os.getenv("TEST_PASSWORD")
RECEIVER = os.getenv("EMAIL")

def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

def send_email(image_path, time_arr):
    current_date = time_arr["current_date"]
    current_time = time_arr["current_time"]
    email_message = EmailMessage()
    email_message["Subject"] = "New object detected!"
    email_message.set_content(f"New object detected at {current_time} on {current_date}.")
    
    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))
    
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    
    print("Email was sent!")
    
    clean_folder_thread = Thread(target=clean_folder)
    clean_folder_thread.daemon = True
    clean_folder_thread.start()
    
if __name__ == "__main__":
    print("Main")