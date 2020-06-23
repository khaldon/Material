from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.conf import settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()

class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer that represents a user login process.
    """

    token = serializers.CharField(allow_blank=True, read_only=True)
    email = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'email', 'password', 'token'

        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        """
        Validates user data & returns token in case provided credentials are correct.
        :params data: dict
        :return: dict
        """
        email = data['email']
        password = data['password']
        user_qs = User.objects.filter(
            Q(email__iexact=email)
        ).distinct()
        if user_qs.exists() and user_qs.count() == 1:
            user_obj = user_qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                data['token'] = token
            else:
                raise serializers.ValidationError("Incorrect password.")
        else:
            raise serializers.ValidationError("The user with this username does not exists.")
        return data


class UserSerializerWithToken(serializers.ModelSerializer):
    """
    Serializer that represents a user registration.
    """

    token = serializers.SerializerMethodField()
    password = serializers.CharField(required=True,write_only=True)
    password_2 = serializers.CharField(required=True,write_only=True)

    class Meta:
        model = User
        fields = [
            'token', 'username', 'email', 'password', 'password_2'
        ]


    def get_token(self, obj):
        """
        Generates JWT.
        :return: string
        """
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError(
            "Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
            )
        return value

    def validate_password_2(self, value):
        data = self.get_initial()
        password = data.get('password')
        if password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def create(self, validated_data):
        """
        Handles the creation of user.
        :params validated_data: dict
        :return: string
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance