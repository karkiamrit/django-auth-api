from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegisterationSerializer, UserLoginSerializer

class UserRegisterationView(APIView):
    def post(self,request, format=None):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({'message': 'Registeration Success'}, 
                            status=status.HTTP_201_CREATED
        )
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginView(APIView):
    def post(self,request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({'message': 'Login Success'}, 
                            status=status.HTTP_200_OK
        )
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
        
                