from django.http import JsonResponse
from django.shortcuts import render

from App import settings
from . models import Register
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
from App_Register.serializers import RegSerializer

from . utils import *
from django.utils import timezone


# Create your views here.





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

            return Response({"status": "success", "message": "Registered successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

# 