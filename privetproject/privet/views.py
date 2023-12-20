from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView,\
    ListAPIView, RetrieveAPIView
from .models import User, UserInfo
from .serializers import StudentSerializer, BuddySerializer, StudentSignupSerializer,\
    BuddySignupSerializer, BaseUserSerializer, StudentArrivalBookingSerializer,\
    ArrivalBookingSerializer, BuddyArrivalsSerializer, ArrivalOtherStudentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Student, Buddy, ArrivalBooking, BuddyArrival
from .permissions import IsStudentUser, IsBuddyUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from .authtoken import ObtainAuthToken


class StudentProfileView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated&IsStudentUser]


class BuddyProfileView(RetrieveUpdateDestroyAPIView):
    queryset = Buddy.objects.all()
    serializer_class = BuddySerializer
    permission_classes = [IsAuthenticated&IsBuddyUser]


class ArrivalBookingView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentArrivalBookingSerializer

class AllArrivalBookingsView(ListAPIView):
    queryset = ArrivalBooking.objects.all()
    serializer_class = ArrivalBookingSerializer


class DefiniteArrivalBookingView(RetrieveAPIView):
    queryset = ArrivalBooking.objects.all()
    serializer_class = ArrivalBookingSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        buddy_arrival = BuddyArrival.objects.filter(student__arrival_booking=instance).first()
        buddy_count = Buddy.objects.filter(buddy_arrivals__student__arrival_booking=instance)
        serializer = self.get_serializer(instance)
        data = serializer.data
        student_count = instance.other_students.count() + 1
        data['student_count'] = student_count
        if buddy_arrival:
            buddy = Buddy.objects.get(buddy_arrivals=buddy_arrival)
            buddy_info = buddy.user.user_info

            buddy_amount = buddy_count.count()
            data['buddy_amount'] = buddy_amount
            if buddy_info is None:
                data['buddy_full_name'] = 'None'
            else:
                data['buddy_full_name'] = buddy_info.full_name
            return Response(data)
        else:
            return Response(data)

class AddArrivalToBuddy(APIView):
    def post(self, request, *args, **kwargs):
        buddy_id = request.data.get('buddy_id')
        buddy = Buddy.objects.get(pk=buddy_id)
        student_id = request.data.get('student_id')
        student = Student.objects.get(pk=student_id)
        buddy_arrival = BuddyArrival.objects.create(student=student)
        buddy.buddy_arrivals.add(buddy_arrival)
        buddy.save()
        serializer = BuddySerializer(buddy)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BuddyArrivalsView(RetrieveAPIView):
    queryset = Buddy.objects.all()
    serializer_class = BuddyArrivalsSerializer
    lookup_field = 'user'


class ArrivalOtherStudentView(APIView):
    def post(self, request, *args, **kwargs):
        student_name = request.data.get('student_name')
        other_info_student = UserInfo.objects.get(full_name=student_name)
        other_user_student = User.objects.get(user_info=other_info_student)
        other_student = Student.objects.get(user=other_user_student)
        student_id = request.data.get('student_id')
        student = Student.objects.get(pk=student_id)
        arrival_booking = student.arrival_booking
        arrival_booking.other_students.add(other_student)
        arrival_booking.save()
        serializer = ArrivalOtherStudentSerializer(arrival_booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




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