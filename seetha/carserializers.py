from rest_framework import serializers
from .models import *

class CLBasicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=CLBasicDetail
        fields='__all__'



        
class CarLoanDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarLoanDocument
        fields = '__all__'

class CarApplicationVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarApplicationVerification
        fields = '__all__'

class carDisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model=CarDisbursementDetails
        fields='__all__'

class CarLoanSerializer(serializers.ModelSerializer):
    applicationverification=CarApplicationVerificationSerializer()
    CarLoandocuments=CarLoanDocumentSerializer()
    applicationverification=CarApplicationVerificationSerializer()
    disbursementdetail=carDisbursementSerializer()
    class Meta:
        model = CarLoan
        fields=['id','name','application_id','application_loan_type','required_loan_amount','created_at','applicationverification','CarLoandocuments','disbursementdetail','dsaref_code','franrefCode','empref_code']
        
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['verification'] = data.pop('applicationverification')
        data['documents'] = data.pop('CarLoandocuments')
        return data