from django.http import JsonResponse
from rest_framework import generics,viewsets,status

from bhanu.EduSerializers import EduSerializer
from .models import *
from django.http import HttpResponse
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import action


class EduViewsets(viewsets.ModelViewSet):
    queryset=Educationalloan.objects.all()
    serializer_class=EduSerializer

    def getByRefCode(self, request, refCode):
        try:
            queryset = Educationalloan.objects.filter(
                Q(dsaref_code__icontains=refCode) |
               Q(franrefCode__icontains=refCode)  |
               Q(empref_code=refCode)  
                 ).prefetch_related('personal_details', 'applicationverification')
            if queryset.exists():
               
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response({"message": "No records found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
    
    
    @action(detail=True, methods=['get'])
    def getApprovedRecords(self, request, pk):
     try:
        queryset = Educationalloan.objects.filter(
    Q(dsaref_code__icontains=pk) |
    Q(franrefCode__icontains=pk) |
    Q(empref_code=pk),
    applicationverification__verification_status='Approved'  
    ).select_related('personal_details', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)


    
    def getRejectedRecords(self, request, refCode):
     try:
        queryset = Educationalloan.objects.filter(
    Q(dsaref_code__icontains=refCode) |
    Q(franrefCode__icontains=refCode) |
    Q(empref_code=refCode),
    applicationverification__verification_status='Approved'  
    ).select_related('personal_details', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    
    @action(detail=False, methods=['get'])
    def getUploadDocuments(self, request):
        queryset=Educationalloan.objects.filter(personal_details__adhar_card_front__isnull=False).select_related('personal_details').all()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No Upload Documents found"}, status=404)

    
    
    @action(detail=True, methods=['get'])
    def education_loan_refCode_LoansCount(self, request, pk=None):
        countValue=Educationalloan.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk)).count()
        return Response({'count': countValue}, status=200)
    
    @action(detail=True, methods=['get'])
    def education_loan_refcode_ApprovedCount(self,request, pk=None):
        countValue=Educationalloan.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk),applicationverification__verification_status='Approved').count()
        return Response({'count': countValue}, status=200)
    
    @action(detail=True, methods=['get'])
    def education_loan_refcode_RejectedCount(self,request, pk=None):
        countValue=Educationalloan.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk),applicationverification__verification_status='Rejected').count()
        return Response({'count': countValue}, status=200)
    
    
    
    
    # Franchise
    def getByFranchiseRefCode(self, request, refCode):
        try:
            queryset = Educationalloan.objects.filter(dsaref_code=None,franrefCode=refCode,empref_code=None).prefetch_related('personal_details', 'applicationverification')
            if queryset.exists():
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response({"message": "No records found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
        
    @action(detail=True, methods=['get'])
    def getFranchiseApprovedRecords(self, request, pk):
     try:
        queryset = Educationalloan.objects.filter(
   dsaref_code=None,franrefCode=pk,empref_code=None,
    applicationverification__verification_status='Approved'  
    ).select_related('personal_details', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    
    
    @action(detail=True, methods=['get'])
    def getFranchiseRejectedRecords(self, request, pk):
     try:
        queryset = Educationalloan.objects.filter(
   dsaref_code=None,franrefCode=pk,empref_code=None,
    applicationverification__verification_status='Rejected'  
    ).select_related('personal_details', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No Rejected records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)

