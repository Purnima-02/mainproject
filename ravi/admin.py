from django.contrib import admin

from .models import *

class PersonalDetailAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'gender', 'date_of_birth', 'mobile_number', 'pan_card_number', 'aadhar_card_number', 
        'marital_status', 'email', 'current_address_pincode', 'aadhar_pincode', 'net_salary', 'company_name',
        'company_type', 'job_joining_date', 'job_location', 'total_job_experience', 'required_loan_amount', 'own_house',)
    
    search_fields = ('first_name', 'last_name', 'mobile_number', 'pan_card_number', 'aadhar_card_number', 'email')

class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ('aadhar_card_front', 'aadhar_card_back', 'pan_card', 'customer_photo', 'payslip_1','payslip_2','payslip_3',
                    'bank_statement', 'employee_id_card', 'current_address_proof', 'other_document_1', 'other_document_2',)
    search_fields = ('aadhar_card_front', 'aadhar_card_back', 'pan_card', 'customer_photo', 'payslip_1','payslip_2','payslip_3',)



class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'loan_type', 'first_name', 'last_name', 'gender', 'date_of_birth',
        'mobile_number', 'pan_card_number', 'aadhar_card_number', 'marital_status',
        'email_id', 'current_address', 'current_address_pincode', 'aadhar_address', 
        'aadhar_pincode', 'running_emis_per_month', 'income_source', 'net_salary_per_month',
        'company_name', 'company_type', 'job_joining_date', 'job_location', 'total_job_experience',
        'work_email',  'net_income_per_month', 'business_name', 
        'business_type', 'business_establishment_date',  'gst_number', 
        'mother_name', 'father_name', 'nature_of_business', 'turnover_per_year', 
        'business_address_pincode', 'house_plot_purchase_value', 'required_loan_amount', 
         'existing_loan_bank_nbfc_name', 'existing_loan_amount', 
        'ref1_person_name', 'ref2_person_name','co_applicant_first_name','co_applicant_last_name','co_applicant_mobile_number',
        'co_applicant_email_id','co_applicant_occupation','co_applicant_net_income_per_month',)
    

    search_fields = ('first_name', 'last_name', 'pan_card_number', 'aadhar_card_number')
   



class ApplicantDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'adhar_card_front', 'adhar_card_back', 'pan_card', 'customer_photo', 'home_plot_photo_1', 'home_plot_photo_2', 'home_plot_photo_3', 'home_plot_photo_4', 
                       'latest_3_months_banked_statement', 'latest_3_months_payslips_1', 'latest_3_months_payslips_2', 
                       'latest_3_months_payslips_3', 'employee_id_card', 'business_proof_1', 'business_proof_2', 'latest_12_months_banked_statement', 
                       'business_office_photo', 'latest_3_yrs_itr_1', 'latest_3_yrs_itr_2', 'latest_3_yrs_itr_3', 
                       'current_address_proof','existing_loan_statement', 'other_documents_1', 'other_documents_2', 
                       'other_documents_3', 'other_documents_4','co_adhar_card_front', 'co_adhar_card_back', 'co_pan_card', 'co_selfie_photo')
      # Adjust filters based on your requirements
    search_fields = ('id','adhar_card_front', 'adhar_card_back', 'pan_card', 'customer_photo', 'home_plot_photo_1', 'home_plot_photo_2', 'home_plot_photo_3', 'home_plot_photo_4',)

    fieldsets = (
        (None, {
            'fields': ('applicant_profile',)
        }),
        ('Common Fields', {
            'fields': ('adhar_card_front', 'adhar_card_back', 'pan_card', 'customer_photo', 'home_plot_photo_1', 'home_plot_photo_2', 'home_plot_photo_3', 'home_plot_photo_4', 
                       'latest_3_months_banked_statement', 'latest_3_months_payslips_1', 'latest_3_months_payslips_2', 
                       'latest_3_months_payslips_3', 'employee_id_card'),
            'classes': ('collapse',)
        }),
        ('HLBT Fields', {
            'fields': ('business_proof_1', 'business_proof_2', 'latest_12_months_banked_statement', 
                       'business_office_photo', 'latest_3_yrs_itr_1', 'latest_3_yrs_itr_2', 'latest_3_yrs_itr_3', 
                       'current_address_proof'),
            'classes': ('collapse',)
        }),
        ('Business Fields', {
            'fields': ('existing_loan_statement', 'other_documents_1', 'other_documents_2', 
                       'other_documents_3', 'other_documents_4'),
            'classes': ('collapse',)
        }),
        ('Co-Applicant Details', {
            'fields': ('co_adhar_card_front', 'co_adhar_card_back', 'co_pan_card', 'co_selfie_photo'),
            'classes': ('collapse',)
        }),
    )

class ApplicationVerificationAdmin(admin.ModelAdmin):
    list_display = [ 'personal_detail_verification', 'documents_upload_verification', 
                    'documents_verification', 'eligibility_check_verification', 
                    'bank_login_verification', 'kyc_and_document_verification', 
                    'enach_verification', 'disbursement_verification', 'verification_status']
    list_filter = ['verification_status']

class HomHomeApplicationeAdmin(admin.ModelAdmin):
    list_display =['documents_upload_status','kyc_documents_verification_status',
        'filed_officer_visit_inspection_status','eligibility_check_status','application_fee_paid_status',
        'tele_verification_status','bank_login_fee_paid_status','bank_login_done_status','credit_manager_visit_status',
        'bank_nbfc_soft_loan_sanction_letter_issued_status','legal_technical_completed_status','final_loan_sanctioned_status',
        'agreement_signatures_done_status','enach_auto_debit_done_status','disbursement_status','post_documentation_mortgage_status',
        'cheque_issued_loan_amount_credited_status']
    
    list_filter = ['documents_upload_status', 'kyc_documents_verification_status'] 








admin.site.register(homebasicdetail)
admin.site.register(personalbasicdetail)
admin.site.register(HomeApplication, HomHomeApplicationeAdmin)
admin.site.register(ApplicationVerification, ApplicationVerificationAdmin)
admin.site.register(ApplicantDocument, ApplicantDocumentAdmin)
admin.site.register(PersonalDetail, PersonalDetailAdmin)
admin.site.register(DocumentUpload, DocumentUploadAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(hldisbursementdetails)
admin.site.register(pldisbursementdetails)