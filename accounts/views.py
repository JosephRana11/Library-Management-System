from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import User
from .serializers import UserViewSerializer , UserRegisterSerializer
from rest_framework import generics
from rest_framework import permissions

class UserViewAPI(ReadOnlyModelViewSet):
  """
  GET

   Returns List of Users for api/users/ endpoint.

   Returns details of a Single User for api/users/userid/ endpoint.

  """
  queryset = User.objects.all()
  serializer_class = UserViewSerializer

class UserRegisterAPI(generics.CreateAPIView):
  permission_classes = [permissions.AllowAny,]
  serializer_class = UserRegisterSerializer
  