from django.http import JsonResponse
from django.shortcuts import render
from . models import Register
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from App_Register.serializers import RegSerializer
from . utils import is_valid_email, send_activation_email, handle_exceptions




class RegistrationView(viewsets.ViewSet):
    serializer_class = RegSerializer


    @handle_exceptions
    def register(self, request):
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