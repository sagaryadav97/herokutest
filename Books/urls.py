from django.urls import path
from .views import *
urlpatterns = [
    path('GetUpdateDeleteBook/',BookView),
    #http://localhost:8000/book/GetUpdateDeleteBook/?id=1
    path('BookCreate/',BookCreateView.as_view(), name='BookCreateView'),
    #http://localhost:8000/book/BookCreate/
    path('readbook/',ReadView),
    #http://localhost:8000/book/readbook/
    path('returnbook/',ReadDeleteView),
    #http://localhost:8000/book/returnbook/
    path('viewbook/',BookListView.as_view(), name='BookView'),
    #http://localhost:8000/book/viewbook/
   
]