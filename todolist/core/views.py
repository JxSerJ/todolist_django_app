from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import User
from .serializers import SignUpSerializer, LoginSerializer


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'password': ['Incorrect password']})
