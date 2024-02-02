from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
  ''' Using Custom User Model'''
  membership_date = models.DateField(auto_now_add= True)
  
  def __str__(self):
      return self.username
  
  class Meta:
    ordering = ["-date_joined"]
  