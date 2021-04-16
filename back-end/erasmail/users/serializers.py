from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'nickname', 'connected_count']

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_unusable_password()
        user.save()
        return user

# class SuccessSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Success
#         exclude = ["user"]
