
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSignupSerializer
from .models import CustomUser


class UserView(APIView):
    # GET: Retrieve a list of users or a specific user by ID
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):

        users = CustomUser.objects.all()
        serializer = UserSignupSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST: Create a new user
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSignupView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        if pk:  # If pk is provided, get the specific user
            user = get_object_or_404(CustomUser, pk=pk)
            serializer = UserSignupSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:  # Otherwise, get all users
            users = CustomUser.objects.all()
            serializer = UserSignupSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    # PUT: Update an existing user's data
    def put(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = UserSignupSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH: Partially update an existing user's data
    def patch(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = UserSignupSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User partially updated successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Delete a user
    def delete(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.delete()
        return Response({'message': 'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
