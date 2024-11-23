from rest_framework import serializers
from .models import *
class hlbasicdetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=homebasicdetail
        fields='__all__'

class hldocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=ApplicantDocument
        fields='__all__'

class hlverificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=HomeApplication
        fields='__all__'
class hldisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model=hldisbursementdetails
        fields='__all__'

class hlApplicationSerializer(serializers.ModelSerializer):
    basicdetailhome=hlbasicdetailSerializer()
    hldocument=hldocumentSerializer()
    applicationverification=hlverificationSerializer()
    disbursementdetail=hldisbursementSerializer()
    class Meta:
        model=CustomerProfile
        fields=['id','name','application_id','application_loan_type','required_loan_amount','created_at','applicationverification','hldocument','basicdetailhome','disbursementdetail','dsaref_code','franrefCode','empref_code']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['verification'] = data.pop('applicationverification')
        data['documents'] = data.pop('hldocument')
        return data

class plbasicSerializer(serializers.ModelSerializer):
    class Meta:
        model=personalbasicdetail
        fields='__all__'

class pldocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=DocumentUpload
        fields='__all__'

class plverificationSrializer(serializers.ModelSerializer):
    class Meta:
        model=ApplicationVerification
        fields='__all__'

class pldisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model=pldisbursementdetails
        fields='__all__'

class plApplicationSerializer(serializers.ModelSerializer):
    basicdetailform=plbasicSerializer()
    pldocument=pldocumentSerializer()
    applicationverification=plverificationSrializer()
    disbursementdetail=pldisbursementSerializer()
    
    class Meta:
        model=PersonalDetail
        fields=['id','name','application_id','application_loan_type','required_loan_amount','created_at','applicationverification','pldocument','basicdetailform','disbursementdetail','dsaref_code','franrefCode','empref_code']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['verification'] = data.pop('applicationverification')
        data['documents'] = data.pop('pldocument')
        return data

