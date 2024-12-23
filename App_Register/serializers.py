from django.contrib.auth.models import User
from . models import *
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import *
import random
import string

def generate_referral_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


class RegSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Register
        fields = ['first_name', 'last_name', 'email', 'phone', 'gender', 'technical_skill', 'heard_by', 'location']
