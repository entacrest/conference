from django.contrib import admin
from App_Register.models import *

class RegisterAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone',]
    list_filter = ['first_name']
    search_fields = ['last_name']

admin.site.register(Register, RegisterAdmin)
# Register your models here.
