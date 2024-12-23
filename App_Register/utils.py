from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework.response import Response
from rest_framework import status
from random import randint, random
import random
import string
import re
from rest_framework.views import exception_handler

class util:
    staticmethod
    email = EmailMessage
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            response = exception_handler(e, context=None)
            if response is None:
                return Response({"status": "failed", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return response
    return wrapper

def send_otp(email):
    if email:
        key = randint(100000, 999999)
        return key
    else:
        return Response({"Error"})
def generate_referral_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# Example usage:
referral_code = generate_referral_code()
print(referral_code)
    
def is_valid_email(email):
      # Define the regex pattern for email validation
      pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      return re.match(pattern, email)


def send_activation_email(user):
    email_body = f"""Dear {user.full_name()},\n\nThank you for registering for the 21st Century Digital Corps Conference 1.0


Overview: The "21st Century Digital Corps" conference is not just a conference; it's a transformative experience tailored specifically for NYSC members. Through engaging sessions, hands-on workshops, and insightful discussions, participants will delve into the intricacies of modern technology and discover how it can be leveraged to unlock their full potential.


Objectives:\n
Empowerment: Provide NYSC members with practical knowledge and skills in various aspects of technology, empowering them to adapt and excel in an increasingly digital world.

Inspiration: Inspire corps members to embrace technology as a catalyst for personal and professional growth, igniting their passion for innovation and creativity.

Networking: Facilitate meaningful connections and collaborations among NYSC members, industry experts, and technology enthusiasts, fostering a vibrant community of digital pioneers.

Impact: Foster a culture of technological excellence and innovation within the NYSC community, driving positive change and progress in society.

Program Highlights:\n
Keynote Addresses: Renowned experts and thought leaders will share their insights on the latest trends and advancements in technology, inspiring participants to embrace innovation and change.

Date: 26th May 2024
Time: 12PM to 3PM
Location: Hunkies, On-George bustop, Ikotun

If you have any questions or need further assistance, feel free to reply to this email or contact us at 08068535646, 08062871275"""
    data = {'email_body': email_body, 'to_email': user.email, 'email_subject': "Confirmation: You're Registered for the 2CDC Conference 1.0"}
    util.send_email(data)