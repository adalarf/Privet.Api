from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView,\
    ListAPIView, RetrieveAPIView
from .models import User, UserInfo
from .serializers import StudentSerializer, BuddySerializer, StudentSignupSerializer,\
    BuddySignupSerializer, BaseUserSerializer, StudentArrivalBookingSerializer,\
    ArrivalBookingSerializer, BuddyArrivalsSerializer, ArrivalOtherStudentSerializer, \
    ArrivalBookingInfoSerializer, DefiniteArrivalBookingSerializer
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

class AllArrivalBookingsView(APIView):
    def get(self, request):
        arrival_bookings = ArrivalBooking.objects.all()
        serializer = ArrivalBookingInfoSerializer(arrival_bookings, many=True)
        data = serializer.data
        for i in data:
            test = Student.objects.get(arrival_booking=i['id'])
            buddy_count = Buddy.objects.filter(buddy_arrivals__student__arrival_booking=i['id'])
            buddies_amount = buddy_count.count()
            i['buddies_amount'] = buddies_amount

            other_stud_set = test.arrival_booking.other_students.all()
            other_stud = ''.join([j.user.user_info.full_name for j in other_stud_set])
            other_stud_citizenship = ''.join([j.citizenship for j in other_stud_set])
            if other_stud == '':
                i['group_full_names'] = f"{test.user.user_info.full_name}"
                i['group_countries'] = f"{test.citizenship}"
            else:
                i['group_full_names'] = f"{test.user.user_info.full_name} {other_stud}"
                i['group_countries'] = f"{test.citizenship} {other_stud_citizenship}"

        return Response(data)


class DefiniteArrivalBookingView(RetrieveAPIView):
    queryset = ArrivalBooking.objects.all()
    serializer_class = DefiniteArrivalBookingSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        student = Student.objects.get(arrival_booking=instance)
        full_name = student.user.user_info.full_name
        sex = student.user.user_info.sex
        citizenship = student.citizenship
        contacts = student.user.user_info.contacts
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['full_name'] = full_name
        data['sex'] = sex
        data['citizenship'] = citizenship
        data['vk'] = contacts.vk
        data['phone'] = contacts.phone
        data['telegram'] = contacts.telegram
        data['whatsapp'] = contacts.whatsapp


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