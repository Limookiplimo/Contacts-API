from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
import jwt, datetime


# Create your views here.
class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')

        user = auth.authenticate(username=username, password=password)

        if user:
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            
            auth_token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')

            serializer = UserSerializer(user)

            data = {'user':serializer.data, 'token':auth_token}

            return Response(data, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Invalid credentials. Try again.'}, status=status.HTTP_401_UNAUTHORIZED)