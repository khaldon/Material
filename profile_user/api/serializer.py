from profile_user.models import Profile
from rest_framework import serializers


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True,)

    class Meta:
        model = Profile
        fields = ('pk', 'profile', 'birth_date', 'image')




