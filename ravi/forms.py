from .models import *
from django.utils import timezone
from datetime import timedelta
from django import forms

class plBasicDetailForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the terms and conditions to proceed.'})

    class Meta:
        model=personalbasicdetail
        fields = ['fname', 'lname', 'Dob', 'phone_number', 'pan_num', 
                  'Aadhar_number', 'gender', 'email', 
                  'marital_status', 'required_loan_amount','terms_accepted']
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
            'marital_status':forms.Select(attrs={'class': 'form-control'}),
            'required_loan_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'created_at':forms.DateInput(attrs={'class':'form-control',}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
        }
        error_messages = {
            'fname': {'required': 'Full name is required.'},
            'lname': {'required': 'Full name is required.'},
             
            'pan_num': {'required': 'Pan number is required.'},
            'phone_number':{'required':'mobilenumber is required'},
            
            'Dob': {'required': 'Date of birth is required.'},
            'required_loan_amount': {'required': 'Required loan amount is required.'},
            'terms_accepted': {'required': 'You must accept the terms and conditions to proceed.'},
        }

    def clean_phone_number(self):
        mobile_number = self.cleaned_data.get('phone_number')
        if personalbasicdetail.objects.filter(phone_number=mobile_number).exists():
            record=personalbasicdetail.objects.filter(phone_number=mobile_number).last()
            if date.today() > record.expiry_at:
                return mobile_number
            raise forms.ValidationError("Mobile Number already exist! Please try after 3Months.")
        return mobile_number
    
    def clean_pan_num(self):
        pan_num = self.cleaned_data.get('pan_num')
        if personalbasicdetail.objects.filter(pan_num=pan_num).exists():
            record=personalbasicdetail.objects.filter(pan_num=pan_num).last()
            if date.today() > record.expiry_at:
                return pan_num
            raise forms.ValidationError("PAN Number already exist! Please try after 3Months.")
        return pan_num

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance
class PersonalDetailForm(forms.ModelForm):
   
    class Meta:
        model = PersonalDetail
        fields = '__all__'
        exclude = ['basicdetailform','franrefCode','empref_code','application_id','dsaref_code','application_loan_type','name']
        widgets = {
             'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
             'job_joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

        

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
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



class HomeBasicDetailForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the terms and conditions to proceed.'})

    class Meta:
        model = homebasicdetail
        fields = ['fname', 'lname', 'Dob', 'phone_number', 'pan_num', 
                  'Aadhar_number', 'gender', 'email', 
                  'marital_status', 'required_loan_amount','terms_accepted']
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

            'required_loan_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'created_at':forms.DateInput(attrs={'class':'form-control',}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
        }
        error_messages = {
            'fname': {'required': 'Full name is required.'},
            'lname': {'required': 'Full name is required.'},
             
            'pan_num': {'required': 'Pan number is required.'},
            'phone_number':{'required':'mobilenumber is required'},
            
            'Dob': {'required': 'Date of birth is required.'},
            'required_loan_amount': {'required': 'Required loan amount is required.'},
            'terms_accepted': {'required': 'You must accept the terms and conditions to proceed.'},
        }


    def clean_phone_number(self):
        mobile_number = self.cleaned_data.get('phone_number')
        if homebasicdetail.objects.filter(phone_number=mobile_number).exists():
            record=homebasicdetail.objects.filter(phone_number=mobile_number).last()
            if date.today() > record.expiry_at:
                return mobile_number
            raise forms.ValidationError("Mobile Number already exist! Please try after 3Months.")
        return mobile_number
    
    def clean_pan_num(self):
        pan_num = self.cleaned_data.get('pan_num')
        if homebasicdetail.objects.filter(pan_num=pan_num).exists():
            record=homebasicdetail.objects.filter(pan_num=pan_num).last()
            if date.today() > record.expiry_at:
                return pan_num
            raise forms.ValidationError("PAN Number already exist! Please try after 3Months.")
        return pan_num

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance

class CustomerProfileForm(forms.ModelForm):
 
    class Meta:
        model = CustomerProfile
        fields = '__all__'
        exclude = ['basicdetailhome','mobile_number','franrefCode','empref_code','application_id','dsaref_code','application_loan_type','name','pan_card_number']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'job_joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'business_establishment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'co_applicant_age':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            
        }
        
       





class ApplicantDocumentForm(forms.ModelForm):
    class Meta:
        model = ApplicantDocument
        fields = '__all__'
        exclude = ['applicant_profile']
        widgets = {
            'adhar_card_front': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'adhar_card_back': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'pan_card': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'customer_photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'home_plot_photo_1': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'home_plot_photo_2': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'home_plot_photo_3': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'home_plot_photo_4': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'latest_3_months_banked_statement': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'latest_3_months_payslips_1': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'latest_3_months_payslips_2': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'latest_3_months_payslips_3': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'employee_id_card': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'business_proof_1': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'business_proof_2': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'latest_12_months_banked_statement': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'business_office_photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'latest_3_yrs_itr_1': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'latest_3_yrs_itr_2': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'latest_3_yrs_itr_3': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'current_address_proof': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'existing_loan_statement': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'other_documents_1': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'other_documents_2': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'other_documents_3': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'other_documents_4': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'co_adhar_card_front': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'co_adhar_card_back': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'co_pan_card': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'co_selfie_photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'random_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'adhar_card_front': 'Aadhar Card Front (Image)',
            'adhar_card_back': 'Aadhar Card Back (Image)',
            'pan_card': 'PAN Card (Image)',
            'customer_photo': 'Customer Photo (Image)',
            'home_plot_photo_1': 'Home Plot Photo 1 (Image)',
            'home_plot_photo_2': 'Home Plot Photo 2 (Image)',
            'home_plot_photo_3': 'Home Plot Photo 3 (Image)',
            'home_plot_photo_4': 'Home Plot Photo 4 (Image)',
            'latest_3_months_banked_statement': 'Latest 3 Months Bank Statement (PDF)',
            'latest_3_months_payslips_1': 'Latest 3 Months Payslips 1 (PDF)',
            'latest_3_months_payslips_2': 'Latest 3 Months Payslips 2 (PDF)',
            'latest_3_months_payslips_3': 'Latest 3 Months Payslips 3 (PDF)',
            'employee_id_card': 'Employee ID Card (Image)',
            'business_proof_1': 'Business Proof 1 (Image)',
            'business_proof_2': 'Business Proof 2 (Image)',
            'latest_12_months_banked_statement': 'Latest 12 Months Bank Statement (PDF)',
            'business_office_photo': 'Business Office Photo (Image)',
            'latest_3_yrs_itr_1': 'Latest 3 Years ITR 1 (PDF)',
            'latest_3_yrs_itr_2': 'Latest 3 Years ITR 2 (PDF)',
            'latest_3_yrs_itr_3': 'Latest 3 Years ITR 3 (PDF)',
            'current_address_proof': 'Current Address Proof (Image)',
            'existing_loan_statement': 'Existing Loan Statement (PDF)',
            'other_documents_1': 'Other Documents 1 (PDF)',
            'other_documents_2': 'Other Documents 2 (PDF)',
            'other_documents_3': 'Other Documents 3 (PDF)',
            'other_documents_4': 'Other Documents 4 (PDF)',
            'co_adhar_card_front': 'Co-Applicant Aadhar Card Front (Image)',
            'co_adhar_card_back': 'Co-Applicant Aadhar Card Back (Image)',
            'co_pan_card': 'Co-Applicant PAN Card (Image)',
            'co_selfie_photo': 'Co-Applicant Selfie Photo (Image)',
            
        }


class ApplicationVerificationForm(forms.ModelForm):
   
    class Meta:
        model=ApplicationVerification
        fields='__all__'
        exclude=['personal_detail']

    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
       
        for field in self.fields:
            
            if not getattr(instance, field):
                setattr(instance, field, 'Pending')
        
        if 'Rejected' in self.cleaned_data.values():
            
            for field in self.fields:
                if getattr(instance, field) == 'Pending':
                    setattr(instance, field,'Rejected')
        
        if commit:
            instance.save()
        return instance
    
class HomeapplicationForm(forms.ModelForm):
   
    class Meta:
        model= HomeApplication
        fields='__all__'
        exclude=['applicant_profile']

    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
       
        for field in self.fields:
            
            if not getattr(instance, field):
                setattr(instance, field, 'Pending')
        
        if 'Rejected' in self.cleaned_data.values():
            
            for field in self.fields:
                if getattr(instance, field) == 'Pending':
                    setattr(instance, field,'Rejected')
        
        if commit:
            instance.save()
        return instance



from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=63, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))




class HlDisbursementDetailsForm(forms.ModelForm):
    class Meta:
        model=hldisbursementdetails
        fields='__all__'
        exclude=['verification']



class PlDisbursementDetailsForm(forms.ModelForm):
    class Meta:
        model=pldisbursementdetails
        fields='__all__'
        exclude=['verification']

