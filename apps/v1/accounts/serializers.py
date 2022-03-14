import profile
from rest_framework import serializers
from common.serializers import Base64ImageField
from apps.v1.accounts.models import User, UserProfile

class ProfileSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(max_length=None,use_url = True,)
    class Meta:
        model = UserProfile
        fields = "address","phone","profile_image"

class CreateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ("pk","username","email","first_name","last_name","password","role","profile")
        extra_kwargs = {"password":{"write_only":True}}
    def create(self,validate_data):
        profile_data = validate_data.pop("profile")
        raw_password = validate_data.pop("password")
        user = User(**validate_data)
        user.set_password(raw_password)
        user.save()

        UserProfile.objects.create(**profile_data,user=user)
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer
    class Meta:
        model= User
        exclude = ('username','email')
    
    def Update(self,instance,validate_data):
        profile = instance.profile
        profile_data = validate_data.pop('profile')
        profile.dob = profile_data.pop('dob',profile.dob)
        profile.address = profile_data('address')
        profile.save()

        instance.first_name = validate_data.get('first_name',instance.first_name)
        instance.last_name = validate_data.get('last_name',instance.last_name)
        instance.role = validate_data.get('role')
        if validate_data.get('password'):
            instance.set_password(validate_data.get('password'))
        instance.save()

        return instance