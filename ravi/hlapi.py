from rest_framework import viewsets
from ravi.hlserializers import *
from .models import *

from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response


class CustomerViewSet(viewsets.ModelViewSet):
    queryset=CustomerProfile.objects.all()
    serializer_class=hlApplicationSerializer
    
    
    

    def getByRefCode(self, request, refCode):
        try:
            queryset = CustomerProfile.objects.filter(
                Q(dsaref_code__icontains=refCode) |
               Q(franrefCode__icontains=refCode)  |
               Q(empref_code=refCode)  
                 ).prefetch_related('hldocument', 'applicationverification')
            if queryset.exists():
               
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response({"message": "No records found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
    def getApprovedRecords(self, request, refCode):
      try:
        queryset = CustomerProfile.objects.filter(
        Q(dsaref_code__icontains=refCode) |
        Q(franrefCode__icontains=refCode) |
        Q(empref_code=refCode),
        applicationverification__verification_status='Approved'  
       ).select_related('hldocument', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

      except Exception as e:
        return Response({"error": str(e)}, status=500)
     
    def getRejectedRecords(self, request, refCode):
     try:
        queryset = CustomerProfile.objects.filter(
        Q(dsaref_code__icontains=refCode) |
        Q(franrefCode__icontains=refCode) |
        Q(empref_code=refCode),
        applicationverification__verification_status='Rejected'  
       ).select_related('hldocument', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    
    
    
    @action(detail=True, methods=['get'])
    def business_loan_refCode_LoansCount(self, request, pk=None):
        countValue=CustomerProfile.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk)).count()
        return Response({'count': countValue}, status=200)
    
    @action(detail=True, methods=['get'])
    def business_loan_refcode_ApprovedCount(self,request, pk=None):
        countValue=CustomerProfile.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk),applicationverification__verification_status='Approved').count()
        return Response({'count': countValue}, status=200)
    
    @action(detail=True, methods=['get'])
    def business_loan_refcode_RejectedCount(self,request, pk=None):
        countValue=CustomerProfile.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk),applicationverification__verification_status='Rejected').count()
        return Response({'count': countValue}, status=200)
    
    # Franchise...................
    def getByFranchiseRefCode(self, request, refCode):
        try:
            queryset = CustomerProfile.objects.filter(dsaref_code=None,franrefCode=refCode,empref_code=None).prefetch_related('hldocument', 'applicationverification')
            if queryset.exists():
               
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response({"message": "No records found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
   
    def getFranchiseApprovedRecords(self, request, refCode):
      try:
        queryset = CustomerProfile.objects.filter(
       dsaref_code=None,franrefCode=refCode,empref_code=None,
        applicationverification__verification_status='Approved'  
       ).select_related('hldocument', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

      except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    
    def getFranchiseRejectedRecords(self, request, refCode):
     try:
        queryset = CustomerProfile.objects.filter(
        dsaref_code=None,franrefCode=refCode,empref_code=None,
        applicationverification__verification_status='Rejected'  
       ).select_related('hldocument', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    




class PlViewSet(viewsets.ModelViewSet):
    queryset=PersonalDetail.objects.all()
    serializer_class=plApplicationSerializer

   
 
    def getByRefCode(self, request, refCode):
        try:
            queryset = PersonalDetail.objects.filter(
                Q(dsaref_code__icontains=refCode) |
               Q(franrefCode__icontains=refCode)  |
               Q(empref_code=refCode)  
                 ).prefetch_related('pldocument','applicationverification')
            if queryset.exists():
               
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response({"message": "No records found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
    def getApprovedRecords(self, request, refCode):
      try:
        queryset = PersonalDetail.objects.filter(
        Q(dsaref_code__icontains=refCode) |
        Q(franrefCode__icontains=refCode) |
        Q(empref_code=refCode),
        applicationverification__verification_status='Approved'  
       ).select_related('lapdocument', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

      except Exception as e:
        return Response({"error": str(e)}, status=500)
     
    def getRejectedRecords(self, request, refCode):
     try:
        queryset = PersonalDetail.objects.filter(
        Q(dsaref_code__icontains=refCode) |
        Q(franrefCode__icontains=refCode) |
        Q(empref_code=refCode),
        applicationverification__verification_status='Rejected'  
       ).select_related('lapdocument', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    
    
    
    @action(detail=True, methods=['get'])
    def business_loan_refCode_LoansCount(self, request, pk=None):
        countValue=PersonalDetail.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk)).count()
        return Response({'count': countValue}, status=200)
    
    @action(detail=True, methods=['get'])
    def business_loan_refcode_ApprovedCount(self,request, pk=None):
        countValue=PersonalDetail.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk),applicationverification__verification_status='Approved').count()
        return Response({'count': countValue}, status=200)
    
    @action(detail=True, methods=['get'])
    def business_loan_refcode_RejectedCount(self,request, pk=None):
        countValue=PersonalDetail.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk),applicationverification__verification_status='Rejected').count()
        return Response({'count': countValue}, status=200)
    
    
    # Franchise...................
    
    
    def getFranchiseRejectedRecords(self, request, refCode):
     try:
        queryset = PersonalDetail.objects.filter(
       dsaref_code=None,franrefCode=refCode,empref_code=None,
        applicationverification__verification_status='Rejected'  
       ).select_related('lapdocument', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    
    def getFranchiseApprovedRecords(self, request, refCode):
      try:
        queryset = PersonalDetail.objects.filter(
       dsaref_code=None,franrefCode=refCode,empref_code=None,
        applicationverification__verification_status='Approved'  
       ).select_related('lapdocument', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

      except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    
    def getFranchiseByRefCode(self, request, refCode):
        try:
            queryset = PersonalDetail.objects.filter(
                dsaref_code=None,franrefCode=refCode,empref_code=None
                 ).prefetch_related('pldocument','applicationverification')
            if queryset.exists():
               
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response({"message": "No records found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        