from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserModel
        fields='__all__'

class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={"input_type":"password"},write_only=True)
   
    class Meta:
        model=UserModel
        fields=['username','password','Role']
        extra_kwargs={'password':{'write_only'}}
    def save(self,**kwargs):
        user=UserModel(
            username=self.validated_data['username'],
            Role=self.validated_data['Role'],
        )
        password=self.validated_data['password']
        user.set_password(password)
        
        if user.Role=="LIBRARIAN":  
            user.is_admin=True
            user.is_superuser=True
            user.is_staff=True
            user.save()
        if user.Role=="MEMBER":
            user.is_admin=False
            user.is_superuser=False
            user.is_staff=True
            user.save()
        return user