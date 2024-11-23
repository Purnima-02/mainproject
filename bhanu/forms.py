from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

class EducationalLoanForm(forms.ModelForm):
    class Meta:
        model = Educationalloan
        fields = '__all__'
        exclude=['application_id','loan_type','name','created_at']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mail_id': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),

            'ref1mobilenumber': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'ref2mobilenumber': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),

            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'university_name': forms.TextInput(attrs={'class': 'form-control'}),
            'score_card': forms.ClearableFileInput(attrs={'class': 'form-control','accept': '.pdf'}),
            'GRE_score': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'IELTS_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'TOEFL_score': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'Duolingo_score': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'PTE_score': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'student_work_experience': forms.Textarea(attrs={'class': 'form-control'}),
            'cibil_score': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'required_loan_amount': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]','placeholder': '₹ Enter amount'}),

            'backlogs': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'residence_location': forms.TextInput(attrs={'class': 'form-control'}),
            'permanent_location': forms.TextInput(attrs={'class': 'form-control'}),
            'co_applicant_type': forms.Select(attrs={'class': 'form-control'}),
            'co_applicant_parent_name': forms.TextInput(attrs={'class': 'form-control salaried-field'}),
            'co_applicant_company_name': forms.TextInput(attrs={'class': 'form-control salaried-field'}),
            'co_applicant_salaried_designation': forms.TextInput(attrs={'class': 'form-control salaried-field'}),
            'co_applicant_salaried_net_pay': forms.NumberInput(attrs={'class': 'form-control salaried-field','pattern':'[0-9]'}),
            'co_applicant_salaried_emis': forms.NumberInput(attrs={'class': 'form-control salaried-field','pattern':'[0-9]'}),
            'co_applicant_salaried_cibil_score': forms.NumberInput(attrs={'class': 'form-control salaried-field','pattern':'[0-9]'}),
            'co_applicant_self_employed_business_name': forms.TextInput(attrs={'class': 'form-control self-employed-field hidden'}),
            'co_applicant_self_employed_itr_mandatory': forms.Select(attrs={'class': 'form-control self-employed-field hidden'}),
            'co_pplicant_self_employed_itr_amount': forms.NumberInput(attrs={'class': 'form-control self-employed-field hidden','pattern':'[0-9]'}),
            'co_applicant_self_employed_business_licence': forms.FileInput(attrs={'class': 'form-control self-employed-field hidden','accept': '.pdf'}),
            'property_location': forms.TextInput(attrs={'class': 'form-control'}),
            'co_applicant_property_details': forms.Select(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'property_market_value': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'property_govt_value': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'property_local_government_body': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels={

           'score_card':'Score Card (PDF) ',
            'dsaref_code':'DSA Referal Code(Optional)',
            'franrefCode':'Franchise Referal Code(Optional)',
           'co_applicant_self_employed_business_licence':'Co Applicant self Employed Business Licence (PDF)',


        }
    def __init__(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id', None)
        kwargs.pop('instance_id', None)
        super().__init__(*args, **kwargs)
        

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        
        if Educationalloan.objects.filter(mobile_number=mobile_number).exclude(id=self.instance_id).exists():
            record=edubasicdetailform.objects.filter(phone_number=mobile_number).last()
            if date.today() > record.expiry_at:
                return mobile_number
            
            raise forms.ValidationError("Mobile number already exist!.")
        if not int(mobile_number)>0 or len(mobile_number)!=10:
            raise forms.ValidationError("Mobile Number Length should be in 10 Digits")
        return mobile_number
    

    def _init_(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id', None)
        kwargs.pop('instance_id', None)  
        super(EducationalLoanForm, self)._init_(*args, **kwargs)
       
    def clean_score_card(self):
        file = self.cleaned_data.get('score_card', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file
    
class DocumentsForm(forms.ModelForm):

    class Meta:
        model=Educationloan_document_upload
        fields='__all__'
        exclude = ['loan']
        widgets={
          'pay_slip_1': forms.FileInput(attrs={'accept': '.pdf'}),
          'pay_slip_2': forms.FileInput(attrs={'accept': '.pdf'}),
          'pay_slip_3': forms.FileInput(attrs={'accept': '.pdf'}),
          'bank_statement': forms.FileInput(attrs={'accept': '.pdf'}),
          'employee_id_card': forms.FileInput(attrs={'accept': '.pdf, image/jpeg, image/png, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document'}),
          'aadhar_card_front': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'aadhar_card_back': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'pan_card': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'customer_photo': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),

          'co_applicant_aadharFront': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'co_applicant_aadharBack': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'co_applicant_panCard': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'co_applicant_photo': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),

        }
        labels = {
         'adhar_card_front': 'Aadhar Card Front (JPEG/PNG)',
         'adhar_card_back': 'Aadhar Card Back (JPEG/PNG)',
         'pan_card': 'Pan Card  (JPEG/PNG)',
         'customer_photo': 'Student Photo or Selfie (JPEG/PNG)',
         'pay_slip_1': 'Co applicant salary pay slip/Business Proof (PDF)',
         'pay_slip_2': 'ITR (PDF)',
         'pay_slip_3': 'Own house proof (PDF)',
         'bank_statement': 'Bank Statement(Latest 12Months) (PDF)',
         'employee_id_card': 'Other Documnets (PDF/JPEG/Doc)',


     }

    def clean_adhar_card_front(self):
        file = self.cleaned_data.get('adhar_card_front', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file
    
    def clean_adhar_card_back(self):
        file = self.cleaned_data.get('adhar_card_back', False)
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
    
    def clean_pay_slip_1(self):
        file = self.cleaned_data.get('pay_slip_1', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file
    
    def clean_pay_slip_2(self):
        file = self.cleaned_data.get('pay_slip_2', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file
    
    def clean_pay_slip_3(self):
        file = self.cleaned_data.get('pay_slip_3', False)
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
    

class eduBasicDetailForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the terms and conditions to proceed.'})

    class Meta:
        model = edubasicdetailform
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
            'phone_number':{'required': 'Pan number is required.'},             
            'Dob': {'required': 'Date of birth is required.'},
            'marital_status': {'required': 'Marital status is required.'},
            'required_loan_amount': {'required': 'Required loan amount is required.'},
            'terms_accepted': {'required': 'You must accept the terms and conditions to proceed.'},
        }

    def clean_phone_number(self):
        mobile_number = self.cleaned_data.get('phone_number')
        if edubasicdetailform.objects.filter(phone_number=mobile_number).exists():
            record=edubasicdetailform.objects.filter(phone_number=mobile_number).last()
            if date.today() > record.expiry_at:
                return mobile_number
            raise forms.ValidationError("Mobile Number already exist! Please try after 3Months.")
        return mobile_number
    
    def clean_pan_num(self):
        pan_num = self.cleaned_data.get('pan_num')
        if edubasicdetailform.objects.filter(pan_num=pan_num).exists():
            record=edubasicdetailform.objects.filter(pan_num=pan_num).last()
            if date.today() > record.expiry_at:
                return pan_num
            raise forms.ValidationError("PAN Number already exist! Please try after 3Months.")
        return pan_num

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance

class EduDisbursementDetailsForm(forms.ModelForm):
    class Meta:
        model=Edudisbursementdetails
        fields='__all__'
        exclude=['verification']