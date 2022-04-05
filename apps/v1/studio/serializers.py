from dataclasses import fields
import profile
from urllib import request
from rest_framework import serializers
from common.serializers import Base64ImageField
from apps.v1.accounts.models import User
from apps.v1.studio.models import StudioProfile,StudioRating
from drf_writable_nested.serializers import WritableNestedModelSerializer

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from apps.v1.accounts.models import User
from rest_framework import status
from django.db.models import Q

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class StudioProfileSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(max_length=None,use_url = True,)
    class Meta:
        model = StudioProfile
        fields = "address","phone","profile_image","studio_name","longitude","latitude","marker_icon","cover_image"


class StudioRegistrationSerializer(serializers.ModelSerializer):

    profile = StudioProfileSerializer(required=False)

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

        StudioProfile.objects.create(**profile_data,user=user)
        return user

class UpdateSudioProfileSerializer(WritableNestedModelSerializer):
    studio_profile = StudioProfileSerializer()
    class Meta:
        model = User
        fields = ('first_name','last_name','studio_profile')
    
    def update(self, instance, validated_data):
        profile = instance.studio_profile
        profile_data = validated_data.pop('studio_profile')
        profile.phone = profile_data.pop('phone',profile.phone)
        profile.address = profile_data.pop('address',profile.address)
        profile.profile_image = profile_data.pop('profile_image',profile.profile_image)
        profile.studio_name = profile_data.pop('studio_name',profile.studio_name)
        profile.longitude = profile_data.pop('longitude',profile.longitude)
        profile.latitude = profile_data.pop('latitude',profile.latitude)
        profile.marker_icon = profile_data.pop('marker_icon',profile.marker_icon)
        profile.cover_image = profile_data.pop('cover_image',profile.cover_image)
        profile.save()

        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.save()
        return instance



class StudioListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    def get_average_rating(self,obj):
        return obj.average_rating['stars__avg']
    class Meta:
        model = StudioProfile
        fields = ("address","average_rating","user","phone","profile_image","studio_name","longitude","latitude","marker_icon","cover_image")

class StudioRatingSerializer(serializers.ModelSerializer):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        context = kwargs.get('context')
        if context:
            self.request = context.get('request')
    class Meta:
        model = StudioRating
        fields = ("pk","stars","studio","rated_user")

    def create(self, validated_data):
        rating = StudioRating.objects.filter(Q(studio = validated_data.get('studio')) & Q(rated_user = self.request.user)).first()
        if rating is None:
            rating = StudioRating(**validated_data)
            rating.rated_user = self.request.user
            rating.studio = validated_data.pop('studio')
            rating.save()
        else:
            rating.stars = validated_data.pop('stars')
            rating.save()
        return rating
