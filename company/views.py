from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.models import User
from company.models import Company
from company.serializers import *
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class CompanyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        creator = User.objects.get(email=request.user)
        serializer = CreateCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_data = serializer.validated_data
        company = Company.create_company(company_data, creator)
        return Response({"message": "company created successfully"}, status=status.HTTP_201_CREATED)

    def get(self, request):
        users = Company.objects.all()
        serializer = GetAllCompanySerializer(users, many=True)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        company = Company.objects.filter(id=pk)
        if company.exists():
            company.delete()
            message = f"Company with id {pk} has been deleted."
            return Response({'message': message}, status=status.HTTP_204_NO_CONTENT)
        else:
            message = f"Company with id {pk} does not exist."
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        company = Company.objects.filter(id=pk)

        if company.exists():
            request_data = UpdateCompanySerializer(data=request.data, partial=True)
            request_data.is_valid(raise_exception=True)
            request_data = request_data.validated_data
            Company.update_data(request_data, pk)
            return Response(status=status.HTTP_200_OK)

        else:
            message = f"Company with id {pk} does not exist."
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)


class CompanyListByIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        company = Company.objects.filter(id=pk).first()
        if company:
            serializer = GetAllCompanySerializer(company)
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            message = f"Company with id {pk} not found."
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)
