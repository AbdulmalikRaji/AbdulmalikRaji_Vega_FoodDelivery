from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'longitude', 'latitude', 'delivery_location']

    def validate_password(self, value):
        # Django's default password validation
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))

        # Custom validation for uppercase, lowercase, and number
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter, one lowercase letter, and one number."
            )
        return value

    def validate(self, data):
        # Check if password and confirm_password match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Remove confirm_password before saving
        validated_data.pop('confirm_password')  
        
        # Create user and hash password
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            longitude=validated_data['longitude'],
            latitude=validated_data['latitude'],
            delivery_location=validated_data['delivery_location']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
