from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView
from .models import User, UserInfo
from .serializers import StudentSerializer, BuddySerializer, StudentSignupSerializer, BuddySignupSerializer, BaseUserSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Student, Buddy
from .permissions import IsStudentUser, IsBuddyUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from .authtoken import ObtainAuthToken

# Create your views here.


class StudentProfileView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated&IsStudentUser]


class BuddyProfileView(RetrieveUpdateDestroyAPIView):
    queryset = Buddy.objects.all()
    serializer_class = BuddySerializer
    permission_classes = [IsAuthenticated&IsBuddyUser]

class StudentSignupView(GenericAPIView):
    serializer_class = StudentSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": BaseUserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "account created"
        })

class BuddySignupView(GenericAPIView):
    serializer_class = BuddySignupSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": BaseUserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "account created"
        })


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created=Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_buddy': user.is_buddy,
        })


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)