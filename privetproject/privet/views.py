from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView,\
    ListAPIView, RetrieveAPIView
from .models import User, UserInfo
from .serializers import StudentSerializer, BuddySerializer, StudentSignupSerializer,\
    BuddySignupSerializer, BaseUserSerializer, StudentArrivalBookingSerializer,\
    ArrivalBookingSerializer, BuddyArrivalsSerializer, ArrivalOtherStudentSerializer, \
    ArrivalBookingInfoSerializer, DefiniteArrivalBookingSerializer, StudentOnlyViewFieldsSerializer,\
    BuddyStudentsSerializer, AddBuddyToArrivalSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Student, Buddy, ArrivalBooking, BuddyArrival, PassCode
from .permissions import IsStudentUser, IsBuddyUser, IsConfirmedBuddyUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from .authtoken import ObtainAuthToken
import secrets
from django.core.mail import send_mail
from django.conf import settings


class StudentProfileView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated&IsStudentUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['profile_type'] = 'student'

        student = Student.objects.get(pk=instance)
        if BuddyArrival.objects.filter(student=student):
            buddy = Buddy.objects.filter(buddy_arrivals__student=student).last()
            data['last_buddy'] = buddy.user.user_info.full_name
            data['last_arrival_date'] = student.arrival_booking.arrival_date
        elif BuddyArrival.objects.filter(student__arrival_booking__other_students=student):
            buddy = Buddy.objects.filter(buddy_arrivals__student__arrival_booking__other_students=student).last()
            data['last_buddy'] = buddy.user.user_info.full_name
            arrival_booking = ArrivalBooking.objects.filter(other_students=student).first()
            data['last_arrival_date'] = arrival_booking.arrival_date
        else:
            data['last_buddy'] = ''
            data['last_arrival_date'] = ''

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
    permission_classes = [IsAuthenticated&IsBuddyUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        buddy = Buddy.objects.get(pk=instance)
        if buddy.user.is_teamlead == True:
            data['profile_type'] = 'teamlead'
        else:
            data['profile_type'] = 'buddy'

        data['buddy_status'] = buddy.buddy_status

        return Response(data)

class StudentProfileForBuddyView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentOnlyViewFieldsSerializer
    permission_classes = [IsAuthenticated, IsConfirmedBuddyUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        student = Student.objects.get(pk=instance)
        data['citizenship'] = student.citizenship
        data['sex'] = student.sex
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
            'birth_date': user_info.birth_date,
            'native_language': user_info.native_language,
            'other_languages_and_levels': [i.other_language_and_level for i in user_info.other_languages_and_levels.all()],
            'contacts': contacts,
        }

        user_data = {
            'email': user.email,
            'user_info': user_info,
        }
        data['user'] = user_data

        return Response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        student = Student.objects.get(pk=instance)
        data = serializer.data
        data['citizenship'] = student.citizenship
        data['sex'] = student.sex
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
            'birth_date': user_info.birth_date,
            'native_language': user_info.native_language,
            'other_languages_and_levels': [i.other_language_and_level for i in user_info.other_languages_and_levels.all()],
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        student = Student.objects.get(pk=instance)
        other_students = student.arrival_booking.other_students.all()

        data['arrival_booking']['other_students'] = [i.user.user_info.full_name for i in other_students]

        return Response(data)

class AllArrivalBookingsView(APIView):
    permission_classes = [IsAuthenticated, IsConfirmedBuddyUser]
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
    permission_classes = [IsAuthenticated, IsConfirmedBuddyUser]
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        student = Student.objects.get(arrival_booking=instance)
        buddy = Buddy.objects.filter(buddy_arrivals__student__arrival_booking=instance)
        buddy_full_names = [i.user.user_info.full_name for i in buddy if i.user.user_info]
        buddy_id = [i.pk for i in buddy]
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
        data['buddy_id'] = buddy_id


        return Response(data)

class AddArrivalToBuddy(APIView):
    permission_classes = [IsAuthenticated, IsConfirmedBuddyUser]
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
    permission_classes = [IsAuthenticated, IsConfirmedBuddyUser]
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
    permission_classes = [IsAuthenticated, IsConfirmedBuddyUser]

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
            #buddy.buddy_arrivals.get(student__arrival_booking_id=buddy_arrival_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BuddyArrival.DoesNotExist:
            return Response("Buddy arrival not found", status=status.HTTP_404_NOT_FOUND)


class ConfirmBuddyArrivalView(APIView):
    def post(self, request):
        buddy_id = request.data.get('buddy_id')
        arrival_id = request.data.get('arrival_id')
        buddy = Buddy.objects.get(pk=buddy_id)
        arrival = ArrivalBooking.objects.get(pk=arrival_id)
        buddy_arrival = buddy.buddy_arrivals.get(student__arrival_booking=arrival)
        buddy_arrival.buddy_arrival_status = True
        buddy_arrival.save()
        return Response(f'Сопровождающий {buddy_id} подтвержден')


class ConfirmBuddyView(APIView):
    def post(self, request):
        buddy_id = request.data.get('buddy_id')
        buddy = Buddy.objects.get(pk=buddy_id)
        buddy.buddy_status = True
        buddy.save()
        return Response(f"Buddy with {buddy_id} id is confirmed", status=status.HTTP_201_CREATED)





class StudentSignupView(GenericAPIView):
    serializer_class = StudentSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        student = Student.objects.get(user=user)
        student.send_confirmation_email()

        return Response({"message": "Код подтверждения отправлен на вашу почту.", "id": student.pk}, status=status.HTTP_200_OK)


class StudentConfirmationView(APIView):
    def post(self, request):
        entered_code = request.data.get('code')
        user_id = request.data.get('user_id')

        try:
            student = Student.objects.get(user_id=user_id)
            if student.confirm_registration(entered_code):
                return Response({"message": "Регистрация успешна.", "token": Token.objects.get(user=student.user).key}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Неверный код подтверждения."}, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({"message": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

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


class SendEmailView(GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.get(email=email)
        if user:
            passcode, created = PassCode.objects.get_or_create(user=user, defaults={
                'code': secrets.token_hex(3)})
            if not created:
                passcode.code = secrets.token_hex(3)
                passcode.save()
            subject = 'Сброс пароля'
            message = f'Ваш код подтверждения: {passcode.code}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
        else:
            return Response('Аккаунт не был найден')
        return Response('Код отправлен')


class EmailConfirmationView(APIView):
    def post(self, request):
        code = request.data.get('code')
        passcode = PassCode.objects.get(code=code)
        if passcode:
            passcode.code = ''
            return Response({'response':'Код верен', 'id': passcode.user.id})
        else:
            return Response('Код не верен')

class UpdatePasswordView(APIView):
    def post(self, request):
        password = request.data.get('password')
        user_id = request.data.get('user_id')

        user = User.objects.get(id=user_id)
        if user:
            user.set_password(password)
            user.save()
            return Response('Пароль изменён')



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