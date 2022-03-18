from ast import mod
from urllib import request
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from apps.v1.accounts.models import User
from apps.v1.accounts.models import UserProfile
from rest_framework.response import Response
from apps.v1.accounts.serializers import (UserLoginSerializer,
                                            UserRegistrationSerializer,
                                            UpdateUserSerializer,
                                            ChangePasswordSerializer,
                                            UpdateMyProfileSerializer)
from django.forms.models import model_to_dict
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from common.permissions import IsAdminOrStudio

# Create your views here.
###############################################################################################################
#========================User Account View Start===============================================================
class UserRegistrationView(generics.CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        
        return Response(response, status=status_code)

class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    
class ChangePasswordView(generics.RetrieveUpdateAPIView):
    queryset= User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

class UserLoginView(generics.RetrieveAPIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            'pk': User.objects.get(username=serializer.data['username']).pk
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

class UpdateMyProfile(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UpdateMyProfileSerializer
    queryset= User.objects.all()
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj
    def get(self,request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': request.user.first_name,
                    'last_name':  request.user.last_name,
                    'phone_number': user_profile.phone,
                    'address': user_profile.address,
                    'profile_image': user_profile.profile_image.url,
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)

    
class UserProfileView(generics.RetrieveAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': request.user.first_name,
                    'last_name':  request.user.last_name,
                    'phone_number': user_profile.phone,
                    'address': user_profile.address,
                    'profile_image': user_profile.profile_image.url,
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)

#========================User Account View End=================================================================
###############################################################################################################

class StudioProfileView(generics.RetrieveAPIView):

    permission_classes = (IsAdminOrStudio,)
    authentication_class = JSONWebTokenAuthentication

    
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': request.user.first_name,
                    'last_name':  request.user.last_name,
                    'phone_number': user_profile.phone,
                    'address': user_profile.address,
                    'profile_image': user_profile.profile_image.url,
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)