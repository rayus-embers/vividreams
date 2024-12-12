from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import models
from .models import User, Channel
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
import datetime

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username','password','birth_date']
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        if validated_data['birth_date'] != None:
            birth_date = validated_data['birth_date']
            user = User.objects.create_user(
                username=validated_data['username'],
                birth_date=birth_date,
                email=validated_data['email'],
                password = validated_data['password'],
                )
            return user
        else:
                raise serializers.ValidationError({"birth_date": "You must provide your birth date"})

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class PublicChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'owner',
            'name',
            'profile_picture',
            'instagram',
            'facebook',
            'tiktok',
            'x',
            'youtube'
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'birth_date')
        extra_kwargs = {
            'email': {'required': False},
            'phone_number': {'required': False},
        }
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class CreateChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'owner',
            'name',
            'profile_picture',
            'instagram',
            'facebook',
            'tiktok',
            'x',
            'youtube'
        ]
        extra_kwargs = {
            'owner':{'write_only': True},
        }

    def validate(self, attrs):
        """
        Custom validation if needed
        """
        if not self.instance and "owner" not in attrs:
            raise serializers.ValidationError(
                {"user": "Owner must be provided when creating a Channel."}
            )
        return attrs
    def create(self, validated_data):
        return Channel.objects.create(**validated_data)

    def update(self,instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class ChannelSerializer(serializers.ModelSerializer):
    subscriber_count = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = [
            'owner',
            'name',
            'profile_picture',
            'instagram',
            'facebook',
            'tiktok',
            'x',
            'youtube',
            'subscriber_count',
            'is_subscribed'
        ]
        read_only_fields = ['owner', 'subscriber_count', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        #return obj.subscribers.filter(id=user.id).exists() if user.is_authenticated else False


class ChangePassowrdSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    old_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('old_password', 'password')


    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance