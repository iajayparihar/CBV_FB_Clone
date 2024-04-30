from rest_framework import serializers
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    class  Meta:
        model = CustomUser
        fields = '__all__'
        managed = True
        verbose_name = 'Register'
        verbose_name_plural = 'Registers'

class LoginApiSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 255)
    class Meta:
        model = CustomUser
        fields = ['username','password']
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name']
        

class ChangePasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password1','password2']
        
    def validate(self,data):
        password1 = data.get('password1')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password1 != password2:
            raise serializers.ValidationError("password and confirm password not matching")
        user.set_password(password1)
        user.save()
        return data