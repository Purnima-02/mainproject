from django.http import JsonResponse
from rest_framework import generics,viewsets,status


from anusha.InsuranceSerializers import AllInsuranceSerializer,LifeInsuranceSerializer,HealthInsuranceSerializer,GeneralInsuranceSerializer
from .models import *
from django.http import HttpResponse
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import action



class AllInsuViewsets(viewsets.ModelViewSet):
    queryset=AllInsurance.objects.all()
    serializer_class=AllInsuranceSerializer
    
    @action(detail=False, methods=['post'])
    def postAllinsurance(self,request):
        mobile_number=request.POST.get('mobile_number')
        default_data = {key: value for key, value in request.data.items() if key not in ['mobile_number', 'csrfmiddlewaretoken']}
        insurance_record, created = AllInsurance.objects.get_or_create(mobile_number=mobile_number,defaults=default_data)
        return Response(status=200) if created else  Response(status=400)
        
class LifeInsuViewsets(viewsets.ModelViewSet):
    queryset=LifeInsurance.objects.all()
    serializer_class=LifeInsuranceSerializer
    
    @action(detail=False, methods=['post'])
    def postlifeinsurance(self,request):
        mobile_number=request.POST.get('mobile_number')
        default_data = {key: value for key, value in request.data.items() if key not in ['mobile_number', 'csrfmiddlewaretoken']}
        insurance_record, created = LifeInsurance.objects.get_or_create(mobile_number=mobile_number,defaults=default_data)
        return Response(status=200) if created else  Response(status=400)
    
    
class GeneralInsuViewsets(viewsets.ModelViewSet):
    queryset=GeneralInsurance.objects.all()
    serializer_class=GeneralInsuranceSerializer
    
    @action(detail=False, methods=['post'])
    def postgeneralinsurance(self,request):
        mobile_number=request.POST.get('mobile_number')
        default_data = {key: value for key, value in request.data.items() if key not in ['mobile_number', 'csrfmiddlewaretoken']}
        insurance_record, created = GeneralInsurance.objects.get_or_create(mobile_number=mobile_number,defaults=default_data)
        
        return Response(status=200) if created else  Response(status=400)

    

class HealthInsuViewsets(viewsets.ModelViewSet):
    queryset=healthInsurance.objects.all()
    serializer_class=HealthInsuranceSerializer
    
    @action(detail=False, methods=['post'])
    def posthealthinsurance(self,request):
        mobile_number=request.POST.get('mobile_number')
        default_data = {key: value for key, value in request.data.items() if key not in ['mobile_number', 'csrfmiddlewaretoken']}
        insurance_record, created = healthInsurance.objects.get_or_create(mobile_number=mobile_number,defaults=default_data)
        return Response(status=200) if created else  Response(status=400)

# bhanu
