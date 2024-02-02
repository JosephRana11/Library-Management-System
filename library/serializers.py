from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from django.utils import timezone
from datetime import date


from .models import Book , BookDetail , BorrowedBook


class BookListSerializer(serializers.ModelSerializer):
  """
  Serializes Book Model object
  """
  class Meta:
    model = Book 
    fields = '__all__'

class BookDetailSerializer(serializers.ModelSerializer):
  """
   Serializes Book Detail Model Object
  """
  class Meta:
    model = BookDetail
    fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
  """
   Serializes Book Model + Book Detail
  """
  details = BookDetailSerializer()
  class Meta:
    model = Book 
    fields = '__all__'