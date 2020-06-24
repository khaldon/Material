from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from profile_user.models import Profile
from .serializer import ProfileSerializer


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'Profile user list'


# class ProfileUserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ProfileUser.objects.all()
#     serializer_class = ProfileUserSerializer
#     name = 'Profile-user-detail'
#

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'profile': reverse(ProfileList.name, request=request),
        })
