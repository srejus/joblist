from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import  JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination

from job.models import *
from job.serializers import *

# Create your views here.
class JobView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    pagination_class = LimitOffsetPagination
    
    def get(self,request,id=None):
        queryset = Job.objects.filter(job_status='open')
        if id:
            queryset = queryset.filter(id=id)
            if not queryset.exists():
                return Response({"status":"failed","message":"No job found with the given id"},status=status.HTTP_404_NOT_FOUND)
            
            serializer = JobSerializer(instance=queryset.first(),many=False)
            return Response({"status":"success","message":"Data fetched successfully","data":serializer.data},status=status.HTTP_200_OK)
        
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = JobSerializer(instance=paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self,request):
        if not request.user.is_authenticated:
            return Response({"status":"failed","message":"You don't have permission to perform this operation"},status=status.HTTP_401_UNAUTHORIZED)

        request.data['posted_by'] = request.user.id
        serializer = CreateJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = Company.objects.filter(id=serializer.validated_data.get('company')).first()
        serializer.save(posted_by=request.user,company=company)
        return Response({"status":"success","message":"Job created successfully","data":serializer.data},status=status.HTTP_201_CREATED)

    def patch(self,request,id):
        if not request.user.is_authenticated:
            return Response({"status":"failed","message":"You don't have permission to perform this operation"},status=status.HTTP_401_UNAUTHORIZED)

        if not id:
            return Response({"status":"failed","message":"id is required"},status=status.HTTP_400_BAD_REQUEST)
        
        instance = Job.objects.filter(id=id,posted_by=request.user)
        if not instance.exists():
            return Response({"status":"failed","message":"No job found with given id"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = CreateJobSerializer(instance=instance.first(),data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"status":"success","message":"Job updated successfully","data":serializer.data},status=status.HTTP_200_OK)
    

    def delete(self,request,id):
        if not request.user.is_authenticated:
            return Response({"status":"failed","message":"You don't have permission to perform this operation"},status=status.HTTP_401_UNAUTHORIZED)

        if not id:
            return Response({"status":"failed","message":"id is required"},status=status.HTTP_400_BAD_REQUEST)

        instance = Job.objects.filter(id=id,posted_by=request.user)
        if not instance.exists():
            return Response({"status":"failed","message":"No job found with given id"},status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()
        return Response({"status":"success","message":"Job deleted successfully"},status=status.HTTP_200_OK)
