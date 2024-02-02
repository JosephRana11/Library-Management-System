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

class BooksListAPI(generics.ListAPIView):
  """
   Returns Books List for /api/books/ endpoint.
  """
  queryset = Book.objects.all()
  serializer_class = BookListSerializer

class BookDetailAPI(views.APIView):
  """"
   Returns Detailed Information of a Book
  """
  def get(self , request , book_id):
    book = Book.objects.get(id = book_id)
    if book is not None:
      serializer = BookSerializer(book)
      return Response(serializer.data , status = status.HTTP_200_OK)
    else:
      return Response({"message":"Book does not exist"} , status = status.HTTP_204_NO_CONTENT)
    
