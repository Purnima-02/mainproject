from rest_framework import serializers
from .models import *



class credbasicdetailformserializers(serializers.ModelSerializer):
    class Meta:
        model=credbasicdetailform
        fields='__all__'


class creditDetailserializers(serializers.ModelSerializer):
    class Meta:
        model=CreditDetail
        fields='__all__'



class creditDocumentUploadserializers(serializers.ModelSerializer):
    class Meta:
        model=creditDocumentUpload
        fields='__all__'

