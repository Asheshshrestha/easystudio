from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from apps.v1.accounts.models import User
from apps.v1.accounts.serializers import CreateUserSerializer,UpdateUserSerializer

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_class = (permissions.AllowAny,)

class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

