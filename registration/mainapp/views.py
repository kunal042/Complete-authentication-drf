from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import UserSignupSerializer,LoginSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

class UserSignupView(APIView):
    # GET: Retrieve a list of users or a specific user by ID
    # authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated]  # Require authentication
    def get(self, request, pk=None):
        if pk:  # Retrieve a specific user by ID
            user = get_object_or_404(User, pk=pk)
            serializer = UserSignupSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:  # Retrieve all users
            users = User.objects.all()
            serializer = UserSignupSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # POST: Create a new user
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT: Update all fields of an existing user
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSignupSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH: Partially update specific fields of an existing user
    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSignupSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User partially updated successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Delete a user by ID
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({'message': 'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)



class LoginView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Validate the user credentials
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.context['user']
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                'message': 'Login successful!',
                'access': str(access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    def get(self, request):
        return Response({"message": "This is a protected view!"}, status=status.HTTP_200_OK)