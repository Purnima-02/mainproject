from .models import *
from django.utils import timezone
from datetime import timedelta
from django import forms



class creditBasicDetailForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the terms and conditions to proceed.'})

    class Meta:
        model = credbasicdetailform
        fields = '__all__'
       
        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control'}),
            'lname': forms.TextInput(attrs={'class': 'form-control'}),
            'pan_num': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'maxlength': '10',
                'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57',
                'min': '0',
                
            }),   
            'Aadhar_number':forms.TextInput(attrs={'class':'form-control'}),
            'Dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),

            'created_at':forms.DateInput(attrs={'class':'form-control',}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
        
            'existing_creditcard_holder':forms.Select(attrs={'class': 'form-control'}),
            'card_limit': forms.TextInput(attrs={'class': 'form-control'}),
            'card_belonging_bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
        
        error_messages = {
            'fname': {'required': 'Full name is required.'},
            'lname': {'required': 'Full name is required.'},
             
            'pan_num': {'required': 'Pan number is required.'},
            'phone_number':{'required':'mobilenumber is required'},
            
            'Dob': {'required': 'Date of birth is required.'},
            'terms_accepted': {'required': 'You must accept the terms and conditions to proceed.'},
        }


    def clean_phone_number(self):
        mobile_number = self.cleaned_data.get('phone_number')
        if credbasicdetailform.objects.filter(phone_number=mobile_number).exists():
            record=credbasicdetailform.objects.filter(phone_number=mobile_number).last()
            if date.today() > record.expiry_at:
                return mobile_number
            raise forms.ValidationError("Mobile Number already exist! Please try after 3Months.")
        return mobile_number
    
    def clean_pan_num(self):
        pan_num = self.cleaned_data.get('pan_num')
        if credbasicdetailform.objects.filter(pan_num=pan_num).exists():
            record=credbasicdetailform.objects.filter(pan_num=pan_num).last()
            if date.today() > record.expiry_at:
                return pan_num
            raise forms.ValidationError("PAN Number already exist! Please try after 3Months.")
        return pan_num

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance
    



class CreditDetailForm(forms.ModelForm):
    class Meta:
        model = CreditDetail
        fields = [
            'first_name', 'last_name', 'gender', 'father_name', 'date_of_birth', 'mobile_number', 
            'pan_card_number', 'aadhar_card_number', 'marital_status', 'email', 'current_address', 
            'current_address_pincode', 'aadhar_address', 'aadhar_pincode', 'running_emis', 'net_salary', 
            'company_name', 'company_type', 'job_joining_date', 'job_location', 'total_job_experience', 
            'work_email', 'office_address', 'office_address_pincode', 'ref1_name', 'ref1_mobile', 
            'ref2_name', 'ref2_mobile', 'own_house'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'placeholder': 'Father\'s Name'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Mobile Number', 'pattern': '[0-9]{10}'}),
            'pan_card_number': forms.TextInput(attrs={'placeholder': 'PAN Card Number'}),
            'aadhar_card_number': forms.TextInput(attrs={'placeholder': 'Aadhar Card Number'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'current_address': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Current Address'}),
            'current_address_pincode': forms.TextInput(attrs={'placeholder': 'Pincode'}),
            'aadhar_address': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Aadhar Address'}),
            'aadhar_pincode': forms.TextInput(attrs={'placeholder': 'Pincode'}),
            'running_emis': forms.TextInput(attrs={'placeholder': 'Running EMIs'}),
            'net_salary': forms.TextInput(attrs={'placeholder': 'Net Salary'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Company Name'}),
            'company_type': forms.Select(attrs={'class': 'form-control'}),
            'job_joining_date': forms.DateInput(attrs={'type': 'date'}),
            'job_location': forms.TextInput(attrs={'placeholder': 'Job Location'}),
            'total_job_experience': forms.NumberInput(attrs={'placeholder': 'Total Job Experience'}),
            'work_email': forms.EmailInput(attrs={'placeholder': 'Work Email'}),
            'office_address': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Office Address'}),
            'office_address_pincode': forms.TextInput(attrs={'placeholder': 'Pincode'}),
            'ref1_name': forms.TextInput(attrs={'placeholder': 'Reference 1 Name'}),
            'ref1_mobile': forms.TextInput(attrs={'placeholder': 'Reference 1 Mobile', 'pattern': '[0-9]{10}'}),
            'ref2_name': forms.TextInput(attrs={'placeholder': 'Reference 2 Name'}),
            'ref2_mobile': forms.TextInput(attrs={'placeholder': 'Reference 2 Mobile', 'pattern': '[0-9]{10}'}),
            'own_house': forms.Select(attrs={'class': 'form-control'}),
            
        }
























class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = creditDocumentUpload
        fields = ['aadhar_card_front', 'aadhar_card_back', 'pan_card', 'customer_photo', 'payslip_1',
                  'payslip_2', 'payslip_3', 'bank_statement', 'employee_id_card', 'current_address_proof',
                  'other_document_1', 'other_document_2']
        widgets = {
            'aadhar_card_front': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'aadhar_card_back': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'pan_card': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'customer_photo': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'payslip_1': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'payslip_2': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'payslip_3': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'bank_statement': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'employee_id_card': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'current_address_proof': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'other_document_1': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'other_document_2': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
        }
        labels = {
            'aadhar_card_front': 'Aadhar Card Front (Image)',
            'aadhar_card_back': 'Aadhar Card Back (Image)',
            'pan_card': 'PAN Card (Image)',
            'customer_photo': 'Customer Photo (Image)',
            'payslip_1': 'Payslip 1 (PDF)',
            'payslip_2': 'Payslip 2 (PDF)',
            'payslip_3': 'Payslip 3 (PDF)',
            'bank_statement': 'Bank Statement (PDF)',
            'employee_id_card': 'Employee ID Card (Image)',
            'current_address_proof': 'Current Address Proof (Image)',
            'other_document_1': 'Other Document 1 (PDF)',
            'other_document_2': 'Other Document 2 (PDF)',
}
