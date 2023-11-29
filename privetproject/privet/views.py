from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from .models import User, UserInfo
from .serializers import UserInfoEditSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UserInfoEditAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoEditSerializer
    permission_classes = (IsAuthenticated, )