from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import authentication_classes , permission_classes , api_view
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserViewSerializer , UserRegisterSerializer
class UserViewAPI(ReadOnlyModelViewSet):
  """
  GET

   1) Returns List of Users for api/users/ endpoint.

   2) Returns details of a Single User for api/users/userid/ endpoint.

  """
  queryset = User.objects.all()
  serializer_class = UserViewSerializer

class UserRegisterAPI(generics.CreateAPIView):
  """
  POST 
   
   1) Creates New User Account for api/register/ end point.

  """
  permission_classes = [permissions.AllowAny,]
  serializer_class = UserRegisterSerializer
  
@api_view(["POST",])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAuthenticated])
def LogoutAPI(request):
  if request.method == "POST":
    request.user.auth_token.delete()
    return Response({"message": "User logged out sucessfully"} , status = status.HTTP_200_OK)
    