from urllib import response
from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from common.permissions import IsAdminOrStudio
from apps.v1.package.serializers import PackageSerializers,ActiveDeactivePackageSerializer
from apps.v1.package.models import PackageModel
from apps.v1.accounts.models import User
from django.shortcuts import get_object_or_404



class CreatePackageAPIView(generics.CreateAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = PackageSerializers
    permission_classes = (IsAdminOrStudio,)

class PackageDetailAPIView(generics.RetrieveAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = PackageSerializers
    queryset = PackageModel.objects.all()
    permission_classes= [permissions.IsAuthenticated]

class UpdatePackageAPIView(generics.UpdateAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = PackageSerializers
    permission_classes = (IsAdminOrStudio,)
    queryset = PackageModel.objects.all()

class ActiveInactivePackageAPIView(generics.UpdateAPIView):
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ActiveDeactivePackageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PackageModel.objects.all()

class DestroyPackageAPIView(generics.DestroyAPIView):
    authentication_class = JSONWebTokenAuthentication
    queryset = PackageModel.objects.all()
    permission_classes= [IsAdminOrStudio]
    
class ListPackageAPIView(generics.ListAPIView):
    serializer_class = PackageSerializers
    queryset = PackageModel.objects.all()
    permission_classes= [permissions.IsAuthenticated]

class MyStudioPackageAPIView(generics.ListAPIView):
    serializer_class = PackageSerializers
    queryset = PackageModel.objects.all()
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = PackageModel.objects.filter(studio = self.request.user)
        return queryset

class StudioPackageListAPIView(generics.ListAPIView):
    serializer_class = PackageSerializers
    queryset = PackageModel.objects.all()
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            pk = self.kwargs['pk']
            user = get_object_or_404(User,pk=pk)
            queryset = PackageModel.objects.filter(studio=user)
            return queryset
        except Exception as e:
            return []