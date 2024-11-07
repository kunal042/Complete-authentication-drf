from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utlis import Util



class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'address'] 

class UserRegistrationSerializer(serializers.ModelSerializer):
	
	# We are writing this becoz we need confirm password field in our Registratin Request
	password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
	class Meta:
		model = User
		fields=['email', 'name', 'password', 'password2', 'phone', 'address', 'image']
		extra_kwargs={
		'password':{'write_only':True}
		}

	# Validating Password and Confirm Password while Registration
	def validate(self, attrs):
		password = attrs.get('password')
		password2 = attrs.get('password2')
		if password != password2:
			raise serializers.ValidationError("Password and Confirm Password doesn't match")
		return attrs

	def create(self, validate_data):
		return User.objects.create_user(**validate_data)
	

class UserLoginSerializer(serializers.ModelSerializer):
	email = serializers.CharField(max_length=255)
	class Meta:
		model = User
		fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name' , 'phone', 'address', 'image']
  


class UserChangePasswordsSerializer(serializers.ModelSerializer):

	password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
	password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

	class Meta:
		model = User
		fields = ['password', 'password2']

	def validate(self, attrs):
		password = attrs.get('password')
		password2 = attrs.get('password2')
		if password != password2:
			raise serializers.ValidationError("Password and Confirm Password don't match!")
		# user = self.context['request'].user
		# user = self.context['user']
		# user.set_password(password)
		# user.save()
		return attrs  # Return the dictionary of validated data
    
    # def save(self, **kwargs):
    #     # Access the user instance from the context
    #     user = self.context['request'].user
    #     password = self.validated_data['password']
        
    #     # Set and save the new password
    #     user.set_password(password)
    #     user.save()
	def save(self, **kwargs):
		user = self.context['user']
		password = self.validated_data['password']
		user.set_password(password)
		user.save()
		
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link', link)
            # Send EMail
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
        # Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')
		

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')