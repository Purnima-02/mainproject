from django.http import JsonResponse
from rest_framework import generics,viewsets,status

from anusha.models import AllInsurance, GeneralInsurance, Goldloanapplication, LifeInsurance, LoanApplication, healthInsurance, otherloans
from bhanu.models import Educationalloan
from ganesh.models import CreditDetail
from ravi.models import CustomerProfile, PersonalDetail
from seetha.models import CarLoan
from .Busi_serializers import BusiSerializer,BusiBasicDetailFormSrializer
from .models import *
from django.http import HttpResponse
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import action
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


class BusiBasicDetailviewset(viewsets.ModelViewSet):
    queryset=busbasicdetailform.objects.all()
    serializer_class=BusiBasicDetailFormSrializer


    def getApplicationId(self,request, mobileNumber):
        try:
            queryset = busbasicdetailform.objects.filter(mobile_number=mobileNumber)
            if queryset.exists():
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response({"message": "No records found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class BusiViewsets(viewsets.ModelViewSet):
    queryset=BusinessLoan.objects.all()
    serializer_class=BusiSerializer

    def getByRefCode(self, request, refCode):
        try:
            queryset = BusinessLoan.objects.filter(
                Q(dsaref_code__icontains=refCode) |
               Q(franrefCode__icontains=refCode)  |
               Q(empref_code=refCode)  
                 ).prefetch_related('BussinessLoandocuments', 'applicationverification')
            if queryset.exists():
               
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response({"message": "No records found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
    def getApprovedRecords(self, request, refCode):
      try:
        queryset = BusinessLoan.objects.filter(
        Q(dsaref_code__icontains=refCode) |
        Q(franrefCode__icontains=refCode) |
        Q(empref_code=refCode),
        applicationverification__verification_status='Approved'  
       ).select_related('BussinessLoandocuments', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

      except Exception as e:
        return Response({"error": str(e)}, status=500)
     
    def getRejectedRecords(self, request, refCode):
     try:
        queryset = BusinessLoan.objects.filter(
        Q(dsaref_code__icontains=refCode) |
        Q(franrefCode__icontains=refCode) |
        Q(empref_code=refCode),
        applicationverification__verification_status='Rejected'  
       ).select_related('BussinessLoandocuments', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    
    
    @action(detail=True, methods=['get'])
    def credit_loan_FranCode_LoansCount(self, request, pk=None):
        countValue=CreditDetail.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count()
        return Response({'count': countValue}, status=200)
        
    @action(detail=True, methods=['get'])
    def credit_loan_refCode_LoansCount(self, request, pk=None):
        countValue=CreditDetail.objects.filter(Q(dsaref_code=pk) |  Q(empref_code=pk)).count()
        return Response({'count': countValue}, status=200)
    
    
    @action(detail=True, methods=['get'])
    def business_loan_refCode_LoansCount(self, request, pk=None):
        countValue=BusinessLoan.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk)).count()
        return Response({'count': countValue}, status=200)
    
    @action(detail=True, methods=['get'])
    def business_loan_refcode_ApprovedCount(self,request, pk=None):
        countValue=BusinessLoan.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk),applicationverification__verification_status='Approved').count()
        return Response({'count': countValue}, status=200)
    
    @action(detail=True, methods=['get'])
    def business_loan_refcode_RejectedCount(self,request, pk=None):
        countValue=BusinessLoan.objects.filter(Q(dsaref_code=pk)|Q(franrefCode=pk)|Q(empref_code=pk),applicationverification__verification_status='Rejected').count()
        return Response({'count': countValue}, status=200)
    
        
    
    @action(detail=True, methods=['get'])
    def All_loan_refCode_LoansCount(self, request, pk=None):
      if request.GET.get('date'):
          date=request.GET.get('date')
          strtDate=date.split(' to ')[0]
          endDate=date.split(' to ')[1]
          date_obj1 = datetime.strptime(strtDate, '%Y-%m-%d').date()
          date_obj2 = datetime.strptime(endDate, '%Y-%m-%d').date()
          
      with ThreadPoolExecutor() as executor:
       if not request.GET.get('date'):
       
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk)).count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk)).count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk)).count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk)).count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk)).count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk)).count())
        goldCount=executor.submit(lambda: Goldloanapplication.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk)).count())
        otherCount=executor.submit(lambda: otherloans.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk)).count())
        allInsuranceCount=executor.submit(lambda: AllInsurance.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk)).count())
        lifeInsuranceCount=executor.submit(lambda: LifeInsurance.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk)).count())
        generalInsuranceCount=executor.submit(lambda: GeneralInsurance.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk)).count())
        healthInsuranceCount=executor.submit(lambda: healthInsurance.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk)).count())
        creditCount=executor.submit(lambda: CreditDetail.objects.filter(Q(dsaref_code=pk) | Q(empref_code=pk)).count())

       else:
    
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(Q(dsaref_code=pk) | Q(empref_code=pk),created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        goldCount=executor.submit(lambda: Goldloanapplication.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        otherCount=executor.submit(lambda: otherloans.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        creditCount=executor.submit(lambda: CreditDetail.objects.filter(Q(dsaref_code=pk) | Q(empref_code=pk),created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        allInsuranceCount=executor.submit(lambda: AllInsurance.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        lifeInsuranceCount=executor.submit(lambda: LifeInsurance.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        generalInsuranceCount=executor.submit(lambda: GeneralInsurance.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        healthInsuranceCount=executor.submit(lambda: healthInsurance.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),created_at__gte=date_obj1,created_at__lte=date_obj2).count())
           
      totalCount=businessCount.result()+eduCount.result()+lapCount.result()+perCount.result()+homeCount.result()+carCount.result()+goldCount.result()+otherCount.result()
      totalInsurance=allInsuranceCount.result()+lifeInsuranceCount.result()+generalInsuranceCount.result()+healthInsuranceCount.result()
      return Response({
          'buscount':businessCount.result(),
          'educount':eduCount.result(),
          'lapcount':lapCount.result(),
          'percount':perCount.result(),
          'homecount':homeCount.result(),
          'carcount':carCount.result(),
          'goldcount':goldCount.result(),
          'othercount':otherCount.result(),
          'totalcount':totalCount,
          'creditcount':creditCount.result(),
          'totalInsurances':totalInsurance,
          'allinsurance':allInsuranceCount.result(),
          'lifeinsurance':lifeInsuranceCount.result(),
          'generalinsurance':generalInsuranceCount.result(),
          'healthinsurance':healthInsuranceCount.result(),
          
          }, status=200)
  
   
    
    @action(detail=True, methods=['get'])
    def All_loan_refCode_ApprovedCount(self, request, pk=None):
      countValue=[]
      if request.GET.get('date'):
          date=request.GET.get('date')
          strtDate=date.split(' to ')[0]
          endDate=date.split(' to ')[1]
          date_obj1 = datetime.strptime(strtDate, '%Y-%m-%d').date()
          date_obj2 = datetime.strptime(endDate, '%Y-%m-%d').date()
          
      with ThreadPoolExecutor() as executor:
       if not request.GET.get('date'):
       
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),applicationverification__verification_status='Approved').count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),applicationverification__verification_status='Approved').count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),applicationverification__verification_status='Approved').count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),applicationverification__verification_status='Approved').count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),applicationverification__verification_status='Approved').count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),applicationverification__verification_status='Approved').count())

       else:
      
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(Q(dsaref_code=pk) | Q(empref_code=pk),applicationverification__verification_status='Approved',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),applicationverification__verification_status='Approved',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(Q(dsaref_code=pk) | Q(empref_code=pk),applicationverification__verification_status='Approved',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),applicationverification__verification_status='Approved',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(Q(dsaref_code=pk) | Q(empref_code=pk),applicationverification__verification_status='Approved',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),applicationverification__verification_status='Approved',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
          
       totalCount=businessCount.result()+eduCount.result()+lapCount.result()+perCount.result()+homeCount.result()+carCount.result()
      return Response({
          'busapprovedcount':businessCount.result(),
          'eduapprovedcount':eduCount.result(),
          'lapapprovedcount':lapCount.result(),
          'perapprovedcount':perCount.result(),
          'homeapprovedcount':homeCount.result(),
          'carapprovedcount':carCount.result(),
          'totalApprovedcount':totalCount,
          }, status=200)
  
    
    @action(detail=True, methods=['get'])
    def All_loan_refCode_RejectedCount(self, request, pk=None):
      countValue=[]
      if request.GET.get('date'):
          date=request.GET.get('date')
          strtDate=date.split(' to ')[0]
          endDate=date.split(' to ')[1]
          date_obj1 = datetime.strptime(strtDate, '%Y-%m-%d').date()
          date_obj2 = datetime.strptime(endDate, '%Y-%m-%d').date()
          
      with ThreadPoolExecutor() as executor:
       if not request.GET.get('date'):
       
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),applicationverification__verification_status='Rejected').count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),applicationverification__verification_status='Rejected').count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),applicationverification__verification_status='Rejected').count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),applicationverification__verification_status='Rejected').count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),applicationverification__verification_status='Rejected').count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(Q(dsaref_code=pk) | Q(franrefCode=pk) | Q(empref_code=pk),applicationverification__verification_status='Rejected').count())
       else:
        
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),applicationverification__verification_status='Rejected',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),applicationverification__verification_status='Rejected',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(Q(dsaref_code=pk) | Q(empref_code=pk),applicationverification__verification_status='Rejected',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(Q(dsaref_code=pk) | Q(empref_code=pk),applicationverification__verification_status='Rejected',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),applicationverification__verification_status='Rejected',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(Q(dsaref_code=pk)  | Q(empref_code=pk),applicationverification__verification_status='Rejected',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
           
    
      totalCount=businessCount.result()+eduCount.result()+lapCount.result()+perCount.result()+homeCount.result()+carCount.result()
      return Response({
          'busrejectedcount':businessCount.result(),
          'edurejectedcount':eduCount.result(),
          'laprejectedcount':lapCount.result(),
          'perrejectedcount':perCount.result(),
          'homerejectedcount':homeCount.result(),
          'carrejectedcount':carCount.result(),
          'totrejectedcount':totalCount,
          }, status=200)      
      # Franchise
    def getByFranchiseRefCode(self, request, refCode):
        try:
            queryset = BusinessLoan.objects.filter(dsaref_code=None,franrefCode=refCode,empref_code=None).prefetch_related('BussinessLoandocuments', 'applicationverification')
            if queryset.exists():
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response({"message": "No records found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
    def getFranchiseRejectedRecords(self, request, refCode):
     try:
        queryset = BusinessLoan.objects.filter(dsaref_code=None,franrefCode=refCode,empref_code=None,
        applicationverification__verification_status='Rejected'  
       ).select_related('BussinessLoandocuments', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No Rejected records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)

    def getFranchiseApprovedRecords(self, request, refCode):
     try:
        queryset = BusinessLoan.objects.filter(
        dsaref_code=None,franrefCode=refCode,empref_code=None,
        applicationverification__verification_status='Approved'  
       ).select_related('BussinessLoandocuments', 'applicationverification')
        
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No approved records found"}, status=404)

     except Exception as e:
        return Response({"error": str(e)}, status=500)
        
    @action(detail=True, methods=['get'])
    def All_Frloan_refCode_LoansCount(self, request, pk=None):
      if request.GET.get('date'):
          date=request.GET.get('date')
         
          strtDate=date.split(' to ')[0]
          endDate=date.split(' to ')[1]
          date_obj1 = datetime.strptime(strtDate, '%Y-%m-%d').date()
          date_obj2 = datetime.strptime(endDate, '%Y-%m-%d').date()
          
      with ThreadPoolExecutor() as executor:
       if not request.GET.get('date'):
       
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count())
        goldCount=executor.submit(lambda: Goldloanapplication.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count())
        otherCount=executor.submit(lambda: otherloans.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count())
        allInsuranceCount=executor.submit(lambda: AllInsurance.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count())
        lifeInsuranceCount=executor.submit(lambda: LifeInsurance.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count())
        generalInsuranceCount=executor.submit(lambda: GeneralInsurance.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count())
        creditCount=executor.submit(lambda: CreditDetail.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count())
        healthInsuranceCount=executor.submit(lambda: healthInsurance.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None).count())

        
       else:
      
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        goldCount=executor.submit(lambda: Goldloanapplication.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        otherCount=executor.submit(lambda: otherloans.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        creditCount=otherCount=executor.submit(lambda: CreditDetail.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        allInsuranceCount=executor.submit(lambda: AllInsurance.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        lifeInsuranceCount=executor.submit(lambda: LifeInsurance.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        generalInsuranceCount=executor.submit(lambda: GeneralInsurance.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        healthInsuranceCount=executor.submit(lambda: healthInsurance.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
           
      totalCount=businessCount.result()+eduCount.result()+lapCount.result()+perCount.result()+homeCount.result()+carCount.result()+goldCount.result()+otherCount.result()
      totalInsurance=allInsuranceCount.result()+lifeInsuranceCount.result()+generalInsuranceCount.result()+healthInsuranceCount.result()
      return Response({
          'buscount':businessCount.result(),
          'educount':eduCount.result(),
          'lapcount':lapCount.result(),
          'percount':perCount.result(),
          'homecount':homeCount.result(),
          'carcount':carCount.result(),
          'goldcount':goldCount.result(),
          'othercount':otherCount.result(),
          'totalcount':totalCount,
          'creditcount':creditCount.result(),
          'totalInsurances':totalInsurance,
          'allinsurance':allInsuranceCount.result(),
          'lifeinsurance':lifeInsuranceCount.result(),
          'generalinsurance':generalInsuranceCount.result(),
          'healthinsurance':healthInsuranceCount.result(),
          
          }, status=200)
    
    @action(detail=True, methods=['get'])
    def All_Frloan_refCode_ApprovedCount(self, request, pk=None):
      countValue=[]
      if request.GET.get('date'):
          date=request.GET.get('date')
          strtDate=date.split(' to ')[0]
          endDate=date.split(' to ')[1]
          date_obj1 = datetime.strptime(strtDate, '%Y-%m-%d').date()
          date_obj2 = datetime.strptime(endDate, '%Y-%m-%d').date()
          
      with ThreadPoolExecutor() as executor:
       if not request.GET.get('date'):
        
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Approved').count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Approved').count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Approved').count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Approved').count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Approved').count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Approved').count())
    
       else:
        
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Approved',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Approved',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Approved',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Approved',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Approved',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Approved',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
          
       totalCount=businessCount.result()+eduCount.result()+lapCount.result()+perCount.result()+homeCount.result()+carCount.result()
      return Response({
          'busapprovedcount':businessCount.result(),
          'eduapprovedcount':eduCount.result(),
          'lapapprovedcount':lapCount.result(),
          'perapprovedcount':perCount.result(),
          'homeapprovedcount':homeCount.result(),
          'carapprovedcount':carCount.result(),
          'totalApprovedcount':totalCount,
          }, status=200)
  
    
    @action(detail=True, methods=['get'])
    def All_Frloan_refCode_RejectedCount(self, request, pk=None):
      countValue=[]
      if request.GET.get('date'):
          date=request.GET.get('date')
          strtDate=date.split(' to ')[0]
          endDate=date.split(' to ')[1]
          date_obj1 = datetime.strptime(strtDate, '%Y-%m-%d').date()
          date_obj2 = datetime.strptime(endDate, '%Y-%m-%d').date()
          
      with ThreadPoolExecutor() as executor:
       if not request.GET.get('date'):
       
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Rejected').count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Rejected').count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Rejected').count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Rejected').count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Rejected').count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Rejected').count())
       else:
       
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Rejected',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Rejected',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Rejected',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Rejected',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Rejected',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(dsaref_code=None,franrefCode=pk,empref_code=None,applicationverification__verification_status='Rejected',created_at__gte=date_obj1,created_at__lte=date_obj2).count())
           
      totalCount=businessCount.result()+eduCount.result()+lapCount.result()+perCount.result()+homeCount.result()+carCount.result()
      return Response({
          'busrejectedcount':businessCount.result(),
          'edurejectedcount':eduCount.result(),
          'laprejectedcount':lapCount.result(),
          'perrejectedcount':perCount.result(),
          'homerejectedcount':homeCount.result(),
          'carrejectedcount':carCount.result(),
          'totrejectedcount':totalCount,
          }, status=200)    
      
    # Data Processed to only Particular Franchise like including DSA,Sales,Franchise Owner 
    @action(detail=True, methods=['get'])
    def All_TotlDSA_SalesFrloan_refCode_LoansCount(self, request, pk=None):
      if request.GET.get('date'):
          date=request.GET.get('date')
         
          strtDate=date.split(' to ')[0]
          endDate=date.split(' to ')[1]
          date_obj1 = datetime.strptime(strtDate, '%Y-%m-%d').date()
          date_obj2 = datetime.strptime(endDate, '%Y-%m-%d').date()
          
      with ThreadPoolExecutor() as executor:
       if not request.GET.get('date'):
        # print("Not with date")
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(franrefCode=pk).count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(franrefCode=pk).count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(franrefCode=pk).count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(franrefCode=pk).count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(franrefCode=pk).count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(franrefCode=pk).count())
        goldCount=executor.submit(lambda: Goldloanapplication.objects.filter(franrefCode=pk).count())
        otherCount=executor.submit(lambda: otherloans.objects.filter(franrefCode=pk).count())
        creditCount=executor.submit(lambda: CreditDetail.objects.filter(franrefCode=pk).count())
        allInsuranceCount=executor.submit(lambda: AllInsurance.objects.filter(franrefCode=pk).count())
        lifeInsuranceCount=executor.submit(lambda: LifeInsurance.objects.filter(franrefCode=pk).count())
        generalInsuranceCount=executor.submit(lambda: GeneralInsurance.objects.filter(franrefCode=pk).count())
        healthInsuranceCount=executor.submit(lambda: healthInsurance.objects.filter(franrefCode=pk).count())
        
       else:
        
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(franrefCode=pk,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(franrefCode=pk,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(franrefCode=pk,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(franrefCode=pk,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(franrefCode=pk,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(franrefCode=pk,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        goldCount=executor.submit(lambda: Goldloanapplication.objects.filter(franrefCode=pk,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        otherCount=executor.submit(lambda: otherloans.objects.filter(franrefCode=pk,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        creditCount=otherCount=executor.submit(lambda: CreditDetail.objects.filter(franrefCode=pk,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        allInsuranceCount=executor.submit(lambda: AllInsurance.objects.filter(franrefCode=pk,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        lifeInsuranceCount=executor.submit(lambda: LifeInsurance.objects.filter(franrefCode=pk,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        generalInsuranceCount=executor.submit(lambda: GeneralInsurance.objects.filter(franrefCode=pk,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        healthInsuranceCount=executor.submit(lambda: healthInsurance.objects.filter(franrefCode=pk,created_at__gte=date_obj1,created_at__lte=date_obj2).count())
           
      totalCount=businessCount.result()+eduCount.result()+lapCount.result()+perCount.result()+homeCount.result()+carCount.result()+goldCount.result()+otherCount.result()
      totalInsurance=allInsuranceCount.result()+lifeInsuranceCount.result()+generalInsuranceCount.result()+healthInsuranceCount.result()
      return Response({
          'buscount':businessCount.result(),
          'educount':eduCount.result(),
          'lapcount':lapCount.result(),
          'percount':perCount.result(),
          'homecount':homeCount.result(),
          'carcount':carCount.result(),
          'goldcount':goldCount.result(),
          'othercount':otherCount.result(),
          'creditcount':creditCount.result(),
          'totalcount':totalCount,
          'totalInsurances':totalInsurance,
          'allinsurance':allInsuranceCount.result(),
          'lifeinsurance':lifeInsuranceCount.result(),
          'generalinsurance':generalInsuranceCount.result(),
          'healthinsurance':healthInsuranceCount.result(),
          
          }, status=200)
          
    # OverAll Data franchises,dsa's,sales ,customers loans data processing ............
    @action(detail=False, methods=['get'])
    def All_OverAll_LoansCount(self, request):
      if request.GET.get('date'):
          date=request.GET.get('date')
         
          strtDate=date.split(' to ')[0]
          endDate=date.split(' to ')[1]
          date_obj1 = datetime.strptime(strtDate, '%Y-%m-%d').date()
          date_obj2 = datetime.strptime(endDate, '%Y-%m-%d').date()
          
      with ThreadPoolExecutor() as executor:
       if not request.GET.get('date'):
       
        businessCount=executor.submit(lambda: BusinessLoan.objects.all().count())
        eduCount=executor.submit(lambda: Educationalloan.objects.all().count())
        lapCount=executor.submit(lambda: LoanApplication.objects.all().count())
        perCount=executor.submit(lambda: PersonalDetail.objects.all().count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.all().count())
        carCount=executor.submit(lambda: CarLoan.objects.all().count())
        goldCount=executor.submit(lambda: Goldloanapplication.objects.all().count())
        otherCount=executor.submit(lambda: otherloans.objects.all().count())
        creditCount=executor.submit(lambda: CreditDetail.objects.all().count())
        allInsuranceCount=executor.submit(lambda: AllInsurance.objects.all().count())
        lifeInsuranceCount=executor.submit(lambda: LifeInsurance.objects.all().count())
        generalInsuranceCount=executor.submit(lambda: GeneralInsurance.objects.all().count())
        healthInsuranceCount=executor.submit(lambda: healthInsurance.objects.all().count())

       else:
        # print
        businessCount=executor.submit(lambda: BusinessLoan.objects.filter(created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        eduCount=executor.submit(lambda: Educationalloan.objects.filter(created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        lapCount=executor.submit(lambda: LoanApplication.objects.filter(created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        perCount=executor.submit(lambda: PersonalDetail.objects.filter(created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        homeCount=executor.submit(lambda: CustomerProfile.objects.filter(created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        carCount=executor.submit(lambda: CarLoan.objects.filter(created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        goldCount=executor.submit(lambda: Goldloanapplication.objects.filter(created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        otherCount=executor.submit(lambda: otherloans.objects.filter(created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        creditCount=executor.submit(lambda: CreditDetail.objects.filter(created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        allInsuranceCount=executor.submit(lambda: AllInsurance.objects.filter(created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        lifeInsuranceCount=executor.submit(lambda: LifeInsurance.objects.filter(created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        generalInsuranceCount=executor.submit(lambda: GeneralInsurance.objects.filter(created_at__gte=date_obj1,created_at__lte=date_obj2).count())
        healthInsuranceCount=executor.submit(lambda: healthInsurance.objects.filter(created_at__gte=date_obj1,created_at__lte=date_obj2).count())
           
      totalCount=businessCount.result()+eduCount.result()+lapCount.result()+perCount.result()+homeCount.result()+carCount.result()+goldCount.result()+otherCount.result()
      totalInsurance=allInsuranceCount.result()+lifeInsuranceCount.result()+generalInsuranceCount.result()+healthInsuranceCount.result()
      
      return Response({
          'buscount':businessCount.result(),
          'educount':eduCount.result(),
          'lapcount':lapCount.result(),
          'percount':perCount.result(),
          'homecount':homeCount.result(),
          'carcount':carCount.result(),
          'goldcount':goldCount.result(),
          'othercount':otherCount.result(),
          'creditcount':0,
          'totalcount':totalCount,
          'totalInsurances':totalInsurance,
          'allinsurance':allInsuranceCount.result(),
          'lifeinsurance':lifeInsuranceCount.result(),
          'generalinsurance':generalInsuranceCount.result(),
          'healthinsurance':healthInsuranceCount.result(),
          
          }, status=200)

