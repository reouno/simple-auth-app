from rest_framework import serializers

from api_server.apps.custom_accounts.models import CustomUser


class MessageSerializer(serializers.Serializer):
    """Message serializer"""
    message = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        """Meta"""
        model = CustomUser
        exclude = ['password']


class NativeLoginSerializer(serializers.Serializer):
    """Login serializer"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        """No need to implement"""
        raise NotImplementedError()

    def update(self, instance, validated_data):
        """No need to implement"""
        raise NotImplementedError()
