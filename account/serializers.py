from django.forms import ValidationError
from rest_framework import serializers
from account.models import User
from django.contrib.auth.hashers import check_password

# for emailing reset doken
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util

class UserRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type:password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'tc', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # validating password
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Password and Confirm Password must match'})
        return data

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,
                                     style={'input_type': 'password'},
                                     write_only=True)
    password2 = serializers.CharField(max_length=255,
                                      style={'input_type': 'password'},
                                      write_only=True)
    old_password = serializers.CharField(max_length=255,
                                         style={'input_type': 'password'},
                                         write_only=True)

    class Meta:
        fields = ['old_password', 'password', 'password2']

    def validate(self, data):
        user = self.context.get('user')
        old_password = data.get('old_password')
        password = data.get('password')
        password2 = data.get('password2')
        if not check_password(old_password, user.password):
            raise serializers.ValidationError(
                {'old_password': 'Old password is incorrect.'})
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Password and Confirm Password must match'})
        user.set_password(password)
        user.save()
        return data


class UserSendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            #Send Email
            body= 'Click Following Link to Reset your password'+link
            data={
                'email_subject':'Reset your password',
                'body':body,
                'to_email':user.email
            }
            Util.send_mail(data)
            
            return data
        else:
            raise ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,
                                     style={'input_type': 'password'},
                                     write_only=True)
    password2 = serializers.CharField(max_length=255,
                                      style={'input_type': 'password'})

    class Meta:
        fields = ['password', 'password2']

    def validate(self, data):
        try:
            password = data.get('password')
            password2 = data.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError(
                    {'password': 'Password and Confirm Password must match'})
            id=smart_str(urlsafe_base64_decode(uid))
            user= User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError(
                    'Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return data
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError(
                    'Token is not Valid or Expired')
            