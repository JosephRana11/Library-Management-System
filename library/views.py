from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import authentication_classes , permission_classes , api_view
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views

from accounts.models import User 
from .serializers import BookListSerializer , BookSerializer
from .models import Book , BookDetail , BorrowedBook

class BooksListAPI(generics.ListCreateAPIView):
  """
   GET 

    Returns Books List for /api/books/ endpoint.
   
   POST 
    
    *requires user authentication
      Creates New Book for /api/books/ endpoint

  """
  queryset = Book.objects.all()
  serializer_class = BookListSerializer
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookDetailAPI(views.APIView):
  """"
   GET

     Returns Detailed Information of a Book (Book + BookDetail)
   
   PATCH
    
    *Requires Staff authentication - Session Token
     Updates Both Book Model and BookDetail Model using Nested Serialization.

  """
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  #overriding super class Get method:
  def get(self , request , book_id):
    book = Book.objects.get(id = book_id)
    if book is not None:
      serializer = BookSerializer(book)
      return Response(serializer.data , status = status.HTTP_200_OK)
    else:
      return Response({"message":"Book does not exist"} , status = status.HTTP_204_NO_CONTENT)
  
  
  #overriding Super class Update Method:
  def patch(self , request , book_id):
    book = Book.objects.get(id = book_id)
    if book is None:
      return Response({"message":"Book does not Exist"} , status = status.HTTP_204_NO_CONTENT)
    #checking if user has necessary permissions
    if request.user.is_staff:
        #passing book , instance data to serializer for partial update
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data , status = status.HTTP_200_OK)
        else:
          return Response({"error":f"{str(serializer.errors)}"} , status = status.HTTP_400_BAD_REQUEST)
    else:
      return Response({"Message":"ACCESS DENIED"} , status = status.HTTP_401_UNAUTHORIZED)
  
  #overwriting super class delete function
  def delete(self , request , book_id):
    book = Book.objects.get(id = book_id)
    if book is None:
      return Response({"message":"Book does not Exist"} , status = status.HTTP_400_BAD_REQUEST)
    #checking user permission
    if request.user.is_staff:
      book.delete()
      return Response({"message":"Book Removed Sucessfully"} , status = status.HTTP_200_OK)
    else:
      return Response({"Message":"ACCESS DENIED"} , status = status.HTTP_401_UNAUTHORIZED)
