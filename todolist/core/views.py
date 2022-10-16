from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from .models import User
from .serializers import SignUpSerializer


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
