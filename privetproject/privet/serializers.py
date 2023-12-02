from rest_framework import serializers
from .models import User, UserInfo, Contacts, Student, Buddy


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('vk', 'phone', 'telegram', 'whatsapp',)

class UserInfoSerializer(serializers.ModelSerializer):
    contacts = ContactsSerializer()
    class Meta:
        model = UserInfo
        fields = ('full_name', 'sex', 'birth_date', 'native_language', 'other_languages_and_levels', 'contacts',)

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
            instance.birth_date = validated_data.get('birth_date', instance.birth_date)
            instance.native_language = validated_data.get('native_language', instance.native_language)
            instance.other_languages_and_levels = validated_data.get('other_languages_and_levels', instance.other_languages_and_levels)
            instance.contacts = contacts_instance
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(contacts_serializer.errors)




class UserSerializer(serializers.ModelSerializer):
    user_info = UserInfoSerializer()
    class Meta:
        model = User
        fields = ('email', 'user_info',)
        extra_kwargs = {
            'email': {'validators': []},
        }

    def update(self, instance, validated_data):
        user_info_data = validated_data.pop('user_info')
        user_info_serializer = UserInfoSerializer(instance=instance.user_info, data=user_info_data)
        if user_info_serializer.is_valid():
            user_info_instance = user_info_serializer.save()
            instance.email = validated_data.get('email', instance.email)
            instance.user_info = user_info_instance
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(user_info_serializer.errors)



class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = ('citizenship', 'user',)

    def update(self, instance, validated_data):
        user_info_data = validated_data.pop('user')
        user_info_serializer = UserSerializer(instance=instance.user, data=user_info_data)
        if user_info_serializer.is_valid():
            user_info_instance = user_info_serializer.save()
            instance.citizenship = validated_data.get('citizenship', instance.buddy_status)
            instance.user_info = user_info_instance
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(user_info_serializer.errors)


class BuddySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Buddy
        fields = ('buddy_status', 'user',)

    def update(self, instance, validated_data):
        user_info_data = validated_data.pop('user')
        user_info_serializer = UserSerializer(instance=instance.user, data=user_info_data)
        if user_info_serializer.is_valid():
            user_info_instance = user_info_serializer.save()
            instance.buddy_status = validated_data.get('buddy_status', instance.buddy_status)
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
