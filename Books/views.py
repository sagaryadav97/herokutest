from .serializers import *
from rest_framework import generics, status
from rest_framework.decorators import api_view
from .models import *
from django.shortcuts import get_object_or_404,redirect
from django.db.models import Max
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from Users.permissions import *
from django.db.models import Sum
from django.db.models import Q
from datetime import date
from django.shortcuts import render
from rest_framework.generics import GenericAPIView

def index(request):
    return render(request, "index.html")

class BookCreateView(generics.CreateAPIView): #to create patient registration
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated&IsLIBRARIANUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(['GET', 'DELETE','PUT'])
def BookView(request):
    user = request.user
    if user.Role=="LIBRARIAN":
        try:
            book = Book.objects.all() #get all book details
            if not book:
                return Response({'message': 'The book list is empty'}, status=status.HTTP_404_NOT_FOUND) 
            book_id= request.GET.get('id', None)  #get ID from parameter of url if specified
            if book_id is not None:
                book = book.filter(id=book_id)  #get that specific book from ID
            if not book:
                return Response({'message': 'The book record does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
        except Book.DoesNotExist: 
            return Response({'message': 'The book model does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    # retrieve specific data or all
        if request.method == 'GET': 
            book_serializer = BookSerializer(book, many=True)
            return Response(book_serializer.data)
    # delete specific data or all
        elif request.method == 'DELETE':
            book.delete() 
            return Response({'message': 'Book record was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PUT':
            book = book.filter(id=book_id).first() #get first entry of book with that ID
            serializer=BookSerializer(book,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    return Response({'message': 'You Have No Permission'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST']) 
def ReadView(request):
   if request.method == 'POST':
    user = request.user
    if user.Role=="MEMBER":
        book_id = request.data['id']
        book = get_object_or_404(Book, id=book_id)
        book_already_borrowed = ReadBook.objects.filter(book=book_id, member=user)
        if book_already_borrowed:
            cp = get_object_or_404(ReadBook,book=book_id, member=user)
            cp.save()
        else:
            ReadBook(member=user, book=book).save()
            
            bk=Book.objects.filter(id=book_id).update(status="BORROWED") 
        return Response({"messege":"Succesfully Borrowed"},status=status.HTTP_200_OK)
    return Response({'message': 'You Have No Permission'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE']) 
def ReadDeleteView(request):
   if request.method == 'DELETE':
    user = request.user
    if user.Role=="MEMBER":
        book_id = request.GET.get('id', None)
        book = get_object_or_404(Book, id=book_id)
        book_already_borrowed = ReadBook.objects.filter(book=book_id, member=user)
        book_already_borrowed.delete()
        bk=Book.objects.filter(id=book_id).update(status="AVAILABLE") 
        return Response({"messege":"Succesfully Returned"},status=status.HTTP_200_OK)
    return Response({'message': 'You Have No Permission'},status=status.HTTP_400_BAD_REQUEST)
            
class BookListView(generics.ListAPIView): #to create patient registration
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated&IsMEMBERUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
