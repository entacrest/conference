from django.urls import path, include
from . import views
from App_Register.views import *
from knox import views as knox_views


#  SWAGGER
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Entacrest Web",
      default_version='v1',
      description="This is Entacrest Web API Doc",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="jedida@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   path('register/', Reg.as_view(), name='register'), # register

   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('go/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
  
]