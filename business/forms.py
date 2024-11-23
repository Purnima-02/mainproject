# forms.py
from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import date



class BusinessLoanForm(forms.ModelForm):
   

    class Meta:
        model = BusinessLoan
        fields = '__all__'
        exclude = ['application_id','loan_type','name','created_at','basicdetailform']
        labels={

            'dsaref_code':'DSA Referal Code(Optional)',
            'franrefCode':'Franchise Referal Code(Optional)',
            'total_job_experience':'Total Job Experience(IN MONTHS)',
        }
       
        widgets = {
            
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'business_establishment_date': forms.DateInput(attrs={'type': 'date'}),
            'mobile_number':forms.NumberInput(attrs={'pattern':'[0-9]'}),
            'pan_card_number': forms.TextInput(attrs={'pattern': '[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}'}),
            'ref1mobilenumber': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'ref2mobilenumber': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'aadhar_card_number':forms.NumberInput(),
            'turnover_in_lakhs_per_year': forms.NumberInput(attrs={'pattern':'[0-9]','placeholder': '₹ Enter amount'}),
            'required_loan_amount': forms.NumberInput(attrs={'pattern':'[0-9]','placeholder': '₹ Enter amount'}),
           
            
        }
        
    
# Mobile Numbers Validation
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if BusinessLoan.objects.filter(mobile_number=mobile_number).exclude(id=self.instance_id).exists():
            record=busbasicdetailform.objects.filter(phone_number=mobile_number).last()
            if date.today() > record.expiry_at:
                return mobile_number
            raise forms.ValidationError("Mobile number already exist!.")
        if len(mobile_number)!=10:
            raise forms.ValidationError("Mobile NUmber Length should be in 10 Digits")
        return mobile_number
    
    def clean_pan_card_number(self):
        pan_card_number = self.cleaned_data.get('pan_card_number')
        if BusinessLoan.objects.filter(pan_card_number=pan_card_number).exclude(id=self.instance_id).exists():
            record=busbasicdetailform.objects.filter(pan_num=pan_card_number).last()
            if date.today() > record.expiry_at:
                return pan_card_number
            raise forms.ValidationError("PAN number already exist!.")
    
    
    def clean_aadhar_card_number(self):
        aadhar_card_number=self.cleaned_data.get('aadhar_card_number')
        if len(aadhar_card_number)!=12:
            raise forms.ValidationError("Aadhar Number Length should be in 10 Digits")
        return aadhar_card_number
    
    def __init__(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id', None)
        kwargs.pop('instance_id', None) 
        super().__init__(*args, **kwargs)
      

from django.utils.translation import gettext_lazy as _

class BusinessLoanDocumentForm(forms.ModelForm):
    class Meta:
        model = BusinessLoanDocument
        fields = '__all__'
        exclude = ['loan']
        widgets={

          'business_proof_1': forms.FileInput(attrs={'accept': '.pdf'}),
          'business_proof_2': forms.FileInput(attrs={'accept': '.pdf'}),
          'latest_12_months_bank_statement': forms.FileInput(attrs={'accept': '.pdf'}),
          'bank_statement': forms.FileInput(attrs={'accept': '.pdf'}),
          'latest_3_yrs_itr_1': forms.FileInput(attrs={'accept': '.pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document'}),
          'latest_3_yrs_itr_2': forms.FileInput(attrs={'accept': '.pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document'}),
          'latest_3_yrs_itr_3': forms.FileInput(attrs={'accept': '.pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document'}),
          'current_address_proof': forms.FileInput(attrs={'accept': '.pdf'}),
          'bank_statement': forms.FileInput(attrs={'accept': '.pdf'}),
          'other_document_1': forms.FileInput(attrs={'accept': '.pdf'}),
          'other_document_2': forms.FileInput(attrs={'accept': '.pdf'}),


          'aadhar_card_front': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'aadhar_card_back': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'pan_card': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'customer_photo': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'business_office_photo': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),

         'co_applicant_aadharFront': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'co_applicant_aadharBack': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'co_applicant_panCard': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'co_applicant_photo': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
        }
        labels = {
            'aadhar_card_front': 'Aadhar Card Front (JPEG/PNG)',
            'aadhar_card_back': 'Aadhar Card Back (JPEG/PNG)',
            'pan_card': 'PAN Card (JPEG/PNG)',
            'customer_photo': 'Customer Photo (JPEG/PNG)',
            'business_proof_1': 'Business Proof 1 (PDF)',
            'business_proof_2': 'Business Proof 2 (PDF)',
            'latest_12_months_bank_statement': 'Latest 12 Months Bank Statement (PDF)',
            'business_office_photo': 'Business Office Photo (JPEG/PNG)',
            'latest_3_yrs_itr_1': 'Latest 3 Years ITR 1 (PDF)',
            'latest_3_yrs_itr_2': 'Latest 3 Years ITR 2 (PDF)',
            'latest_3_yrs_itr_3': 'Latest 3 Years ITR 3 (PDF)',
            'current_address_proof': 'Current Address Proof(RENTAL AGRSEEMENT/ CURRENT BILL/ GAS BILL/WIFI BILL) (PDF)',
            'other_document_1': 'Other Document 1 (PDF)',
            'other_document_2': 'Other Document 2 (PDF)',
        }

    def clean_aadhar_card_front(self):
        file = self.cleaned_data.get('aadhar_card_front', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png') :
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file

    def clean_aadhar_card_back(self):
        file = self.cleaned_data.get('aadhar_card_back', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file

    def clean_pan_card(self):
        file = self.cleaned_data.get('pan_card', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file

    def clean_customer_photo(self):
        file = self.cleaned_data.get('customer_photo', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file

    def clean_business_proof_1(self):
        file = self.cleaned_data.get('business_proof_1', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_business_proof_2(self):
        file = self.cleaned_data.get('business_proof_2', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_latest_12_months_bank_statement(self):
        file = self.cleaned_data.get('latest_12_months_bank_statement', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_business_office_photo(self):
        file = self.cleaned_data.get('business_office_photo', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file

    def clean_latest_3_yrs_itr_1(self):
        file = self.cleaned_data.get('latest_3_yrs_itr_1', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_latest_3_yrs_itr_2(self):
        file = self.cleaned_data.get('latest_3_yrs_itr_2', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_latest_3_yrs_itr_3(self):
        file = self.cleaned_data.get('latest_3_yrs_itr_3', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_current_address_proof(self):
        file = self.cleaned_data.get('current_address_proof', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_other_document_1(self):
        file = self.cleaned_data.get('other_document_1', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_other_document_2(self):
        file = self.cleaned_data.get('other_document_2', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file
    

class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = '__all__'


class ApplicationVerifyForm(forms.ModelForm):
    class Meta:
        model=ApplicationVerification
        fields='__all__'
        exclude=['loan']

    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
       
        for field in self.fields:
            
            if not getattr(instance, field):
                setattr(instance, field, 'Pending')
        
        if 'Rejected' in self.cleaned_data.values():
            for field in self.fields:
                if getattr(instance, field) == 'Pending':
                    setattr(instance, field, 'Rejected')
        
        if commit:
            instance.save()
        return instance

class busBasicDetailForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the terms and conditions to proceed.'})

    class Meta:
        model = busbasicdetailform
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
                
            }),             'Aadhar_number':forms.TextInput(attrs={'class':'form-control'}),
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
        if busbasicdetailform.objects.filter(phone_number=mobile_number).exists():
            record=busbasicdetailform.objects.filter(phone_number=mobile_number).last()
            if date.today() > record.expiry_at:
                return mobile_number
            raise forms.ValidationError("Mobile Number already exist! Please try after 3Months.")
        return mobile_number
    
    def clean_pan_num(self):
        pan_num = self.cleaned_data.get('pan_num')
        if busbasicdetailform.objects.filter(pan_num=pan_num).exists():
            record=busbasicdetailform.objects.filter(pan_num=pan_num).last()
            if date.today() > record.expiry_at:
                return pan_num
            raise forms.ValidationError("PAN Number already exist! Please try after 3Months.")
        return pan_num

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance

class BusDisbursementDetailsForm(forms.ModelForm):
    class Meta:
        model=Busdisbursementdetails
        fields='__all__'
        exclude=['verification']