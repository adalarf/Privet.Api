from rest_framework import serializers
from .models import User, UserInfo, Contacts, Student, Buddy, ArrivalBooking,\
    BuddyArrival, StudentOnlyViewFields, OtherLanguagesAndLevels, Ticket


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('vk', 'phone', 'telegram', 'whatsapp',)

class OtherLanguagesAndLevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherLanguagesAndLevels
        fields = ('language', 'level')

class UserInfoSerializer(serializers.ModelSerializer):
    contacts = ContactsSerializer()
    other_languages_and_levels = OtherLanguagesAndLevelsSerializer(many=True, required=False)
    class Meta:
        model = UserInfo
        fields = ('full_name', 'birth_date', 'native_language', 'other_languages_and_levels', 'contacts',)

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts', None)
        other_languages_data = validated_data.pop('other_languages_and_levels', None)
        contacts = Contacts.objects.create(**contacts_data)

        user_info = UserInfo.objects.create(contacts=contacts, **validated_data)
        if other_languages_data:
            for language_data in other_languages_data:
                language = OtherLanguagesAndLevels.objects.create(**language_data)
                user_info.other_languages_and_levels.add(language)

        return user_info

    def update(self, instance, validated_data):
        contacts_data = validated_data.pop('contacts', None)
        other_languages_data = validated_data.pop('other_languages_and_levels', None)

        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.native_language = validated_data.get('native_language', instance.native_language)

        if contacts_data:
            contacts_serializer = ContactsSerializer(instance.contacts, data=contacts_data)
            if contacts_serializer.is_valid():
                contacts_serializer.save()

        if other_languages_data:
            instance.other_languages_and_levels.clear()  # Удалить все связи с другими языками и уровнями
            for language_data in other_languages_data:
                language_id = language_data.get('id')
                if language_id:
                    language_instance = OtherLanguagesAndLevels.objects.get(id=language_id)
                    language_serializer = OtherLanguagesAndLevelsSerializer(language_instance, data=language_data)
                else:
                    language_serializer = OtherLanguagesAndLevelsSerializer(data=language_data)
                if language_serializer.is_valid():
                    language = language_serializer.save()
                    instance.other_languages_and_levels.add(language)

        instance.save()
        return instance




class UserSerializer(serializers.ModelSerializer):
    user_info = UserInfoSerializer()
    class Meta:
        model = User
        fields = ('email', 'university', 'user_info',)
        extra_kwargs = {
            'email': {'validators': []},
        }

    def update(self, instance, validated_data):
        user_info_data = validated_data.pop('user_info')
        user_info_serializer = UserInfoSerializer(instance=instance.user_info, data=user_info_data)
        if user_info_serializer.is_valid():
            user_info_instance = user_info_serializer.save()
            instance.email = validated_data.get('email', instance.email)
            instance.university = validated_data.get('university', instance.university)
            instance.user_info = user_info_instance
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(user_info_serializer.errors)



class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = ('citizenship', 'sex', 'user',)

    def update(self, instance, validated_data):
        user_info_data = validated_data.pop('user')
        user_info_serializer = UserSerializer(instance=instance.user, data=user_info_data)
        if user_info_serializer.is_valid():
            user_info_instance = user_info_serializer.save()
            instance.citizenship = validated_data.get('citizenship', instance.citizenship)
            instance.sex = validated_data.get('sex', instance.sex)
            instance.user_info = user_info_instance
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(user_info_serializer.errors)


class OnlyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOnlyViewFields
        exclude = ('id', )

class StudentOnlyViewFieldsSerializer(serializers.ModelSerializer):
    only_view = OnlyViewSerializer()
    class Meta:
        model = Student
        fields = ('only_view',)


    def update(self, instance, validated_data):
        only_view_data = validated_data.pop('only_view')
        only_view_instance = instance.only_view

        if not only_view_instance:
            only_view_instance = StudentOnlyViewFields.objects.create()
            instance.only_view = only_view_instance
            instance.save()

        only_view_instance.institute = only_view_data.get('institute', only_view_instance.institute)
        only_view_instance.study_program = only_view_data.get('study_program', only_view_instance.study_program)

        # if 'last_arrival_date' not in only_view_data:
        #     student = Student.objects.get(only_view=instance.only_view)
        #     last_arrival = student.arrival_booking.arrival_date
        #     only_view_instance.last_arrival_date = last_arrival
        # else:
        #     only_view_instance.last_arrival_date = only_view_data.get('last_arrival_date', only_view_instance.last_arrival_date)

        only_view_instance.last_visa_expiration = only_view_data.get('last_visa_expiration', only_view_instance.last_visa_expiration)
        only_view_instance.accommodation = only_view_data.get('accommodation', only_view_instance.accommodation)
        only_view_instance.buddys_comment = only_view_data.get('buddys_comment', only_view_instance.buddys_comment)
        only_view_instance.save()

        return instance

    # def update(self, instance, validated_data):
    #     only_view_data = validated_data.pop('only_view')
    #     only_view_instance = instance.only_view
    #     if not instance.only_view:
    #         instance.only_view = StudentOnlyViewFields.objects.create()
    #
    #     only_view_instance.institute = only_view_data.get('institute', only_view_instance.institute)
    #     only_view_instance.study_program = only_view_data.get('study_program', only_view_instance.study_program)
    #     if 'last_arrival_date' not in only_view_data:
    #         student = Student.objects.get(only_view=instance.only_view)
    #         last_arrival = student.arrival_booking.arrival_date
    #         only_view_instance.last_arrival_date = last_arrival
    #     else:
    #         only_view_instance.last_arrival_date = only_view_data.get('last_arrival_date', only_view_instance.last_arrival_date)
    #     # only_view_instance.last_visa_expiration = only_view_data.get('last_visa_expiration',
    #                                                                  #only_view_instance.last_visa_expiration)
    #     only_view_instance.accommodation = only_view_data.get('accommodation', only_view_instance.accommodation)
    #     only_view_instance.buddys_comment = only_view_data.get('buddys_comment', only_view_instance.buddys_comment)
    #     only_view_instance.save()
    #
    #     return instance

    # def update(self, instance, validated_data):
    #     only_view_data = validated_data.pop('only_view')
    #     only_view_instance = instance.only_view
    #
    #     only_view_instance.institute = only_view_data.get('institute', only_view_instance.institute)
    #     only_view_instance.study_program = only_view_data.get('study_program', only_view_instance.study_program)
    #     only_view_instance.last_visa_expiration = only_view_data.get('last_visa_expiration',
    #                                                                  only_view_instance.last_visa_expiration)
    #     only_view_instance.accommodation = only_view_data.get('accommodation', only_view_instance.accommodation)
    #     only_view_instance.buddys_comment = only_view_data.get('buddys_comment', only_view_instance.buddys_comment)
    #     only_view_instance.save()
    #
    #     return instance

class ArrivalBookingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrivalBooking
        fields = ('id', 'arrival_date', 'arrival_time', 'arrival_point',)

class ArrivalOtherStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrivalBooking
        fields = ('other_students',)


class UserInfoOtherStudentSerializer(serializers.ModelSerializer):
    contacts = ContactsSerializer()
    class Meta:
        model = UserInfo
        fields = ('full_name', 'contacts',)


    def update(self, instance, validated_data):
        contacts_data = validated_data.pop('contacts')
        contacts_serializer = ContactsSerializer(instance=instance.contacts, data=contacts_data)
        if contacts_serializer.is_valid():
            contacts_instance = contacts_serializer.save()
            instance.full_name = validated_data.get('full_name', instance.full_name)
            instance.contacts = contacts_instance
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(contacts_serializer.errors)



class UserOtherStudentSerializer(serializers.ModelSerializer):
    user_info = UserInfoOtherStudentSerializer()
    class Meta:
        model = User
        fields = ('user_info',)

    def update(self, instance, validated_data):
        user_info_data = validated_data.pop('user_info', {})
        user_info_instance = instance.user_info
        user_info_serializer = UserInfoOtherStudentSerializer(user_info_instance, data=user_info_data)
        if user_info_serializer.is_valid():
            user_info_serializer.save()
        instance.save()
        return instance


class OtherStudentsArrivalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = ('pk', 'citizenship', 'sex', 'user')


class DefiniteArrivalBookingSerializer(serializers.ModelSerializer):
    students = OtherStudentsArrivalSerializer(many=True, source='other_students')
    class Meta:
        model = ArrivalBooking
        exclude = ('other_students',)

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('file',)


class ArrivalBookingSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, required=False)
    class Meta:
        model = ArrivalBooking
        exclude = ('other_students',)

class UserInfoArrivalSerializer(serializers.ModelSerializer):
    contacts = ContactsSerializer()
    class Meta:
        model = UserInfo
        fields = ('full_name', 'sex', 'contacts',)

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        user_info = Contacts.objects.create(**contacts_data)
        res = UserInfo.objects.create(contacts=user_info, **validated_data)
        return res

    def update(self, instance, validated_data):
        contacts_data = validated_data.pop('contacts')
        contacts_serializer = ContactsSerializer(instance=instance.contacts, data=contacts_data)
        if contacts_serializer.is_valid():
            contacts_instance = contacts_serializer.save()
            instance.full_name = validated_data.get('full_name', instance.full_name)
            instance.sex = validated_data.get('sex', instance.sex)
            instance.contacts = contacts_instance
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(contacts_serializer.errors)


class StudentArrivalBookingSerializer(serializers.ModelSerializer):
    user = UserOtherStudentSerializer()
    arrival_booking = ArrivalBookingSerializer()
    class Meta:
        model = Student
        fields = ('citizenship', 'sex', 'user', 'arrival_booking',)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        arrival_booking_data = validated_data.pop('arrival_booking', None)
        instance.citizenship = validated_data.get('citizenship', instance.citizenship)
        instance.sex = validated_data.get('sex', instance.sex)

        user_instance = instance.user
        user_serializer = UserOtherStudentSerializer(user_instance, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()


        if arrival_booking_data:
            arrival_booking_instance = instance.arrival_booking
            if arrival_booking_instance:
                arrival_booking_serializer = ArrivalBookingSerializer(arrival_booking_instance,
                                                                      data=arrival_booking_data)
            else:
                arrival_booking_serializer = ArrivalBookingSerializer(data=arrival_booking_data)
            if arrival_booking_serializer.is_valid():
                arrival_booking = arrival_booking_serializer.save()
                instance.arrival_booking = arrival_booking

        instance.save()
        return instance



class StudentArrivalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    arrival_booking = ArrivalBookingSerializer()
    class Meta:
        model = Student
        fields = ('citizenship', 'user', 'arrival_booking')


class BuddyArrivalSerializer(serializers.ModelSerializer):
    student = StudentArrivalSerializer()
    class Meta:
        model = BuddyArrival
        fields = ('student', )

class StudentForBuddySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        exclude = ('confirmation_code', 'arrival_booking', 'only_view')


class ArrivalBookingForBuddySerializer(serializers.ModelSerializer):
    #other_students = StudentForBuddySerializer(many=True)
    class Meta:
        model = ArrivalBooking
        fields = ('id', 'arrival_date', 'arrival_time', 'arrival_point',)


class StudentArrivalForBuddySerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    arrival_booking = ArrivalBookingForBuddySerializer()
    class Meta:
        model = Student
        fields = ('arrival_booking',)


class BuddyArrivalForBuddySerializer(serializers.ModelSerializer):
    student = StudentArrivalForBuddySerializer()
    class Meta:
        model = BuddyArrival
        fields = ('student', )



class BuddyArrivalsSerializer(serializers.ModelSerializer):
    buddy_arrivals = BuddyArrivalForBuddySerializer(many=True)
    class Meta:
        model = Buddy
        fields = ('buddy_arrivals',)




class BuddyStudentOtherInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('full_name',)

class BuddyStudentUserSerialzier(serializers.ModelSerializer):
    user_info = BuddyStudentOtherInfoSerializer()
    class Meta:
        model = User
        fields = ('id', 'user_info',)

class BuddyOtherStudentsSerializer(serializers.ModelSerializer):
    user = BuddyStudentUserSerialzier()
    class Meta:
        model = Student
        fields = ('user', 'citizenship')

class BuddyStudentArrivalBookingSerializer(serializers.ModelSerializer):
    other_students = BuddyOtherStudentsSerializer(many=True)
    class Meta:
        model = ArrivalBooking
        fields = ('other_students', )

class BuddyStudentArrivalSerializer(serializers.ModelSerializer):
    user = BuddyStudentUserSerialzier()
    arrival_booking = BuddyStudentArrivalBookingSerializer()
    class Meta:
        model = Student
        fields = ('user', 'citizenship', 'arrival_booking',)

class BuddyStudentsArrivalsSerializer(serializers.ModelSerializer):
    student = BuddyStudentArrivalSerializer()
    class Meta:
        model = BuddyArrival
        fields = ('id', 'student',)


class BuddyStudentsSerializer(serializers.ModelSerializer):
    buddy_arrivals = BuddyStudentsArrivalsSerializer(many=True)
    class Meta:
        model = Buddy
        fields = ('buddy_arrivals',)



class AddBuddyToArrivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuddyArrival
        fields = '__all__'


class UserInfoForAllBuddysSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('full_name',)

class UserForAllBuddysSerializer(serializers.ModelSerializer):
    user_info = UserInfoForAllBuddysSerializer()
    class Meta:
        model = User
        fields = ('id', 'user_info',)

class AllBuddysSerializer(serializers.ModelSerializer):
    user = UserForAllBuddysSerializer()
    class Meta:
        model = Buddy
        fields = ('user',)



class BuddySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Buddy
        fields = ('city', 'user',)

    def update(self, instance, validated_data):
        user_info_data = validated_data.pop('user')
        instance.city = validated_data.get('city', instance.city)
        user_info_serializer = UserSerializer(instance=instance.user, data=user_info_data)
        if user_info_serializer.is_valid():
            user_info_instance = user_info_serializer.save()
            instance.user_info = user_info_instance
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(user_info_serializer.errors)





class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('university', 'email', 'password', 'is_buddy',)


class StudentSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('university', 'email', 'password',)


    def save(self, **kwargs):
        user = User(
            university=self.validated_data['university'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.is_student = True
        user.save()
        Student.objects.create(user=user)
        return user

class BuddySignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('university', 'email', 'password',)


    def save(self, **kwargs):
        user = User(
            university=self.validated_data['university'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.is_buddy = True
        user.save()
        Buddy.objects.create(user=user)
        return user
