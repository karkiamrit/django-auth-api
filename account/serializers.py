from rest_framework import serializers
from account.models import User

class UserRegisterationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type:password'}, write_only=True)
    class Meta:
        model= User
        fields=['email','name','tc', 'password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
    #validating password
    def validate(self,data):
        password =data.get('password')
        password2 =data.get('password2')
        if password!=password2:
            raise serializers.ValidationError({'password':'Password and Confirm Password must match'})
        return data    

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    
    
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_Length=255)
    class Meta:
        model= User
        fields=['email', 'password']
       
    