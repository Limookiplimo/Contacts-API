from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=55, min_length=8)
    email = serializers.CharField(max_length=50, min_length=12)
    first_name = serializers.CharField(max_length=30, min_length=2)
    last_name = serializers.CharField(max_length=30, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password':{'write_only': True}} #Do not return password to user
    
    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email', ('Email already exists!')})
        return super().validate(attrs)

    def create(self, validated_data):
        #Hash the password
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=55, min_length=8, write_only = True)
    username = serializers.CharField(max_length=50, min_length=12)

    class Meta:
        model = User
        fields = ['username', 'password']