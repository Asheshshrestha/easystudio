from urllib import response
from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from common.permissions import IsAdminOrStudio
from apps.v1.services.serializers import (ServiceRequestSerializer, 
                                            ServiceTypeSerializer,
                                            ActiveDeactiveServiceTypeSerializer,
                                            ReceivedServiceRequestSerializer,
                                            PrintedServiceRequestSerializer,
                                            CancelServiceRequestSerializer)
from apps.v1.services.models import ServiceRequestModel,ServiceTypeModel
from apps.v1.accounts.models import User
from django.shortcuts import get_object_or_404

# Create your views here.


class CreateServiceTypeAPIView(generics.CreateAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ServiceTypeSerializer
    permission_classes = (IsAdminOrStudio,)

class ServiceTypeDetailAPIView(generics.RetrieveAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ServiceTypeSerializer
    queryset = ServiceTypeModel.objects.all()
    permission_classes= [permissions.IsAuthenticated]

class UpdateServiceTypeAPIView(generics.UpdateAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ServiceTypeSerializer
    permission_classes = (IsAdminOrStudio,)
    queryset = ServiceTypeModel.objects.all()

class ActiveInactiveServiceTypeAPIView(generics.UpdateAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ActiveDeactiveServiceTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ServiceTypeModel.objects.all()

class DestroyServiceTypeAPIView(generics.DestroyAPIView):
    authentication_class = JSONWebTokenAuthentication
    queryset = ServiceTypeModel.objects.all()
    permission_classes= [IsAdminOrStudio]

class StudioServiceTypeListAPIView(generics.ListAPIView):
    serializer_class = ServiceTypeSerializer
    queryset = ServiceTypeModel.objects.all()
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            pk = self.kwargs['pk']
            user = get_object_or_404(User,pk=pk)
            queryset = ServiceTypeModel.objects.filter(studio=user)
            return queryset
        except Exception as e:
            return []



class RequestServiceAPIView(generics.CreateAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ServiceRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

class RequestServiceDetailAPIView(generics.RetrieveAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ServiceRequestSerializer
    queryset = ServiceRequestModel.objects.all()
    permission_classes= [permissions.IsAuthenticated]

class UpdateRequestServiceAPIView(generics.UpdateAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ServiceRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ServiceRequestModel.objects.all()

class DestroyRequestServiceAPIView(generics.DestroyAPIView):
    authentication_class = JSONWebTokenAuthentication
    queryset = ServiceRequestModel.objects.all()
    permission_classes= [permissions.IsAuthenticated]

class ReceivedServiceRequestAPIView(generics.UpdateAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ReceivedServiceRequestSerializer
    permission_classes = (IsAdminOrStudio,)
    queryset = ServiceRequestModel.objects.all()


class PrintedServiceRequestAPIView(generics.UpdateAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = PrintedServiceRequestSerializer
    permission_classes = (IsAdminOrStudio,)
    queryset = ServiceRequestModel.objects.all()

class CancelServiceRequestAPIView(generics.UpdateAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = CancelServiceRequestSerializer
    permission_classes = (IsAdminOrStudio,)
    queryset = ServiceRequestModel.objects.all()


class DestroyServiceRequestAPIView(generics.DestroyAPIView):
    authentication_class = JSONWebTokenAuthentication
    queryset = ServiceRequestModel.objects.all()
    permission_classes= [permissions.IsAuthenticated,]

class MyServiceRequestUserAPIView(generics.ListAPIView):
    serializer_class = ServiceRequestSerializer
    queryset = ServiceRequestModel.objects.all()
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = ServiceRequestModel.objects.filter(request_user = self.request.user)
        return queryset

class MyServiceRequestStudioAPIView(generics.ListAPIView):
    serializer_class = ServiceRequestSerializer
    queryset = ServiceRequestModel.objects.all()
    permission_classes= [IsAdminOrStudio]

    def get_queryset(self):
        queryset = ServiceRequestModel.objects.filter(studio = self.request.user)
        return queryset