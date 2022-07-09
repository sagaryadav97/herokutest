from . serializers import *
from .models import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

class SignupView(generics.GenericAPIView):
    serializer_class= SignupSerializer
    def post(self, request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user":UserSerializer(user,context=self.get_serializer_context()).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
         
        },status=status.HTTP_201_CREATED)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request,*args,**kwargs):
        serializer= self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        refresh=RefreshToken.for_user(user=user)
        return Response({
            "user_id":user.pk,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role":user.Role,   
        },status=status.HTTP_200_OK)
        
@api_view(['GET', 'DELETE','PUT'])
def MemberView(request):
    user = request.user
    if user.Role=="LIBRARIAN":
        try:
            users = UserModel.objects.all() #get all user details
            if not users:
                return Response({'message': 'The user list is empty'}, status=status.HTTP_404_NOT_FOUND) 
            user_id= request.GET.get('id', None)  #get ID from parameter of url if specified
            if user_id is not None:
               users = users.filter(id=user_id,Role="MEMBER")  #get that specific user from ID
            if not users:
                return Response({'message': 'The user record does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
        except UserModel.DoesNotExist: 
            return Response({'message': 'The user model does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    # retrieve specific data or all
        if request.method == 'GET': 
            user_serializer = UserSerializer(users, many=True)
            return Response(user_serializer.data)
    # delete specific data or all
        elif request.method == 'DELETE':
            users.delete() 
            return Response({'message': 'User record was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PUT':
            user = users.filter(id=user_id,Role="MEMBER").first() #get first entry of user with that ID
            serializer=UserSerializer(users,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    return Response({'message': 'You Have No Permission'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def DeleteAccountView(request):
    user = request.user
    if user.Role=="MEMBER":
        try:
            users = UserModel.objects.all() 
            if not users:
                return Response({'message': 'The user list is empty'}, status=status.HTTP_404_NOT_FOUND) 
            user_id= request.GET.get('id', None)  
            if user_id is not None:
                users = users.filter(id=user_id)  
            if not users:
                return Response({'message': 'No any User Exist'}, status=status.HTTP_404_NOT_FOUND) 
 
        except UserModel.DoesNotExist: 
            return Response({'message': 'The user model does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    # delete specific data or all
        if request.method == 'DELETE':
            users.delete() 
            return Response({'message': 'Your Account is deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'message': 'You Have No Permission'},status=status.HTTP_400_BAD_REQUEST)