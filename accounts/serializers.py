from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role',
                 'phone_number', 'address', 'profile_picture', 'bio', 'is_verified',
                 'rating', 'date_joined')
        read_only_fields = ('id', 'username', 'email', 'date_joined')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'address',
                 'profile_picture', 'bio')
        read_only_fields = ('id', 'username', 'email', 'role', 'is_verified',
                           'rating', 'date_joined') 