from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import *
from django.contrib.auth import authenticate,logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# Generate Token Manually

def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("user created successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(request=request,email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': ['Invalid User']},
                            status=status.HTTP_404_NOT_FOUND)
        


# class UserLogoutView(APIView):

#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         print(request.user)
#         request.user.auth_token.delete()
#         logout(request)
#         return Response(status=status.HTTP_200_OK)



class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = GetAllUserSerializer(users, many=True)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)
    
    
    def delete(self, request, pk):
        user = User.objects.filter(id=pk)
        if user.exists():
            user.delete()
            message = f"User with id {pk} has been deleted."
            return Response({'message': message}, status=status.HTTP_204_NO_CONTENT)
        else:
            message = f"User with id {pk} does not exist."
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)
        

    def put(self, request, pk):
        user = User.objects.filter(id=pk)

        if user.exists():
            request_data = UpdateUserSerializer(data=request.data,partial=True)
            request_data.is_valid(raise_exception=True)
            request_data = request_data.validated_data
            User.update_data(request_data,pk)
            return Response({'message': "user updated successfully"},status=status.HTTP_200_OK)
        
        else:
            message = f"User with id {pk} does not exist."
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)
        
        
class UserByIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        user = User.objects.filter(id=pk).first()
        if user:
            serializer = GetAllUserSerializer(user)
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            message = f"User with id {pk} not found."
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)
    


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):

    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):

    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)