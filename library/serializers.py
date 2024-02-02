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
  

  #overriding the super class update method for nested update for Book and BookDetails
  def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        instance = super().update(instance, validated_data)

        if details_data:
            detail_serializer = self.fields['details']
            detail_instance = instance.details
            detail_serializer.update(detail_instance, details_data)

        return instance

class BorrowedBookSerializer(serializers.ModelSerializer):
  class Meta:
    model = BorrowedBook
    fields = ['id', 'borrower', 'book', 'borrowed_date', 'returned']
  
  #overriding super class representation to include nested data
  def to_representation(self , instance):
    representation = super().to_representation(instance)
     
    #adding nested repreesentatin for borrower user
    representation['borrower'] = {
      'user_id': instance.borrower.id,
      'username' : instance.borrower.username
    }
    
    #adding nested representation for borrowed book
    representation['book'] = {
      'book_id' : instance.book.id,
      'title' : instance.book.title
    }

    return representation

class BorrowBookSerializer(serializers.ModelSerializer):
  class Meta:
    model = BorrowedBook
    fields = ['borrower', 'book', 'borrowed_date', 'returned']
