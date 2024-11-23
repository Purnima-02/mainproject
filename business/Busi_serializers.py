from rest_framework import serializers

from .models import *



class BusiDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model=BusinessLoanDocument
        fields=['aadhar_card_front']

class BusiApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model=ApplicationVerification
        fields=['verification_status']


class BusiBasicDetailFormSrializer(serializers.ModelSerializer):
    class Meta:
        model=busbasicdetailform
        fields='__all__'
        

class BusiDisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Busdisbursementdetails
        fields='__all__'
        
class BusiSerializer(serializers.ModelSerializer):
    basicdetailform=BusiBasicDetailFormSrializer()
    BussinessLoandocuments=BusiDocumentSerializer()
    applicationverification=BusiApplicationSerializer()
    disbursementdetail=BusiDisbursementSerializer()
    
    class Meta:
        model=BusinessLoan
        fields=['id','name','application_id','basicdetailform','application_loan_type','required_loan_amount','created_at','BussinessLoandocuments','applicationverification','disbursementdetail','dsaref_code','franrefCode','empref_code']
        
    
    def to_representation(self, instance):
        # Get the original serialized data
        data = super().to_representation(instance)
        
        data['verification'] = data.pop('applicationverification')
        data['documents'] = data.pop('BussinessLoandocuments')
        
        return data
    

