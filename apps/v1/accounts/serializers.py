from dataclasses import fields
import profile
from urllib import request
from rest_framework import serializers
from common.serializers import Base64ImageField
from apps.v1.accounts.models import User, UserProfile
from drf_writable_nested.serializers import WritableNestedModelSerializer

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from apps.v1.accounts.models import User

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class ProfileSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(max_length=None,use_url = True,)
    class Meta:
        model = UserProfile
        fields = "address","phone","profile_image"


class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ("pk","username","email","first_name","last_name","password","role","profile")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        raw_password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(raw_password)
        user.save()

        UserProfile.objects.create(**profile_data,user=user)
        return user

class UpdateUserSerializer(WritableNestedModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model= User
        fields =('first_name','last_name','profile')
    
    def Update(self,instance,validate_data):
        profile = instance.profile
        profile_data = validate_data.pop('profile')
        profile.phone = profile_data.pop('phone',profile.phone)
        profile.address = profile_data('address',profile.address)
        profile.profile_image = profile_data('profile_image',profile.profile_image)
        profile.save()

        instance.first_name = validate_data.get('first_name',instance.first_name)
        instance.last_name = validate_data.get('last_name',instance.last_name)
        instance.save()

        return instance
class UpdateMyProfileSerializer(WritableNestedModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('first_name','last_name','profile')
    
    def update(self, instance, validated_data):
        profile = instance.profile
        profile_data = validated_data.pop('profile')
        profile.phone = profile_data.pop('phone',profile.phone)
        profile.address = profile_data.pop('address',profile.address)
        profile.profile_image = profile_data.pop('profile_image',profile.profile_image)
        profile.save()

        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.ModelSerializer):
    confirm_password =serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    old_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [ 'old_password', 'new_password','confirm_password']



    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)

        if not validated_data['new_password']:
              raise serializers.ValidationError({'new_password': 'not found'})

        if not validated_data['old_password']:
              raise serializers.ValidationError({'old_password': 'not found'})

        if not instance.check_password(validated_data['old_password']):
              raise serializers.ValidationError({'old_password': 'wrong password'})

        if validated_data['new_password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({'passwords': 'passwords do not match'})

        if validated_data['new_password'] == validated_data['confirm_password'] and instance.check_password(validated_data['old_password']):
            # instance.password = validated_data['new_password'] 
            instance.set_password(validated_data['new_password'])
            instance.save()
            return instance
        return instance

class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exists'
            )
        return {
            'username':user.username,
            'token': jwt_token
        }