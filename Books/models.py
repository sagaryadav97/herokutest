from django.db import models
from Users.models import *
class Book(models.Model):
    book_name = models.CharField(max_length=150, verbose_name="Books Name")
    book_description=models.CharField(max_length=150, verbose_name="Books Description")
    BOOK_STATUS=(
        ('BORROWED','BORROWED'),
        ('AVAILABLE','AVAILABLE'),
    )
    status=models.CharField(max_length=200,blank=False,null=False, choices=BOOK_STATUS,default="AVAILABLE")
    
    def __str__(self):
        return f"{self.book_name}"
    
class ReadBook(models.Model):
    member = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    book=models.ForeignKey(Book, on_delete=models.CASCADE)