from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from .models import User, UserInfo
from .serializers import UserInfoEditSerializer

# Create your views here.

class UserInfoEditAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoEditSerializer