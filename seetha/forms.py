from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.db.models import Q
# from decimal import Decimal
import re

from .models import CarLoan

class CarLoanForm(forms.ModelForm):
    # random_number = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = CarLoan
        fields = '__all__'
        exclude=['application_id','carbasic_detail','franrefCode','empref_code','dsaref_code','application_loan_type','name']

      

        
        widgets = {
            
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email_id': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_number':forms.NumberInput(attrs={'pattern': r'^\d{10}$',}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'car_loan_type': forms.Select(attrs={'id': 'id_car_loan_type'}),
            'income_source': forms.Select(attrs={'id': 'id_income_source'}),
            'car_vehicle_no': forms.TextInput(attrs={'pattern': r'^[A-Z]{2}\d{1,2}[A-Z]{1,2}\d{4}$'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'work_email': forms.EmailInput(attrs={}),
            'job_joining_date': forms.DateInput(attrs={'type': 'date'}),
            'total_job_experience': forms.NumberInput(attrs={'pattern': r'^\d{2}$'}),
            'business_establishment_date': forms.DateInput(attrs={'type': 'date'}),
            'pan_card_number': forms.TextInput(attrs={ 'pattern': r'^[A-Z]{5}\d{4}[A-Z]$'}),
            'aadhar_card_number':forms.NumberInput(),
            'current_address': forms.Textarea(attrs={'class': 'form-control'}),
            'aadhar_address': forms.Textarea(attrs={'class': 'form-control'}),
            'current_address_type': forms.Select(attrs={'class': 'form-control'}),
            'aadhar_address_type': forms.Select(attrs={'class': 'form-control'}),
            'aadhar_pincode': forms.NumberInput(attrs={'pattern': r'^\d{6}$'}),
            'current_address_pincode': forms.NumberInput(attrs={'pattern': r'^\d{6}$'}),
            'net_salary_per_month': forms.NumberInput(attrs={'class': 'form-control'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_address_pincode': forms.NumberInput(attrs={'pattern': r'^\d{6}$'}),
            'net_income_per_month': forms.NumberInput(attrs={'class': 'form-control'}),
            'gst_certificate': forms.Select(attrs={'id': 'id_gst_certificate'}),
            'gst_number': forms.TextInput(attrs={'pattern': r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$'}),
            'existing_loan': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'existing_loan_bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'existing_loan_amount_in_rs':forms.NumberInput(attrs={'class': 'form-control'}),
            'ref1_person_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ref_1_person_mobile_number':forms.NumberInput(attrs={'pattern': r'^\d{10}$'}),
            'ref2_person_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ref_2_person_mobile_number':forms.NumberInput(attrs={'pattern': r'^\d{10}$'}),
            'dsaref_code': forms.TextInput(attrs={'class': 'form-control'}),
            'franrefCode': forms.TextInput(attrs={'class': 'form-control'}),
            'empref_code': forms.TextInput(attrs={'class': 'form-control'}),
            'required_loan_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'quotation_value_on_ex_showroom': forms.NumberInput(attrs={'class': 'form-control'}),
            'downpayment_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'showroom_quotation': forms.NumberInput(attrs={'class': 'form-control'}),
        }




    def __init__(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id', None)
        kwargs.pop('instance_id', None) 
        super(CarLoanForm, self).__init__(*args, **kwargs)

    def clean_aadhar_card_number(self):
        aadhar = self.cleaned_data.get('aadhar_card_number')
        if not aadhar.isdigit():
            raise forms.ValidationError("Aadhaar number must contain only digits.")
        if len(aadhar) != 12:
            raise forms.ValidationError("Aadhaar number must be exactly 12 digits long.")
        return aadhar

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if mobile_number:
            mobile_number_str = str(mobile_number)
            if not re.match(r'^\d{10}$', mobile_number_str):
                raise forms.ValidationError("Mobile number must be exactly 10 digits.")
        return mobile_number

    def clean_email_id(self):
        email = self.cleaned_data.get('email_id')
        if email and not re.match(r'^[a-zA-Z]', email):
            raise ValidationError("Email must start with an alphabet.")
        return email
    
    
    def clean_work_email(self):
        work_email = self.cleaned_data.get('work_email')
        if work_email and not re.match(r'^[a-zA-Z]', work_email):
            raise ValidationError("Work email must start with an alphabet.")

        return work_email
    
    
    def clean_gst_number(self):
        gst_number = self.cleaned_data.get('gst_number')
        if gst_number and not re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$', gst_number):
            raise ValidationError("Invalid GST number format.")
    
        return gst_number
 
    def clean_ref_1_person_mobile_number(self):
        ref_1_mobile = self.cleaned_data.get('ref_1_person_mobile_number')
        if ref_1_mobile:
            if len(ref_1_mobile) != 10 or not ref_1_mobile.isdigit():
                raise forms.ValidationError("Reference 1 mobile number must be exactly 10 digits.")
        return ref_1_mobile
     
    
    def clean_ref_2_person_mobile_number(self):
        ref_2_mobile = self.cleaned_data.get('ref_2_person_mobile_number')
        if ref_2_mobile:
            if len(ref_2_mobile) != 10 or not ref_2_mobile.isdigit():
                raise forms.ValidationError("Reference 2 mobile number must be exactly 10 digits.")
        return ref_2_mobile
    

    def clean_pan_card(self):
        pan_card = self.cleaned_data.get('pan_card')
        if pan_card and not re.match(r'^[A-Z]{5}\d{4}[A-Z]$', pan_card):
            raise forms.ValidationError("PAN card number must be in the correct format (e.g., ABCDE1234F).")
        return pan_card
    

    def clean_total_job_experience(self):
        total_job_experience = self.cleaned_data.get('total_job_experience')
        if total_job_experience is not None:
            total_job_experience_str = str(total_job_experience).zfill(2)
            if not re.match(r'^\d{2}$', total_job_experience_str):
                raise forms.ValidationError("Total job experience must be exactly 2 digits.")
        return total_job_experience
    

    
        
    def clean_model_year(self):
        model_year = self.cleaned_data.get('model_year')
        
        # Ensure the model_year is exactly 4 digits and numeric
        if model_year and not re.match(r'^\d{4}$', str(model_year)):
            raise forms.ValidationError("Model year must be exactly a 4-digit number.")
        
        return model_year
    
    def clean_car_model_year(self):
        car_model_year = self.cleaned_data.get('car_model_year')
        
        # Ensure the model_year is exactly 4 digits and numeric
        if car_model_year and not re.match(r'^\d{4}$', str(car_model_year)):
            raise forms.ValidationError("Model year must be exactly a 4-digit number.")
        
        return car_model_year


    def clean_car_vehicle_no(self):
        vehicle_no = self.cleaned_data.get('car_vehicle_no')
        if vehicle_no and not re.match(r'^[A-Z]{2}\d{1,2}[A-Z]{1,2}\d{4}$', vehicle_no):
            raise forms.ValidationError("Car vehicle number must be in the correct format (e.g., MH12AB1234 or KA01C5678).")
        return vehicle_no
       
    def clean_current_address(self):
        current_address = self.cleaned_data['current_address']
        # Custom validation logic to ensure both numbers and alphabets are present
        if not re.search(r'[A-Za-z]', current_address) or not re.search(r'[0-9]', current_address):
            raise forms.ValidationError("Current address must contain both numbers and alphabets.")
        return current_address

    def clean_aadhar_address(self):
        aadhar_address = self.cleaned_data['aadhar_address']
        # Custom validation logic to ensure both numbers and alphabets are present
        if not re.search(r'[A-Za-z]', aadhar_address) or not re.search(r'[0-9]', aadhar_address):
            raise forms.ValidationError("Aadhaar address must contain both numbers and alphabets.")
        return aadhar_address
    

    def clean_aadhar_pincode(pincode):
        if len(str(pincode)) != 6 or not str(pincode).isdigit():
           raise ValidationError('Pincode must be exactly 6 digits.')

    def clean_aadhar_pincode(self):
        aadhar_pincode = self.cleaned_data.get('aadhar_pincode')
        if aadhar_pincode:
            aadhar_pincode_str = str(aadhar_pincode)
            if not re.match(r'^\d{6}$', aadhar_pincode_str):
                raise forms.ValidationError("Aaadhar Pincode must be a 6-digit number.")
        return aadhar_pincode
    
    def clean_current_address_pincode(self):
        current_address_pincode = self.cleaned_data.get('current_address_pincode')
        if current_address_pincode:
            current_address_pincode_str = str(current_address_pincode)
            if not re.match(r'^\d{6}$', current_address_pincode_str):
                raise forms.ValidationError("Current address pincode must be a 6-digit number.")
        return current_address_pincode
    

    def clean_business_address_pincode(self):
        business_address_pincode = self.cleaned_data.get('current_address_pincode')
        if business_address_pincode:
            current_address_pincode_str = str(business_address_pincode)
            if not re.match(r'^\d{6}$', current_address_pincode_str):
                raise forms.ValidationError("Current address pincode must be a 6-digit number.")
        return business_address_pincode


from django.utils.translation import gettext_lazy as _

class CarLoanDocumentForm(forms.ModelForm):
    class Meta:
        model = CarLoanDocument
        fields = '__all__'
        exclude = ['loan']
        labels = {
            
            'car_rc_front': 'Car Rc Front(JPEG)',
            'car_rc_back': 'Car Rc Back (JPEG)',
            'aadhaar_card_front': 'Aadhar Card Front (JPEG)',
            'aadhaar_card_back': 'Aadhar Card Back (JPEG)',
            'pan_card': 'PAN Card (JPEG)',
            'customer_photo': 'Customer Photo (JPEG)',
            'payslip1': 'Payslip 1 (PDF)',
            'payslip2': 'Payslip 2 (PDF), (Optional)',
            'payslip3': 'Payslip 3 (PDF),(Optional)',
            'bank_statement': 'Bank Statement (PDF)',
            'employee_id_card': 'Employee ID Card (JPEG),(Optional)',
            'business_proof_1': 'Business Proof 1 (PDF)',
            'business_proof_2': 'Business Proof 2 (PDF),(Optional)',
            'latest_12_months_bank_statement': 'Latest 12 Months Bank Statement (PDF)',
            'business_office_photo': 'Business Office Photo (JPEG)',
            'latest_3_yrs_itr_1': 'Latest 3 Years ITR 1 (PDF)',
            'latest_3_yrs_itr_2': 'Latest 3 Years ITR 2 (PDF)',
            'latest_3_yrs_itr_3': 'Latest 3 Years ITR 3 (PDF),(Optional)',
            'current_address_proof': 'Current Address Proof (PDF),(Optional)',
            'existing_loan_statement': 'Existing Loan Statement (PDF)',
            'other_document_1': 'Other Document 1 (PDF),(Optional)',
            'other_document_2': 'Other Document 2 (PDF),(Optional)',
            
        }


    def __init__(self, *args, **kwargs):
        super(CarLoanDocumentForm, self).__init__(*args, **kwargs)
        self.fields['payslip3'].required = False
        self.fields['employee_id_card'].required = False


    def clean_car_rc_front(self):
        file = self.cleaned_data.get('car_rc_front', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG/PNG files are allowed.'), code='invalid')
        return file


    def clean_car_rc_back(self):
        file = self.cleaned_data.get('car_rc_back', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG/PNG files are allowed.'), code='invalid')
        return file
    

    def clean_aadhaar_card_front(self):
        file = self.cleaned_data.get('aadhaar_card_front', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file
    

    def clean_aadhaar_card_back(self):
        file = self.cleaned_data.get('aadhaar_card_back', False)
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
    

    def clean_payslip1(self):
        file = self.cleaned_data.get('payslip1', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file


    def clean_payslip2(self):
        file = self.cleaned_data.get('payslip2', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file


    def clean_payslip3(self):
        file = self.cleaned_data.get('payslip3', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file
    

    def clean_bank_statement(self):
        file = self.cleaned_data.get('bank_statement', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file
    

    def clean_employee_id_card(self):
        file = self.cleaned_data.get('employee_id_card', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') or file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG/PNG files are allowed.'), code='invalid')
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
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg'):
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
    

    def clean_existing_loan_statement(self):
        file = self.cleaned_data.get('existing_loan_statement', False)
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
    
class CarApplicationVerifyForm(forms.ModelForm):
    class Meta:
        model=CarApplicationVerification
        fields='__all__'
        exclude=['loan']

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        for field in self.fields:
            if not getattr(instance, field):
                setattr(instance, field, 'Rejected')
        
        if commit:
            instance.save()
        return instance
    

class CLBasicDetailForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the terms and conditions to proceed.'})

    class Meta:
        model = CLBasicDetail
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
        if CLBasicDetail.objects.filter(phone_number=mobile_number).exists():
            record=CLBasicDetail.objects.filter(phone_number=mobile_number).last()
            if date.today() > record.expiry_at:
                return mobile_number
            raise forms.ValidationError("Mobile Number already exist! Please try after 3Months.")
        return mobile_number
    
    def clean_pan_num(self):
        pan_num = self.cleaned_data.get('pan_num')
        if CLBasicDetail.objects.filter(pan_num=pan_num).exists():
            record=CLBasicDetail.objects.filter(pan_num=pan_num).last()
            if date.today() > record.expiry_at:
                return pan_num
            raise forms.ValidationError("PAN Number already exist! Please try after 3Months.")
        return pan_num

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match("^[a-zA-Z ]+$", full_name):
            raise ValidationError("Full Name should contain only alphabets.")
        if len(full_name) > 25:
            raise ValidationError("Full Name should not exceed 25 characters.")
        return full_name


    def clean_pan_number(self):
        pan_number = self.cleaned_data.get('pan_number')
        pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        if not re.match(pattern, pan_number):
            raise ValidationError("Invalid PAN Number format.")
        return pan_number


    def clean_Aadhar_number(self):
        Aadhar_number = self.cleaned_data.get('Aadhar_number')
        if not re.match(r'^\d{12}$', Aadhar_number):
            raise ValidationError("Aadhar number must be 12 digits.")
        return Aadhar_number


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email is required.")
        return email


    def clean_required_loan_amount(self):
        required_loan_amount = self.cleaned_data.get('required_loan_amount')
        if not required_loan_amount.isdigit():
            raise ValidationError("Loan amount should be numeric.")
        if int(required_loan_amount) <= 0:
            raise ValidationError("Loan amount must be greater than 0.")
        return required_loan_amount


   

    def clean_terms_accepted(self):
        terms_accepted = self.cleaned_data.get('terms_accepted')
        if not terms_accepted:
            raise ValidationError("You must accept the terms and conditions.")
        return terms_accepted



class CarDisbursementDetailsForm(forms.ModelForm):
    class Meta:
        model=CarDisbursementDetails
        fields='__all__'
        exclude=['verification']