from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate



class UserSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email', 'phone', 'image', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # Check if password and password2 match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Remove password2 from validated_data since it's not in the User model
        validated_data.pop('password2')
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        # Create a new user instance
        user = User.objects.create(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        # Remove password2 from validated_data if it exists
        validated_data.pop('password2', None)
        
        # Check if password is in validated_data and hash it if present
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        
        # Update the instance with the remaining validated data
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")
        self.context['user'] = user  # Save the user for token creation
        return data