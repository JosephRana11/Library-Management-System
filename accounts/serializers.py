from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime , date

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
    fields = ['username' , 'first_name' , 'last_name' , 'email' , 'password' , 'password2', 'membership_date']
  
  def validate(self , data):
    """ 
      Checks if Passwords Match 
      Checks if membership date is Valid
    """
    if data['password'] != data['password2']:
      raise serializers.ValidationError({"Password":"Your Passwords did not Match! Try Again."})

    membership_datetime = data['membership_date']
    if membership_datetime < date.today():
        raise serializers.ValidationError({"Incorrect Entry": "Incorrect Membership date provided"})

    return data
  
  def create(self , valid_data):
    user = User.objects.create(
      username = valid_data['username'],
      email = valid_data['email'],
      first_name =  valid_data['first_name'],
      last_name = valid_data['last_name'],
      membership_date =  valid_data['membership_date']
    )
    user.set_password(valid_data['password'])
    user.save()
    return user
