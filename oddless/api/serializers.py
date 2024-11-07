from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)  # Password confirmation

    class Meta:
        model = User
        fields = ['id','username','first_name', 'last_name', 'email', 'password', 'password2', 'address', 'phone', 'profile_picture']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
        

    def update(self, instance, validated_data):
        # Check if 'password' is in validated_data for PATCH
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super(UserSignupSerializer, self).update(instance, validated_data)
