from django.contrib import admin

from .models import Book , BookDetail , BorrowedBook

admin.site.register(Book)
admin.site.register(BookDetail)
admin.site.register(BorrowedBook)