from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,UserChangePasswordsSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer,UserListSerializer
from .renderers import UserRenderers

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



# Create your views here.
class UserListView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this

    def get(self, request, format=None):
        users = User.objects.all()  # Retrieve all users
        serializer = UserListSerializer(users, many=True)  # Serialize the user queryset
        return Response(serializer.data, status=status.HTTP_200_OK)
    


    
class UserRegistrationView(APIView):
    
    renderer_classes = [UserRenderers]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({ 'token':token,'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    renderer_classes = [UserRenderers]
    def post(self,request, formate=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_filed_error':['Email or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class UserProfileView(APIView):
#     renderer_classes = [UserRenderers]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         serializer = UserProfileSerializer(request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    

# Accress profile to also add PUT PATCH and DELETE Opeations

class UserProfileView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    # GET method for retrieving user profile
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PATCH method for partially updating user profile
    def patch(self, request, format=None):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT method for fully updating user profile
    def put(self, request, format=None):
        serializer = UserProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method for deleting user profile
    def delete(self, request, format=None):
        request.user.delete()
        return Response({"detail": "User profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def post(self, request, formate=None):
        serializer = UserChangePasswordsSerializer(data=request.user, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderers]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
  

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderers]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)