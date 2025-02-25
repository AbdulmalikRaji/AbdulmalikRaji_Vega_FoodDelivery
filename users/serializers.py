from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'longitude', 'latitude', 'delivery_location']

    def validate_password(self, value):
        # Validate password strength
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, validated_data):
        # Create user and hash password
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            longitude=validated_data['longitude'],
            latitude=validated_data['latitude'],
            delivery_location=validated_data['delivery_location']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
