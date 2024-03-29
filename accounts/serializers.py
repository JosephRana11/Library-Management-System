from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from django.utils import timezone
from datetime import date

from .models import User 

#Serializer for Viewing Users
class UserViewSerializer(serializers.ModelSerializer):
  class Meta:
    model = User 
    fields = ['username','first_name' , 'last_name' , 'email' , 'membership_date']


#Serializer for Creating New User
class UserRegisterSerializer(serializers.ModelSerializer):

  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = User 
    fields = ['username' , 'first_name' , 'last_name' , 'email' , 'password' , 'password2']
  

  def validate(self, data):
    """ 
      Checks if Passwords Match 
    """
    if data['password'] != data['password2']:
        raise serializers.ValidationError({"Password": "Your Passwords did not Match! Try Again."})

    membership_date = data.get('membership_date')

    return data

  def create(self , valid_data):
    user = User.objects.create(
      username = valid_data['username'],
      email = valid_data['email'],
      first_name =  valid_data['first_name'],
      last_name = valid_data['last_name'],
    )
    user.set_password(valid_data['password'])
    user.save()
    return user
