from rest_framework import serializers
from .models import *


class BasicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=basicdetailform
        fields='__all__'



class LapDocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = lapDocumentUpload
        fields = '__all__'

class DisbursementDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = disbursementdetails
        fields = '__all__'


class LapApplicationVerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = lapApplicationVerification
        fields = '__all__'



class LoanApplicationSerializer(serializers.ModelSerializer):
    basic_detail = BasicDetailSerializer()
    lapdocument = LapDocumentUploadSerializer()
    applicationverification = LapApplicationVerificationSerializer()
    disbursementdetail=DisbursementDetailsSerializer()
    class Meta:
        model = LoanApplication
        fields=['id','name','basic_detail','application_id','application_loan_type','required_loan_amount','created_at','applicationverification','lapdocument','disbursementdetail','applicationverification','dsaref_code','franrefCode','empref_code']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['verification'] = data.pop('applicationverification')
        data['documents'] = data.pop('lapdocument')
        return data

class goldbasicdetailSerializer(serializers.ModelSerializer):               
    class Meta:
        model=goldbasicdetailform
        fields='__all__'

class goldapplicationSerializer(serializers.ModelSerializer):
    goldbasicdetail=goldbasicdetailSerializer()
    class Meta:
        model=Goldloanapplication
        fields='__all__'

class otherbasicdetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=otherbasicdetailform
        fields='__all__'

class otherloanSerializer(serializers.ModelSerializer):
    otherbasicdetail=otherbasicdetailSerializer()
    class Meta:
        model=otherloans
        fields='__all__'

class dsaSerializer(serializers.ModelSerializer):
    class Meta:
        model=dsa
        fields='__all__'

        

class franchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model=franchise
        fields='__all__'

