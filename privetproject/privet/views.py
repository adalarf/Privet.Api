from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView,\
    ListAPIView, RetrieveAPIView
from .models import User, UserInfo
from .serializers import StudentSerializer, BuddySerializer, StudentSignupSerializer,\
    BuddySignupSerializer, BaseUserSerializer, StudentArrivalBookingSerializer,\
    ArrivalBookingSerializer, BuddyArrivalsSerializer, ArrivalOtherStudentSerializer, \
    ArrivalBookingInfoSerializer, DefiniteArrivalBookingSerializer, StudentOnlyViewFieldsSerializer,\
    BuddyStudentsSerializer, AddBuddyToArrivalSerializer
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
    # permission_classes = [IsAuthenticated&IsStudentUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        student = Student.objects.get(pk=instance)

        if student.only_view is None:
            data['institute'] = ''
            data['study_program'] = ''
            data['last_visa_expiration'] = ''
            data['accommodation'] = ''
        else:
            data['institute'] = student.only_view.institute
            data['study_program'] = student.only_view.study_program
            data['last_visa_expiration'] = student.only_view.last_visa_expiration
            data['accommodation'] = student.only_view.accommodation

        return Response(data)


class BuddyProfileView(RetrieveUpdateDestroyAPIView):
    queryset = Buddy.objects.all()
    serializer_class = BuddySerializer
    # permission_classes = [IsAuthenticated&IsBuddyUser]

class StudentProfileForBuddyView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentOnlyViewFieldsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        student = Student.objects.get(pk=instance)
        data['citizenship'] = student.citizenship
        user = student.user
        user_info = user.user_info
        contacts = user_info.contacts
        contacts = {
            'vk': contacts.vk,
            'phone': contacts.phone,
            'telegram': contacts.telegram,
            'whatsapp': contacts.whatsapp,
        }
        user_info = {
            'full_name': user_info.full_name,
            'sex': user_info.sex,
            'birth_date': user_info.birth_date,
            'native_language': user_info.native_language,
            'other_languages_and_levels': user_info.other_languages_and_levels,
            'contacts': contacts,
        }

        user_data = {
            'email': user.email,
            'user_info': user_info,
        }
        data['user'] = user_data

        return Response(data)

class ArrivalBookingView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentArrivalBookingSerializer

class AllArrivalBookingsView(APIView):
    def get(self, request):
        arrival_bookings = ArrivalBooking.objects.all()
        serializer = ArrivalBookingInfoSerializer(arrival_bookings, many=True)
        data = serializer.data
        for i in data:
            student = Student.objects.get(arrival_booking=i['id'])
            buddy_count = Buddy.objects.filter(buddy_arrivals__student__arrival_booking=i['id'])
            buddies_amount = buddy_count.count()
            i['buddies_amount'] = buddies_amount

            other_stud_set = student.arrival_booking.other_students.all()
            other_stud = ''.join([j.user.user_info.full_name for j in other_stud_set])
            other_stud_citizenship = ''.join([j.citizenship for j in other_stud_set])
            if other_stud == '':
                i['group_full_names'] = f"{student.user.user_info.full_name}"
                i['group_countries'] = f"{student.citizenship}"
            else:
                i['group_full_names'] = f"{student.user.user_info.full_name} {other_stud}"
                i['group_countries'] = f"{student.citizenship} {other_stud_citizenship}"

        return Response(data)


class DefiniteArrivalBookingView(RetrieveAPIView):
    queryset = ArrivalBooking.objects.all()
    serializer_class = DefiniteArrivalBookingSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        student = Student.objects.get(arrival_booking=instance)
        buddy = Buddy.objects.filter(buddy_arrivals__student__arrival_booking=instance)
        buddy_full_names = [i.user.user_info.full_name for i in buddy if i.user.user_info]
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
        data['buddy_full_names'] = buddy_full_names


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


class BuddyStudentsView(RetrieveAPIView):
    queryset = Buddy.objects.all()
    serializer_class = BuddyStudentsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        arrivals = data['buddy_arrivals']
        students = []
        for i in range(len(arrivals)):
            arrival = arrivals[i]
            student_info = {
                'arrival_id': arrival['id'],
                'student_full_name': arrival['student']['user']['user_info']['full_name'],
                'citizenship': arrival['student']['citizenship'],
                'student_id': arrival['student']['user']['id']
            }
            students.append(student_info)

            for j in range(len(arrival['student']['arrival_booking']['other_students'])):
                other_student_info = {
                    'arrival_id': arrival['id'],
                    'student_full_name': arrival['student']['arrival_booking']['other_students'][j]['user']['user_info'][
                        'full_name'],
                    'citizenship': arrival['student']['arrival_booking']['other_students'][j]['citizenship'],
                    'student_id': arrival['student']['arrival_booking']['other_students'][j]['user']['id'],
                }
                students.append(other_student_info)

        return Response(students)






class AddBuddyToArrivalView(APIView):
    def post(self, request, *args, **kwargs):
        arrival_booking_id = request.data.get('arrival_booking_id')
        buddy_id = request.data.get('buddy_id')
        buddy = Buddy.objects.get(pk=buddy_id)
        arrival_booking = Student.objects.get(arrival_booking__id=arrival_booking_id)
        buddy_arrivals = buddy.buddy_arrivals
        buddy_arrivals.create(student=arrival_booking)
        buddy.save()
        serializer = AddBuddyToArrivalSerializer(buddy_arrivals, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteBuddyArrivalView(APIView):
    def delete(self, request):
        try:
            buddy_id = request.data.get('buddy_id')
            buddy_arrival_id = request.data.get('buddy_arrival_id')
            buddy = Buddy.objects.get(pk=buddy_id)
            buddy_arrivals = buddy.buddy_arrivals.get(student__arrival_booking_id=buddy_arrival_id)
            buddy_arrivals.delete()
            buddy.buddy_arrivals.get(student__arrival_booking_id=buddy_arrival_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BuddyArrival.DoesNotExist:
            return Response("Buddy arrival not found", status=status.HTTP_404_NOT_FOUND)





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