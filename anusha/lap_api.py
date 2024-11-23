from rest_framework import viewsets,status
from rest_framework.decorators import action

from .lapserializers import *
from .models import *
from ravi.models import *
from seetha.models import *
from seetha.carserializers import *
from ravi.hlserializers import *
from business.models import *
from business.Busi_serializers import *
from bhanu.models import *
from bhanu.EduSerializers import *
from django.http import JsonResponse
from rest_framework.response import Response

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q


from rest_framework.decorators import action


class LapViewSet(viewsets.ModelViewSet):
    queryset=LoanApplication.objects.all()
    serializer_class=LoanApplicationSerializer


    @action(detail=False, methods=['get'],url_path='getdisbursementdetails')
    def get_disbursement_details(self,request):
        queryset=LoanApplication.objects.filter(disbursementdetail__isnull=False).distinct()
        serializer = LoanApplicationSerializer(queryset, many=True)

        personal_details_queryset = PersonalDetail.objects.filter(disbursementdetail__isnull=False).distinct()
        personal_details_serializer = plApplicationSerializer(personal_details_queryset, many=True)


        home_details_queryset = CustomerProfile.objects.filter(disbursementdetail__isnull=False).distinct()
        home_details_serializer = hlApplicationSerializer(home_details_queryset, many=True)

        car_details_queryset = CarLoan.objects.filter(disbursementdetail__isnull=False).distinct()
        car_details_serializer = CarLoanSerializer(car_details_queryset, many=True)

        bus_details_queryset = BusinessLoan.objects.filter(disbursementdetail__isnull=False).distinct()
        bus_details_serializer = BusiSerializer(bus_details_queryset, many=True)

        edu_details_queryset =Educationalloan.objects.filter(disbursementdetail__isnull=False).distinct()
        edu_details_serializer = EduSerializer(edu_details_queryset, many=True)
        
        response_data = {
            'personal_details': personal_details_serializer.data,
            'loan_applications': serializer.data,
            'home_applications': home_details_serializer.data,
            'car_applications':car_details_serializer.data,
            'bus_applications':bus_details_serializer.data,
            'edu_applications':edu_details_serializer.data
        }
    
        return Response(response_data)
    # Bhanu
    def getByRefCode(self, request, refCode):
        try:
            queryset = LoanApplication.objects.filter(
                Q(dsaref_code__icontains=refCode) |
                Q(franrefCode__icontains=refCode)  |
                Q(empref_code=refCode)  
                 ).prefetch_related('lapdocument', 'applicationverification')
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
        queryset = LoanApplication.objects.filter(
    Q(dsaref_code__icontains=pk) |
    Q(franrefCode__icontains=pk) |
    Q(empref_code=pk),
    applicationverification__verification_status='Approved'  
    ).select_related('lapdocument', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)
     
    @action(detail=True, methods=['get'])
    def getRejectedRecords(self, request, pk):
     try:
        queryset = LoanApplication.objects.filter(
    Q(dsaref_code__icontains=pk) |
    Q(franrefCode__icontains=pk) |
    Q(empref_code=pk),
    applicationverification__verification_status='Rejected'  
    ).select_related('lapdocument', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No rejected records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)
     
    @action(detail=True, methods=['get'])
    def business_loan_refCode_LoansCount(self, request, pk=None):
        countValue=LoanApplication.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk)).count()
        return Response({'count': countValue}, status=200)
     
    
    @action(detail=True, methods=['get'])
    def business_loan_refcode_ApprovedCount(self,request, pk=None):
        countValue=LoanApplication.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk),applicationverification__verification_status='Approved').count()
        return Response({'count': countValue}, status=200)
    
    @action(detail=True, methods=['get'])
    def business_loan_refcode_RejectedCount(self,request, pk=None):
        countValue=LoanApplication.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk),applicationverification__verification_status='Rejected').count()
        return Response({'count': countValue}, status=200)
    # Franchise.........
    def getFranchiseByRefCode(self, request, refCode):
        try:
            queryset = LoanApplication.objects.filter(
                dsaref_code=None,
               franrefCode=refCode,
               empref_code=None,
                 ).prefetch_related('lapdocument', 'applicationverification')
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
        queryset = LoanApplication.objects.filter(
               dsaref_code=None,
               franrefCode=pk,
               empref_code=None,
        applicationverification__verification_status='Approved'  
       ).select_related('lapdocument', 'applicationverification')
        
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
        queryset = LoanApplication.objects.filter(
               dsaref_code=None,
               franrefCode=pk,
               empref_code=None,
    applicationverification__verification_status='Rejected'  
    ).select_related('lapdocument', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No rejected records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)

    
# Bhanu


        


class goldviewset(viewsets.ModelViewSet):
    queryset=Goldloanapplication.objects.all()
    serializer_class=goldapplicationSerializer

class otherviewset(viewsets.ModelViewSet):
    queryset=otherloans.objects.all()
    serializer_class=otherloanSerializer

class dsaViewSet(viewsets.ModelViewSet):
    queryset=dsa.objects.all()
    serializer_class=dsaSerializer
   
    @action(detail=False, methods=['get'], url_path='(?P<dsa_id>[^/.]+)')
    def get_by_dsa_registerid(self, request, dsa_id=None):
        # Fetch DSA by `dsa_registerid`
        if not dsa_id:
            return Response({'error': 'dsa_registerid is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            employee = dsa.objects.get(dsa_id=dsa_id)
            serializer = dsaSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except dsa.DoesNotExist:
            return Response({'error': 'DSA not found'}, status=status.HTTP_404_NOT_FOUND)
        
    


class franchiseViewSet(viewsets.ModelViewSet):
    queryset=franchise.objects.all()
    serializer_class=franchiseSerializer

    @action(detail=False, methods=['get'], url_path='(?P<franchise_id>[^/.]+)')
    def get_by_franchiseid(self, request, franchise_id=None):
        # Fetch franchise by `franchise_id`
        if not franchise_id:
            return Response({'error': 'franchise_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            employee = franchise.objects.get(franchise_id=franchise_id)
            serializer = franchiseSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except franchise.DoesNotExist:
            return Response({'error': 'DSA not found'}, status=status.HTTP_404_NOT_FOUND)