from django.contrib import admin

from .models import *

class creditDetailAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'gender', 'date_of_birth', 'mobile_number', 'pan_card_number', 'aadhar_card_number', 
        'marital_status', 'email', 'current_address_pincode', 'aadhar_pincode', 'net_salary', 'company_name',
        'company_type', 'job_joining_date', 'job_location', 'total_job_experience', 'own_house'
    )
    search_fields = ('first_name', 'last_name', 'mobile_number', 'pan_card_number', 'aadhar_card_number', 'email')

class creditDocumentUploadAdmin(admin.ModelAdmin):
    list_display = ('aadhar_card_front', 'aadhar_card_back', 'pan_card', 'customer_photo', 'payslip_1','payslip_2','payslip_3',
                    'bank_statement', 'employee_id_card', 'current_address_proof', 'other_document_1', 'other_document_2',)
    search_fields = ('aadhar_card_front', 'aadhar_card_back', 'pan_card', 'customer_photo', 'payslip_1','payslip_2','payslip_3',
                     'DSA_refferal_code','sales_refferal_code','franchisee_refferal_code')

admin.site.register(CreditDetail, creditDetailAdmin)
admin.site.register(creditDocumentUpload, creditDocumentUploadAdmin)
admin.site.register(credbasicdetailform)


