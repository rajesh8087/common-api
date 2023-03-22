from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    UpdateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User
from user.serializers import *
from django.http import Http404


class UserRegistrationView(CreateAPIView):
    def post(self, request):

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "User created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserLogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"msg": "Logout Successfully"}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response({"errors": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)


class UserView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            user = self.get_object(pk=pk)
            user.delete()
            message = f"User with id {pk} has been deleted."
            return Response({"message": message}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            message = f"User with id {pk} does not exist."
            return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            user = self.get_object(pk=pk)
            serializer = UpdateUserSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.update(
                    instance=user, validated_data=serializer.validated_data
                )

                return Response(
                    {"message": "User updated successfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            message = f"User with id {pk} does not exist."
            return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)


class ListUsersView(ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Changed Successfully"}, status=status.HTTP_200_OK
        )


class SendPasswordResetEmailView(APIView):
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Reset link send. Please check your Email"},
            status=status.HTTP_200_OK,
        )


class UserPasswordResetView(APIView):
    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Reset Successfully"}, status=status.HTTP_200_OK
        )


class FetchChildEmployeeView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        user = request.user
        serializer = FetchChildEmployeeSerializer(instance=user)

        return Response(serializer.data, status=status.HTTP_200_OK)
