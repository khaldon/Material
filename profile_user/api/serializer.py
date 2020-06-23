from profile_user.models import  ProfileUser
from rest_framework import serializers


class ProfileUserSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='profile-user')

    class Meta:
        model = ProfileUser
        fields = ('url', 'pk', 'profile', 'birth_date', 'image')




