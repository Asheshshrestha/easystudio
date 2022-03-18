from ast import mod
from urllib import request
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from apps.v1.accounts.models import User
from apps.v1.studio.models import StudioProfile
from rest_framework.response import Response
from apps.v1.studio.serializers import StudioRegistrationSerializer,UpdateSudioProfileSerializer
from common.permissions import IsAdmin, IsAdminOrStudio
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class StudioRegistrationView(generics.CreateAPIView):

    serializer_class = StudioRegistrationSerializer
    permission_classes = (IsAdmin,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Studio registered  successfully',
            }
        
        return Response(response, status=status_code)


    
class StudioProfileView(generics.RetrieveAPIView):

    permission_classes = (permissions.IsAuthenticated,IsAdminOrStudio,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            studio_profile = StudioProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'Studio profile fetched successfully',
                'data': [{
                    'first_name': request.user.first_name,
                    'last_name':  request.user.last_name,
                    'phone_number': studio_profile.phone,
                    'address': studio_profile.address,
                    'profile_image': studio_profile.get_profile_image,
                    'studio_name':studio_profile.studio_name,
                    'longitude':studio_profile.longitude,
                    'latitude':studio_profile.latitude,
                    'marker_icon':studio_profile.get_marker_icon,
                    'cover_image':studio_profile.get_cover_image
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'Studio does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)


class UpdateStudioProfile(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsAdminOrStudio,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UpdateSudioProfileSerializer
    queryset= User.objects.all()
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj
    def get(self,request):
        try:
            studio_profile = StudioProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': request.user.first_name,
                    'last_name':  request.user.last_name,
                    'phone_number': studio_profile.phone,
                    'address': studio_profile.address,
                    'profile_image': studio_profile.get_profile_image,
                    'studio_name':studio_profile.studio_name,
                    'longitude':studio_profile.longitude,
                    'latitude':studio_profile.latitude,
                    'marker_icon':studio_profile.get_marker_icon,
                    'cover_image':studio_profile.get_cover_image
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