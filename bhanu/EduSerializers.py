from rest_framework import serializers

from .models import *


class EduDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model=Educationloan_document_upload
        fields=['adhar_card_front']

class EduApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model=ApplicationVerification
        fields=['verification_status']

class edubasicdetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=edubasicdetailform
        fields='__all__'

class eduDisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Edudisbursementdetails
        fields='__all__'



class EduSerializer(serializers.ModelSerializer):
    basicdetailform=edubasicdetailSerializer()
    personal_details =  EduDocumentSerializer()
    applicationverification = EduApplicationSerializer()
    disbursementdetail=eduDisbursementSerializer()

    class Meta:
        model=Educationalloan
        fields=['id','name','application_id','application_loan_type','required_loan_amount','created_at','applicationverification','personal_details','disbursementdetail','dsaref_code','franrefCode','empref_code','basicdetailform']
        
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['verification'] = data.pop('applicationverification')
        data['documents'] = data.pop('personal_details')
        return data