from dataclasses import fields
from rest_framework import status
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Contact

class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'country_code', 'phone_number', 'first_name', 'last_name', 'contact_picture', 'is_favourite']

    def validate(self, attrs):
        if Contact.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({'detail': 'Phone number already exists!'})
        return super().validate(attrs)
