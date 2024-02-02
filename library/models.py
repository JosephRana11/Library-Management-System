from django.db import models
from accounts.models import User 

class Book(models.Model):
    """
    Stores general information about a book.

    Attributes:
        title (str): The title of the book.
        isbn (str): The ISBN of the book.
        genre (str): The genre of the book.
    """

    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=17, unique=True)
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class BookDetail(models.Model):
    """
    Stores detailed information about a book.

    Attributes:
        book (Book): The associated book.
        number_of_pages (int): The number of pages in the book.
        publisher (str): The publisher of the book.
        language (str): The language of the book.
    """

    book = models.OneToOneField(Book, related_name="details", on_delete=models.CASCADE)
    number_of_pages = models.IntegerField()
    publisher = models.CharField(max_length=150)
    language = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.book.title} - {self.publisher} - {self.language}"

class BorrowedBook(models.Model):
    """ 
    Stores information about a borrowed book.

    Attributes:
        borrower (User): The user who borrowed the book.
        book (Book): The borrowed book.
        borrowed_date (Date): The date the book was borrowed.
        returned (bool): Indicates whether the book has been returned.
    """

    borrower = models.ForeignKey(User, related_name="borrowed_books", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="borrowed_by", on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.borrower.username} - {self.book.title} - {self.borrowed_date}"

    class Meta:
        ordering = ["-borrowed_date"]
