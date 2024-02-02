from django.urls import include , path   
from  library import views


urlpatterns = [
    path('books/' , views.BooksListAPI.as_view()),
    path('books/<int:book_id>/' , views.BookDetailAPI.as_view()),
    path('borrowed/all/' , views.BorrowedBookAPI.as_view()),
    path('borrow/<int:book_id>/' , views.BorrowBookView),
    path('return/<int:book_id>/' , views.ReturnBookView),
]
