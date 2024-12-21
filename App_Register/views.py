from django.http import JsonResponse
from django.shortcuts import render

from App import settings
from . models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import TokenAuthentication
from random import randint
from rest_framework.views import APIView
from knox.auth import AuthToken
from rest_framework.permissions import IsAuthenticated
from App_Register.serializers import *
import re
from . utils import *
from django.utils import timezone


# Create your views here.

def send_otp(email):
    if email:
        key = randint(100000, 999999)
        return key
    else:
        return Response({"Error"})

# Example usage:
referral_code = generate_referral_code()
print(referral_code)
    
def is_valid_email(email):
      # Define the regex pattern for email validation
      pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      return re.match(pattern, email)

# Account activation email
def send_activation_email(user):
    email_body = f"""Dear {user.first_name},\n\nThank you for registering for the 21st Century Digital Corps Conference 1.0


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


class Reg(generics.GenericAPIView):
    serializer_class = RegSerializer

    def post(self, request):
        email = request.data["email"]
        phone = request.data["phone"]

        if Register.objects.filter(email=email):
            return Response({"status": "failed", "message": "Email already registered"}, status=status.HTTP_409_CONFLICT)
        if not is_valid_email(email):
            return Response({"status": "failed", "message": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        elif Register.objects.filter(phone=phone):
             return Response({"status": "failed", "message": "Phone already registered"}, status=status.HTTP_409_CONFLICT)
        
        else:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            send_activation_email(user)

            return Response({
                "status": "success",
                "message": "Registered successfully",
                "data": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": user.phone,
                    "gender": user.gender,
                    "technical_skill": user.technical_skill,
                    "heard_by": user.heard_by,
                    "location": user.location,
                }
            }, status=status.HTTP_201_CREATED)

# 