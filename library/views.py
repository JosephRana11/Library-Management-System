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
from rest_framework.decorators import api_view , permission_classes , permission_classes

from accounts.models import User 
from .serializers import BookListSerializer , BookSerializer , BorrowedBookSerializer , BorrowBookSerializer
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

   DELETE
    
    *Requires Staff authentication - Session Token
     DELETES BOOK Model and its Detail

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

class BorrowedBookAPI(generics.ListAPIView):
  """
   GET
    
    Returns List of all actively borrowed Books .

  """
  queryset = BorrowedBook.objects.filter(returned=False)
  serializer_class = BorrowedBookSerializer

@api_view(['POST',])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def BorrowBookView(request, book_id):
    """
     POST 
      
      Creates BorrowedBook Model instance using request.uesr and book_id

    """
    #checking if the book with the book id exists
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"Message": "Book does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    #checking if book is already borrowed
    try:
        borrowed_book = BorrowedBook.objects.get(book=book, returned=False)
        return Response({"message": "Book is already borrowed"}, status=status.HTTP_400_BAD_REQUEST)
    except BorrowedBook.DoesNotExist:
        instance = BorrowedBook(borrower=request.user, book=book)
        instance.save()
        return Response({"message": "Book borrowed successfully"}, status=status.HTTP_200_OK)

@api_view(['POST',])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def ReturnBookView(request , book_id):
    """
     POST

       Returns BorrowedBook sets BorrowedBook.returned to True

     """
  #checking if the book with the book id exists
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"Message": "Book does not exist"}, status=status.HTTP_404_NOT_FOUND)
  
  #check if user currenty owns the book , if user owns the book set returned to True else return error
    try:
      borrowed_book = BorrowedBook.objects.get(borrower = request.user , book = book , returned = False)
      borrowed_book.returned = True
      borrowed_book.save()
      return Response({"Message":"Book Sucessfully Returned"} , status = status.HTTP_200_OK)
    except BorrowedBook.DoesNotExist:
      return Response({"Message":"You do not currently borrow the Book"} , status = status.HTTP_400_BAD_REQUEST)

    
