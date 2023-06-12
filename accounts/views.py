from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
from rest_framework.pagination import LimitOffsetPagination

from accounts.models import *
from accounts.serializers import *


# Create your views here.
class SignupView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser,MultiPartParser,FormParser]
    
    def get(self,request,id):
        instance = Account.objects.filter(id=id)
        if not instance.exists():
            return Response({"status":"failed","message":"No user found with given id"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = ViewAccountSerializer(instance=instance.first(),many=False)
        return Response({"status":"success","data":serializer.data},status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = CreateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":"success","message":"Account created successfully","data":serializer.data},status=status.HTTP_201_CREATED)

    def patch(self,request,id):
        if not request.user.is_authenticated or request.user.id != id:
            return Response({"status":"failed","message":"You don't have permission to perform this operation"},status=status.HTTP_401_UNAUTHORIZED)
        
        instance = Account.objects.filter(id=id)
        if not instance.exists():
            return Response({"status":"failed","message":"No user found with given id"},status=status.HTTP_404_NOT_FOUND)
        
        request.data.pop('id',None)
        request.data.pop('user_type',None)
        serializer = CreateAccountSerializer(instance=instance.first(),data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":"success","message":"User updated successfully","data":serializer.data},status=status.HTTP_200_OK)
    

class CompanyView(APIView):
    pagination_class = LimitOffsetPagination
    parser_classes = [FormParser,JSONParser,MultiPartParser]
    permission_classes = [AllowAny]

    def get(self, request, id=None):
        queryset = Company.objects.all()

        if id:
            company = queryset.filter(id=id)
            if not company.exists():
                return Response({"status": "failed", "message": "No Company found with the given id"}, status=status.HTTP_404_NOT_FOUND)

            serializer = CompanySerializer(instance=company.first(),many=False)
            return Response({"status": "success", "message": "Data fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = CompanySerializer(instance=paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
    

    def post(self,request):
        if not request.user.is_authenticated:
            return Response({"status":"failed","message":"You must login to perform this operation"},status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":"success","message":"Company profile created successfully","data":serializer.data},status=status.HTTP_200_OK)
    
    def patch(self,request,id):
        if not request.user.is_authenticated:
            return Response({"status":"failed","message":"You must login to perform this operation"},status=status.HTTP_401_UNAUTHORIZED)
        
        instance = Company.objects.filter(id=id)
        if not instance.exists():
            return Response({"status":"failed","message":"No company profile found"},status=status.HTTP_404_NOT_FOUND)
        
        
        serializer = CompanySerializer(instance=instance.first(),data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":"success","message":"Company profile created successfully","data":serializer.data},status=status.HTTP_200_OK)