from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from profile_user.models import ProfileUser
from .serializer import ProfileUserSerializer


class ProfileUserList(generics.ListCreateAPIView):
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileUserSerializer
    name = 'Profile user list'


class ProfileUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileUserSerializer
    name = 'Profile user detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'profile': reverse(ProfileUserList.name, request=request),
        })
