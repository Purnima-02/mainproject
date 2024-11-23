from rest_framework import serializers

from .models import *



class AllInsuranceSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=AllInsurance
        fields='__all__'
        
        
class LifeInsuranceSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=LifeInsurance
        fields='__all__'
        
        
class HealthInsuranceSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=healthInsurance
        fields='__all__'

class GeneralInsuranceSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=GeneralInsurance
        fields='__all__'