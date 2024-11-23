from django.db import models,transaction
from decimal import Decimal
import re
from datetime import timedelta
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator
import random
import string
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone
from django.db.models import Max
from datetime import date
import datetime

from dateutil.relativedelta import relativedelta

## insurance
class AllInsurance(models.Model):
    insurance_name=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    mobile_number=models.CharField(max_length=15)
    email_id = models.EmailField()
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    messgae=models.TextField()
    dsaref_code=models.CharField(max_length=100,null=True,blank=True)
    franrefCode=models.CharField(max_length=100,null=True,blank=True)
    empref_code=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateField(auto_now_add=True,null=True,blank=True)


    def __str__(self) :
        return f"{self.insurance_name} -{self.name}"
    
class LifeInsurance(models.Model):
    insurance_name=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    mobile_number=models.CharField(max_length=15)
    email_id = models.EmailField()
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    messgae=models.TextField()
    dsaref_code=models.CharField(max_length=100,null=True,blank=True)
    franrefCode=models.CharField(max_length=100,null=True,blank=True)
    empref_code=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateField(auto_now_add=True,null=True,blank=True)


    def __str__(self) :
        return f"{self.insurance_name} -{self.name}" 

class GeneralInsurance(models.Model):
    insurance_name=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    mobile_number=models.CharField(max_length=15)
    email_id = models.EmailField()
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    messgae=models.TextField()
    dsaref_code=models.CharField(max_length=100,null=True,blank=True)
    franrefCode=models.CharField(max_length=100,null=True,blank=True)
    empref_code=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateField(auto_now_add=True,null=True,blank=True)

    def __str__(self) :
        return f"{self.insurance_name} -{self.name}" 

class healthInsurance(models.Model):
    insurance_name=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    mobile_number=models.CharField(max_length=15)
    email_id = models.EmailField()
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    messgae=models.TextField()
    dsaref_code=models.CharField(max_length=100,null=True,blank=True)
    franrefCode=models.CharField(max_length=100,null=True,blank=True)
    empref_code=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateField(auto_now_add=True,null=True,blank=True)

    def __str__(self) :
        return f"{self.insurance_name} -{self.name}" 


# Custom validators

def validate_only_letters(value):
    if not value.isalpha() and r'^\s{100}$':
        raise ValidationError('Only letters are allowed.')
    
def validate_pan(value):
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid PAN number format')

def validate_mobile_number(value):
    
    if len(value)!=10 or not value.isdigit():
        raise ValidationError('Invalid mobile number format')

def validate_pincode(value):
    pattern = r'^\d{6}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid pincode format')

def validate_amount(value):
    if len(str(value)) > 10:
        raise ValidationError('Amount must be 10 digits.')
    
def validate_date(value):
    if value > timezone.now().date():
        raise ValidationError('Date should be in the past or present.')
    
def validate_address(value):
    # Check if value contains both letters and digits
    has_letter = re.search(r'[A-Za-z]', value)
    has_digit = re.search(r'\d', value)

    if not (has_letter and has_digit):
        raise ValidationError('Address must contain both letters and digits.')

    
def validate_gst_number(value):
    gst_regex = re.compile(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$')
    
    value_str = str(value)  # Convert the value to a string
    if not gst_regex.match(value_str):
        raise ValidationError('Invalid GST number format.')

def validate_age(date_of_birth):
    if not isinstance(date_of_birth, date):
        raise ValidationError('Invalid date format.')
    
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    
    if not (18 <= age <= 70):
        raise ValidationError('Age must be between 18 and 70 years.')
    
def validate_email(value):
    if "@" not in value:
        raise ValidationError('Invalid email address.')

    local_part, domain = value.rsplit('@', 1)

    valid_extensions = ['.com', '.in']
    if not any(domain.endswith(ext) for ext in valid_extensions):
        raise ValidationError('Please enter a valid email address with .com or .in domain.')

    if not re.search(r'[a-zA-Z]', local_part):
        raise ValidationError('Email must contain at least one letter before @domain.')

    # Optionally: Ensure the email does not contain invalid characters
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
        raise ValidationError('Invalid email address format.')

# Models
class basicdetailform(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')]
    
    fname = models.CharField(max_length=25)
    lname = models.CharField(max_length=50)
    Dob = models.DateField(validators=[validate_age])
    phone_number = models.BigIntegerField()
    pan_num = models.CharField(max_length=10, validators=[validate_pan])
    Aadhar_number = models.CharField(max_length=12)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,null=True,blank=True)
    email = models.EmailField(validators=[EmailValidator()], blank=True, null=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES,null=True,blank=True)
    required_loan_amount = models.CharField(max_length=10)
    otp = models.CharField(max_length=6, blank=True, null=True)
    application_id = models.CharField(max_length=100, blank=True, unique=True)
    created_at=models.DateField(auto_now_add=True)
    terms_accepted=models.BooleanField(default=False)
    expiry_at=models.DateField(null=True,blank=True)


    def __str__(self):
        return f"{self.application_id}"

    def save(self, *args, **kwargs):
        self.expiry_at = date.today() + relativedelta(months=3)

        if not self.application_id:
            last_entry = basicdetailform.objects.filter(application_id__startswith='SLNLAP').order_by('-application_id').first()
            
            if last_entry:
                last_number = int(last_entry.application_id[6:])
                new_number = last_number + 1
            else:
                new_number = 1001
            
            self.application_id = f"SLNLAP{new_number:04d}"
        
       
        
        super(basicdetailform, self).save(*args, **kwargs)

class CibilCheck(models.Model):
    user = models.ForeignKey(basicdetailform, on_delete=models.CASCADE,related_name='cibil_checks')
    otp = models.CharField(max_length=6,default='')
    cibil_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)

    def __str__(self):
        return self.cibil_score

class goldbasicdetailform(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')]
    
    fname = models.CharField(max_length=25)
    lname = models.CharField(max_length=50)
    Dob = models.DateField(validators=[validate_age])
    phone_number = models.BigIntegerField()
    pan_num = models.CharField(max_length=10, validators=[validate_pan])
    Aadhar_number = models.CharField(max_length=12)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,null=True,blank=True)
    email = models.EmailField(validators=[EmailValidator()], blank=True, null=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES,null=True,blank=True)
    required_loan_amount = models.CharField(max_length=10)
    otp = models.CharField(max_length=6, blank=True, null=True)
    application_id = models.CharField(max_length=100, blank=True, unique=True)
    created_at=models.DateField(auto_now_add=True)
    terms_accepted=models.BooleanField(default=False)
    expiry_at=models.DateField(null=True,blank=True)

    def __str__(self):
        return f"{self.application_id}"
    def save(self, *args, **kwargs):
        self.expiry_at = date.today() + relativedelta(months=3)

        if not self.application_id:
            last_entry = goldbasicdetailform.objects.filter(application_id__startswith='SLNGL').aggregate(Max('application_id'))
            last_number = last_entry.get('application_id__max', None)

            if last_number:
                try:
                    last_number_int = int(last_number[5:])  
                    new_number = last_number_int + 1
                except ValueError:
                    new_number = 1001
            else:
                new_number = 1001

            self.application_id = f"SLNGL{new_number:04d}"
        
        
        super(goldbasicdetailform, self).save(*args, **kwargs)
class goldCibilCheck(models.Model):
    user = models.ForeignKey(goldbasicdetailform, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6,default='')
    cibil_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)

    def __str__(self):
        return self.cibil_score

class LoanApplication(models.Model):
    LOAN_TYPE_CHOICES = [
        ('LAP', 'Lap'),
        ('LAPBT', 'Lap-BT'),
    ]
    INCOME_SOURCE_CHOICES = [
        ('JOB', 'Job'),
        ('BUSINESS', 'Business'),
    ]
    BUSINESS_TYPE_CHOICES = [
        ('Retail', 'Retail'),
        ('Manufacturing', 'Manufacturing'),
        ('Services', 'Services'),
        ('Other', 'Other'),
    ]

    
    basic_detail = models.OneToOneField(basicdetailform, on_delete=models.CASCADE,related_name='loanapplication')

    loan_type = models.CharField(max_length=10, choices=LOAN_TYPE_CHOICES)
    first_name = models.CharField(max_length=50,validators=[validate_only_letters])
    last_name = models.CharField(max_length=50,validators=[validate_only_letters])
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = models.DateField(validators=[validate_age])
    mobile_number = models.CharField(max_length=10, validators=[validate_mobile_number],null=True,blank=True)
    pan_card_number = models.CharField(max_length=10,null=True,blank=True,default='')
    aadhar_card_number = models.CharField(max_length=12,)
    marital_status = models.CharField(max_length=10, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')])
    email_id = models.EmailField(validators=[validate_email],null=True,blank=True)
    current_address_type=models.CharField(max_length=20,choices=[('OWN','Own'),('Rent','Rent')])
    current_address = models.TextField(validators=[validate_address])
    current_address_pincode = models.CharField(max_length=6, validators=[validate_pincode])
    aadhar_address_type=models.CharField(max_length=20,choices=[('OWN','OWN'),('Rent','RENT')],default='')

    aadhar_address = models.TextField(validators=[validate_address])
    aadhar_pincode = models.CharField(max_length=6, validators=[validate_pincode])

    # Job-related Fields
    income_source = models.CharField(max_length=10, choices=INCOME_SOURCE_CHOICES)
    net_salary_per_month = models.IntegerField(validators=[validate_amount],null=True,blank=True)
    company_name = models.CharField(max_length=100,validators=[validate_only_letters],default='',null=True,blank=True)
    company_type = models.CharField(max_length=50, null=True, blank=True,validators=[validate_only_letters])
    job_joining_date = models.DateField(null=True, blank=True,validators=[validate_date])
    job_location = models.CharField(max_length=100, null=True, blank=True)
    total_job_experience = models.IntegerField(null=True, blank=True)

    # Business-related Fields
    net_income_per_month = models.IntegerField(null=True, blank=True,validators=[validate_amount])
    business_name = models.CharField(max_length=100, null=True, blank=True,validators=[validate_only_letters])
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES, blank=True, null=True)
    business_establishment_date = models.DateField(null=True, blank=True,validators=[validate_date])
    gst_certificate = models.BooleanField(default=False, verbose_name="GST Certificate?")
    gst_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="GST Number",validators=[validate_gst_number])
    nature_of_business = models.TextField(null=True, blank=True,validators=[validate_only_letters])
    turnover_in_lakhs_per_year = models.IntegerField(null=True, blank=True,validators=[validate_amount])

    # Additional Fields
    property_value = models.IntegerField(validators=[validate_amount])
    required_loan_amount = models.IntegerField(validators=[validate_amount])
    existing_loan = models.BooleanField(default=False)
    existing_loan_details = models.CharField(max_length=100, null=True, blank=True)
    existing_loan_amount=models.CharField(max_length=10,blank=True,null=True)
    ref1_name = models.CharField(max_length=10,null=True,blank=True)
    ref1_mobile = models.CharField(max_length=10,null=True,blank=True, validators=[validate_mobile_number])
    ref2_name = models.CharField(max_length=10,null=True,blank=True)
    ref2_mobile = models.CharField(max_length=10,null=True,blank=True, validators=[validate_mobile_number])
    remarks = models.TextField(null=True, blank=True)

    # Co-Applicant Fields
    co_applicant_first_name = models.CharField(max_length=50, null=False, blank=False,validators=[validate_only_letters],default="")
    co_applicant_last_name = models.CharField(max_length=50, null=False, blank=False,validators=[validate_only_letters],default="")
    co_applicant_gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    co_applicant_age = models.DateField(null=False, blank=False, validators=[validate_age], default=datetime.date(2020, 1, 1))
    co_applicant_relationship = models.CharField(max_length=50, null=False, blank=False,validators=[validate_only_letters],default="")
    co_applicant_mobile_number = models.CharField(max_length=10, null=False, blank=False, validators=[validate_mobile_number],default="")
    co_applicant_email_id = models.EmailField(null=True, blank=True, validators=[validate_email])
    co_applicant_occupation = models.CharField(max_length=50, null=False, blank=False,validators=[validate_only_letters],default="")
    co_applicant_net_income_per_month = models.IntegerField(null=False, blank=False,validators=[validate_amount])
    dsaref_code=models.CharField(max_length=100,null=True,blank=True)
    franrefCode=models.CharField(max_length=100,null=True,blank=True)
    application_loan_type=models.CharField(max_length=100,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True,null=True,blank=True)
    empref_code=models.CharField(max_length=40,null=True,blank=True)
    application_id=models.CharField(max_length=500,null=True,blank=True)


    def __str__(self):
        return f"{self.basic_detail.application_id}"
    def save(self,*args,**kwargs):
        self.name=self.first_name+self.last_name
        self.application_loan_type="LAP"
        self.application_id=self.basic_detail.application_id
        if not self.franrefCode:
            self.franrefCode="SLNBR1001"
       
        super(LoanApplication,self).save(*args,**kwargs)
    
    

def validate_image_file(value):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    extension = value.name.split('.')[-1].lower()
    if f".{extension}" not in valid_extensions:
        raise ValidationError('Only JPG, JPEG, and PNG files are allowed.')

def validate_pdf_file(value):
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')


class lapDocumentUpload(models.Model):
    personal_details = models.OneToOneField(LoanApplication, on_delete=models.CASCADE,related_name='lapdocument')
    adhar_card_front = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    adhar_card_back = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    pan_card = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    customer_photo = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    property_photo1 = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    property_photo2 = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    property_photo3 = models.ImageField(upload_to='documents/',validators=[validate_image_file],null=True, blank=True)
    property_photo4 = models.ImageField(upload_to='documents/',validators=[validate_image_file],null=True, blank=True)
    pay_slips_1 = models.FileField(upload_to='documents/',validators=[validate_pdf_file],null=True, blank=True,default='')
    pay_slips_2 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    pay_slips_3 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    bank_statement = models.FileField(upload_to='documents/',validators=[validate_pdf_file],null=True, blank=True,default='')
    employee_id_card = models.ImageField(upload_to='documents/', validators=[validate_image_file],null=True, blank=True,)
    business_proof1 = models.FileField(upload_to='documents/', validators=[validate_pdf_file],null=True, blank=True,default='')
    business_proof2 = models.FileField(upload_to='documents/', validators=[validate_pdf_file],null=True, blank=True,default='')
    bank_statement_12m = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    business_office_photo = models.ImageField(upload_to='documents/',validators=[validate_image_file],null=True, blank=True,default='')
    itr1 = models.FileField(upload_to='documents/',validators=[validate_pdf_file],null=True, blank=True,default='')
    itr2 = models.FileField(upload_to='documents/',validators=[validate_pdf_file],null=True, blank=True,default='')
    itr3 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    address_proof = models.FileField(upload_to='documents/', validators=[validate_pdf_file],null=True, blank=True,default='')
    existing_loan_statement = models.FileField(upload_to='documents/',null=True, blank=True,validators=[validate_pdf_file],default='')
    other_document1 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    other_document2 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    other_document3 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    other_document4 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])

    # Co-applicant documents
    co_applicant_adhar_card_front = models.ImageField(upload_to='documents/adhar_front/',null=False, blank=False,validators=[validate_image_file],default="image")
    co_applicant_adhar_card_back = models.ImageField(upload_to='documents/adhar_back/',null=False, blank=False,validators=[validate_image_file],default="image")
    co_applicant_pan_card = models.ImageField(upload_to='documents/pan_card/',null=False, blank=False,validators=[validate_image_file],default="image")
    co_applicant_selfie_photo = models.ImageField(upload_to='documents/selfie_photo/',null=False, blank=False,validators=[validate_image_file],default="image")


class Goldloanapplication(models.Model):
    goldbasicdetail=models.OneToOneField(goldbasicdetailform,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    Pan_number=models.CharField(max_length=11,default='',null=True,blank=True)
    Aadhar_number=models.CharField(max_length=10,null=False,default='')
    email = models.EmailField(null=True, blank=True, validators=[validate_email])
    mobile_number = models.CharField(
        max_length=10,  
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Contact number must be 10 digits.',
                code='invalid_contact_number'
            )
        ],
        null=True,
        blank=True
    )    
    state = models.CharField(max_length=50, null=False, blank=False,validators=[validate_only_letters])
    pincode = models.CharField(max_length=6, validators=[validate_pincode])
    dsaref_code=models.CharField(max_length=100,null=True,blank=True)
    franrefCode=models.CharField(max_length=100,null=True,blank=True)
    application_loan_type=models.CharField(max_length=100,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True,null=True,blank=True)
    empref_code=models.CharField(max_length=40,null=True,blank=True)
    application_id=models.CharField(max_length=500,null=True,blank=True)
    def save(self,*args,**kwargs):
        self.name=self.name
        self.application_loan_type="goldloan"
        self.application_id=self.goldbasicdetail.application_id

        if not self.franrefCode:
            self.franrefCode="SLNBR1001"
        super(Goldloanapplication,self).save(*args,**kwargs)
   



class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)


class lapApplicationVerification(models.Model):

    loan= models.OneToOneField(LoanApplication, on_delete=models.CASCADE,blank=True,related_name='applicationverification')
    personal_detail_verifaction=models.CharField(max_length=50,blank=True)
    documents_upload_verification=models.CharField(max_length=50,blank=True)
    kyc_and_document_verification=models.CharField(max_length=50,blank=True)
    field_officer_visit_inspection=models.CharField(max_length=50,blank=True)
    eligibility_check_verification=models.CharField(max_length=50,blank=True)
    approved_rejected=models.CharField(max_length=50,blank=True)
    Application_fee_paid=models.CharField(max_length=50,blank=True)
    tele_verification=models.CharField(max_length=50,blank=True)
    bank_login_fee_paid=models.CharField(max_length=50,blank=True)
    bank_login_done=models.CharField(max_length=50,blank=True)
    credit_manager_visit=models.CharField(max_length=50,blank=True)
    bank_or_nbfc_soft_loan_sanctioned=models.CharField(max_length=50,blank=True)
    final_loan_sanctioned=models.CharField(max_length=50,blank=True)
    legal_techinal_completed=models.CharField(max_length=50,blank=True)
    agreement_signatures_done=models.CharField(max_length=50,blank=True)
    enach_verification=models.CharField(max_length=50,blank=True)
    disbursment_verification=models.CharField(max_length=50,blank=True)
    post_documentation=models.CharField(max_length=100,blank=True)
    cheque_issued=models.CharField(max_length=100,blank=True)
    verification_status=models.CharField(max_length=100,blank=True)
    status_approved_at= models.DateTimeField(null=True, blank=True)  # New field to store timestamp

    def clean(self):
        super().clean()
        if self.verification_status == 'Approved' and not self.status_approved_at:
            self.status_approved_at = timezone.now()
        elif self.verification_status != 'Approved':
            self.status_approved_at = None

class disbursementdetails(models.Model):
    verification = models.OneToOneField(LoanApplication, on_delete=models.CASCADE,blank=True, related_name='disbursementdetail',default='')
    bank_nbfc_name=models.CharField(max_length=50,null=True,blank=True)
    bank_loginid=models.CharField(max_length=20,null=True,blank=True)
    location=models.CharField(max_length=20,null=True,blank=True)
    loan_amount=models.CharField(max_length=20,null=True,blank=True)
    disbursement_date=models.DateField(default=date.today)
    tenure=models.CharField(max_length=50,null=True,blank=True)
    roi=models.CharField(max_length=50,null=True,blank=True)
    insurance=models.CharField(max_length=50,null=True,blank=True)
    net_disbursement=models.CharField(max_length=50,null=True,blank=True)
    bank_person_name=models.CharField(max_length=50,null=True,blank=True)
    mobile_no=models.CharField(max_length=10,null=True,blank=True)
    comment=models.TextField(max_length=500,null=True,blank=True)
    

    def __str__(self):
        return f"{self.bank_nbfc_name}-{self.verification.basic_detail}"
    
class otherbasicdetailform(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')]
    
    fname = models.CharField(max_length=25)
    lname = models.CharField(max_length=50)
    Dob = models.DateField(validators=[validate_age])
    phone_number = models.BigIntegerField()
    pan_num = models.CharField(max_length=10, validators=[validate_pan])
    Aadhar_number = models.CharField(max_length=12)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,null=True,blank=True)
    email = models.EmailField(validators=[EmailValidator()], blank=True, null=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES,null=True,blank=True)
    comment = models.CharField(max_length=500)
    otp = models.CharField(max_length=6, blank=True, null=True)
    application_id = models.CharField(max_length=100, blank=True, unique=True)
    created_at=models.DateField(auto_now_add=True)
    terms_accepted=models.BooleanField(default=False)
    expiry_at=models.DateField(null=True,blank=True)


    def __str__(self):
        return f"{self.application_id}"

    def save(self, *args, **kwargs):
        self.expiry_at = date.today() + relativedelta(months=3)

        if not self.application_id:
            last_entry = otherbasicdetailform.objects.filter(application_id__startswith='SLNOL').aggregate(Max('application_id'))
            last_number = last_entry.get('application_id__max', None)

            if last_number:
                try:
                    last_number_int = int(last_number[5:])  
                    new_number = last_number_int + 1
                except ValueError:
                    new_number = 1001
            else:
                new_number = 1001

            self.application_id = f"SLNOL{new_number:04d}"
        
        
        super(otherbasicdetailform, self).save(*args, **kwargs)
class otherCibilCheck(models.Model):
    user = models.ForeignKey(otherbasicdetailform, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6,default='')
    cibil_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)

    def __str__(self):
        return self.cibil_score

        
    
class otherloans(models.Model):
    otherbasicdetail=models.OneToOneField(otherbasicdetailform,on_delete=models.CASCADE,related_name='otherloan',default='')
    Full_name=models.CharField(max_length=50,validators=[validate_only_letters])
    pan_number=models.CharField(max_length=10,null=True,blank=True)
    mobile_number=models.CharField(max_length=10,default='',null=True,blank=True)
    Aadhar_number=models.CharField(max_length=12)
    date_of_birth=models.DateField(null=True,blank=True,validators=[validate_age])
    email=models.EmailField(null=True,blank=True)
    state=models.CharField(max_length=30)
    pincode=models.CharField(max_length=6)
    comments=models.CharField(max_length=500,null=True,blank=True)
    loan_type=models.CharField(max_length=50)
    created_at=models.DateField(auto_now_add=True)
    dsaref_code=models.CharField(max_length=100,null=True,blank=True)
    franrefCode=models.CharField(max_length=100,null=True,blank=True)
    application_loan_type=models.CharField(max_length=100,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True,null=True,blank=True)
    empref_code=models.CharField(max_length=40,null=True,blank=True)
    application_id=models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.Full_name
    def save(self,*args,**kwargs):
        if not self.application_id:
            self.application_id = self.otherbasicdetail.application_id
        self.name=self.Full_name
        self.application_loan_type="otherloan"  
        if not self.franrefCode:
            self.franrefCode="SLNBR1001"
        super(otherloans,self).save(*args,**kwargs)
from django.db import IntegrityError

class dsa(models.Model):
    name=models.CharField(max_length=100)
    email_id=models.EmailField(null=True,blank=True)
    phone=models.CharField(max_length=10)
    pan=models.CharField(max_length=12,null=True,blank=True)
    aadhar=models.CharField(max_length=12)
    profession=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    acc_number=models.CharField(max_length=30)
    acc_holder_name=models.CharField(max_length=30)
    bank_name=models.CharField(max_length=30)
    ifsc_code=models.CharField(max_length=40)
    branch_name=models.CharField(max_length=20)
    agreeCheck=models.BooleanField(default=False)
    franchiserefcode=models.CharField(max_length=400,null=True,blank=True)
    dsa_id = models.CharField(max_length=15, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            max_id = dsa.objects.aggregate(models.Max('id'))['id__max']
            if max_id is None:
                self.id = 555  # Starting from 555 as per your requirement
                self.dsa_id = f"SLNDSA{self.id}"
            else:
                all_ids = set(dsa.objects.values_list('id', flat=True))
                for i in range(555, max_id + 2):
                    if i not in all_ids:
                        self.id = i
                        self.dsa_id = f"SLNDSA{self.id}"
                        break
        super(dsa, self).save(*args, **kwargs)    
class franchise(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(null=True,blank=True)
    phone=models.CharField(max_length=10)
    pan=models.CharField(max_length=12,null=True,blank=True)
    aadhar=models.CharField(max_length=12)
    profession=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    agreeCheck=models.BooleanField(default=False)
    dsaPhoto=models.ImageField(validators=[validate_image_file],upload_to='dsa/')
    aadharFront=models.ImageField(validators=[validate_image_file],upload_to='dsa/')
    aadharBack=models.ImageField(validators=[validate_image_file],upload_to='dsa/')
    panCard=models.ImageField(validators=[validate_image_file],upload_to='dsa/')
    bankDocument=models.ImageField(validators=[validate_image_file],upload_to='dsa/')
    franchiserefcode=models.CharField(max_length=500,null=True,blank=True)
    franchise_id = models.CharField(max_length=15, unique=True, blank=True)

    def save(self, *args, **kwargs):
       if not self.franchise_id:  
            max_id = franchise.objects.aggregate(models.Max('id'))['id__max']  
        
            if max_id is None:
                new_id = 1  # Start from 1 if there are no records
            else:
                all_ids = set(franchise.objects.values_list('id', flat=True))
            # Initialize new_id with max_id + 1 to handle the case where all IDs are sequentially assigned
                new_id = max_id + 1
                for i in range(1, max_id + 2):  
                    if i not in all_ids:
                       new_id = i
                       break

            self.franchise_id = f"SLNBR{new_id:03d}" 

            super(franchise, self).save(*args, **kwargs)


    def __str__(self):
        return self.name


class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    reason_to_connect = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}-{self.email}"

   



    













    




    

   
    