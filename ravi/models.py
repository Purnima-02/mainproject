from django.db import models
from django.core.validators import EmailValidator
import random
import string
import re
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta


def validate_only_letters(value):
    if not value.isalpha():
        raise ValidationError('Only letters are allowed.')
    
def validate_pan(value):
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid PAN number format')

def validate_mobile_number(value):
    pattern = r'^\+?[1-9]\d{1,14}$'
    if not re.match(pattern, value) or len(value) < 10:
        raise ValidationError('Invalid mobile number format. Must be at least 10 digits long.')
    if len(value) > 15:
        raise ValidationError('Mobile number cannot be more than 15 digits long.')

def validate_aadhar_number(value):
    pattern = r'^\d{12}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid Aadhar number format')

def validate_pincode(value):
    pattern = r'^\d{6}$'
    if not re.match(pattern, value):
        raise ValidationError('Pincode must be 6 digits.')

def validate_pincodes(value):
    if len(str(value)) != 6:
        raise ValidationError('Pincode must be 6 digits.')

def validate_amount(value):
    if len(str(value)) > 10:
        raise ValidationError('Amount must be 10 digits.')
    
def clean_aadhar_card_front(self):
        file = self.cleaned_data.get('aadhar_card_front', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg'):
                raise ValidationError(('Only JPG/JPEG/ files are allowed.'), code='invalid')
        return file
def clean_business_proof_1(self):
        file = self.cleaned_data.get('business_proof_1', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(('Only PDF files are allowed.'), code='invalid')
        return file
def validate_image_file(value):
    if not (value.name.endswith('.jpg') or value.name.endswith('.png') or value.name.endswith('.jpeg')):
        raise ValidationError('Only JPG/JPEG/PNG files are allowed.')


def validate_pdf_file(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')
def validate_date(value):
    if value > timezone.now().date():
        raise ValidationError('Date cannot be in the future.')
def validate_gst_number(value):
    gst_regex = re.compile(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$')
    if not gst_regex.match(value):
        raise ValidationError('Invalid GST number format.')


def validate_age(date_of_birth):
    if not isinstance(date_of_birth, date):
        raise ValidationError('Invalid date format.')
    
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    
    if not (18 <= age <= 70):
        raise ValidationError('Age must be between 18 and 70 years.')
def validate_email(value):
    # Check for the presence of the '@' symbol
    if "@" not in value:
        raise ValidationError('Invalid email address.')

    # Split the email into local part and domain part
    local_part, domain = value.rsplit('@', 1)

    # Check if domain has a valid extension
    valid_extensions = ['.com', '.in']
    if not any(domain.endswith(ext) for ext in valid_extensions):
        raise ValidationError('Please enter a valid email address with .com or .in domain.')

    # Ensure that the local part contains at least one letter
    if not re.search(r'[a-zA-Z]', local_part):
        raise ValidationError('Email must contain at least one letter before @domain.')

    # Optionally: Ensure the email does not contain invalid characters
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
        raise ValidationError('Invalid email address format(abc123@gmail.com).')
    
def validate_address(value):
    if not re.search(r'[A-Za-z]', value):
        raise ValidationError('Address must contain letters and digits.')

from dateutil.relativedelta import relativedelta

class personalbasicdetail(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')]
    
    fname = models.CharField(max_length=50,default='')
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


    def save(self, *args, **kwargs):
        self.expiry_at = date.today() + relativedelta(months=3)

        if not self.application_id:
            # Ensure that we are getting the latest application ID
            last_entry = personalbasicdetail.objects.filter(application_id__startswith='SLNPL').order_by('-application_id').first()
            
            if last_entry:
                # Extract the numeric part from the application ID
                last_number = int(last_entry.application_id[5:])
                new_number = last_number + 1
            else:
                # If no previous entry, start with 1001
                new_number = 1001
            
            # Generate the new application ID
            self.application_id = f"SLNPL{new_number:04d}"
        
        # Ensure the application_id is not an empty string or None
        if not self.application_id:
            raise ValueError("The application_id cannot be empty or None")

        # Save the instance
        print(f"Saving personalbasicdetail with application_id: {self.application_id}")
        super(personalbasicdetail, self).save(*args, **kwargs)


    def __str__(self):
        return f"ApplicationVerification for {self.application_id}"
 
class plCibilCheck(models.Model):
    user = models.ForeignKey(personalbasicdetail, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6,default='')
    cibil_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)


class PersonalDetail(models.Model):
    basicdetailform = models.OneToOneField(personalbasicdetail, on_delete=models.CASCADE)
  
    GENDER_CHOICES = [
        ('FEMALE', 'Female'),
        ('MALE', 'Male'),
        ('OTHER', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
    ]

    COMPANY_TYPE_CHOICES = [
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('GOVERNMENT', 'Government'),
        ('SELF_EMPLOYED', 'Self-employed'),
        ('OTHER', 'Other'),
    ]
    own_house = [
        ('YES', 'Yes'),
        ('NO', 'No'),
    ]
    address = [
        ('RENT', 'Rent'),
        ('OWN', 'Own'),

    ]
    first_name = models.CharField(max_length=100, validators=[validate_only_letters])  # Required
    last_name = models.CharField(max_length=100, validators=[validate_only_letters])  # Required
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)  # Required
    father_name = models.CharField(max_length=100, validators=[validate_only_letters])  # Required
    date_of_birth = models.DateField(validators=[validate_date])  # Required
    mobile_number = models.CharField(max_length=10,null=True,blank=True)  # Required
    pan_card_number = models.CharField(max_length=10,null=True,blank=True)  # Required
    aadhar_card_number = models.CharField(max_length=12, validators=[validate_aadhar_number])  # Required
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)  # Required
    email = models.EmailField(validators=[validate_email])  # Required
    current_address = models.TextField(validators=[validate_address])  # Required
    current_address_type = models.TextField(choices=address)
    current_address_pincode = models.CharField(max_length=6, validators=[validate_pincode])  # Required
    aadhar_address_type = models.TextField(choices=address)
    aadhar_address = models.TextField(validators=[validate_address])  # Required
    aadhar_pincode = models.CharField(max_length=6, validators=[validate_pincode])  # Required
    running_emis = models.CharField(max_length=10, validators=[validate_amount])  # Required
    net_salary = models.CharField(max_length=10, validators=[validate_amount])  # Required
    company_name = models.CharField(max_length=100, validators=[validate_only_letters])  # Required
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES)  # Required
    job_joining_date = models.DateField()  # Required
    job_location = models.CharField(max_length=100)  # Required
    total_job_experience = models.IntegerField()  # Required
    work_email = models.EmailField(validators=[validate_email], blank=True, null=True)  # Optional
    office_address = models.TextField(validators=[validate_address], blank=True, null=True)  # Optional
    office_address_pincode = models.CharField(max_length=6, validators=[validate_pincode])  # Required
    required_loan_amount = models.CharField(max_length=10, validators=[validate_amount])  # Required
    ref1_person_name = models.CharField(max_length=200, validators=[validate_only_letters])  # Required
    ref1_mobile_number = models.CharField(max_length=10, validators=[validate_mobile_number])  # Required
    ref2_person_name = models.CharField(max_length=200, validators=[validate_only_letters], blank=True, null=True)  # Optional
    ref2_mobile_number = models.CharField(max_length=10, validators=[validate_mobile_number], blank=True, null=True)  # Optional
    own_house = models.CharField(max_length=10,choices=own_house)  # Required
    dsaref_code=models.CharField(max_length=100,null=True,blank=True)
    franrefCode=models.CharField(max_length=100,null=True,blank=True)
    application_loan_type=models.CharField(max_length=100,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True,null=True,blank=True)
    empref_code=models.CharField(max_length=40,null=True,blank=True)
    application_id=models.CharField(max_length=500,null=True,blank=True)

    
   
    
    def __str__(self):
        return f"ApplicationVerification for {self.first_name} - Status: {self.last_name}"
    def save(self,*args,**kwargs):
        self.name=self.first_name+self.last_name
        self.application_id=self.basicdetailform.application_id
        print(self.name)  
        if not self.franrefCode:
            self.franrefCode="SLNBR1001"
        # self.application_loan_type=""
        super(PersonalDetail,self).save(*args,**kwargs)


class DocumentUpload(models.Model):
    personal_detail = models.OneToOneField(PersonalDetail, on_delete=models.CASCADE,related_name='pldocument')
    aadhar_card_front = models.ImageField(upload_to='documents/', validators=[validate_image_file])
    aadhar_card_back = models.ImageField(upload_to='documents/', validators=[validate_image_file])
    pan_card = models.ImageField(upload_to='documents/', validators=[validate_image_file])
    customer_photo = models.ImageField(upload_to='documents/', validators=[validate_image_file])
    bank_statement = models.FileField(upload_to='documents/',validators=[validate_pdf_file])
    payslip_1 = models.FileField(upload_to='documents/', validators=[validate_pdf_file])
    
    # Optional fields
    payslip_2 = models.FileField(upload_to='documents/', blank=True, null=True, validators=[validate_pdf_file])
    payslip_3 = models.FileField(upload_to='documents/', blank=True, null=True, validators=[validate_pdf_file])
    employee_id_card = models.ImageField(upload_to='documents/', blank=True, null=True, validators=[validate_image_file])
    current_address_proof = models.FileField(upload_to='documents/', validators=[validate_image_file])
    
    # Additional optional fields
    other_document_1 = models.FileField(upload_to='documents/', blank=True, null=True, validators=[validate_pdf_file])
    other_document_2 = models.FileField(upload_to='documents/', blank=True, null=True, validators=[validate_pdf_file])

    def __str__(self):
        return str(self.personal_detail)

class ApplicationVerification(models.Model):
    personal_detail = models.OneToOneField(PersonalDetail, on_delete=models.CASCADE,related_name='applicationverification') 
    personal_detail_verification = models.CharField(max_length=50, blank=True, )
    documents_upload_verification = models.CharField(max_length=50, blank=True, )
    documents_verification = models.CharField(max_length=50, blank=True, )
    eligibility_check_verification = models.CharField(max_length=50, blank=True, )
    bank_login_verification = models.CharField(max_length=50, blank=True, )
    kyc_and_document_verification = models.CharField(max_length=50, blank=True, )
    enach_verification = models.CharField(max_length=50, blank=True, )
    disbursement_verification = models.CharField(max_length=50, blank=True, )
    verification_status = models.CharField(max_length=100, blank=True,)
    approved_rejected=models.CharField(max_length=50,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ApplicationVerification for {self.personal_detail} - Status: {self.verification_status}"
    

from datetime import date

class pldisbursementdetails(models.Model):
    verification = models.OneToOneField(PersonalDetail, on_delete=models.CASCADE,blank=True, related_name='disbursementdetail',default='')
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
        return f"{self.bank_nbfc_name}-{self.verification.personal_detail}"


class homebasicdetail(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')]
    
    fname = models.CharField(max_length=50,default='')
    lname = models.CharField(max_length=50)
    Dob = models.DateField(validators=[validate_age])
    phone_number = models.BigIntegerField()
    pan_num = models.CharField(max_length=10, validators=[validate_pan])
    Aadhar_number = models.CharField(max_length=12)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    email = models.EmailField(validators=[EmailValidator()], blank=True, null=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    required_loan_amount = models.CharField(max_length=10)
    otp = models.CharField(max_length=6, blank=True, null=True)
    application_id = models.CharField(max_length=100, blank=True, unique=True)
    created_at=models.DateField(auto_now_add=True)
    terms_accepted=models.BooleanField(default=False)
    expiry_at=models.DateField(null=True,blank=True)


    def save(self, *args, **kwargs):
        self.expiry_at = date.today() + relativedelta(months=3)

        if not self.application_id:
            last_entry = homebasicdetail.objects.filter(application_id__startswith='SLNHL').order_by('-application_id').first()
            
            if last_entry:
                last_number = int(last_entry.application_id[5:])
                new_number = last_number + 1
            else:
                new_number = 1001
            
            self.application_id = f"SLNHL{new_number:04d}"
        
        if not self.application_id:
            raise ValueError("The application_id cannot be empty or None")

        print(f"Saving homebasicdetail with application_id: {self.application_id}")
        super(homebasicdetail, self).save(*args, **kwargs)

    def __str__(self):
        return f"ApplicationVerification for {self.application_id}"
class hlCibilCheck(models.Model):
    user = models.ForeignKey(homebasicdetail, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6,default='')
    cibil_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)
#homeloan=============
class CustomerProfile(models.Model):
    basicdetailhome = models.OneToOneField(homebasicdetail, on_delete=models.CASCADE)

    LOAN_TYPE_CHOICES = [('HL', 'HL'), ('HLBT', 'HLBT')]
    INCOME_SOURCE_CHOICES = [('Job', 'Job'), ('Business', 'Business')]
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    COMPANY_TYPE_CHOICES = [
        ('Private', 'Private'),
        ('Public', 'Public'),
        ('Government', 'Government'),
        ('Other', 'Other'),
    ]
    BUSINESS_TYPE_CHOICES = [
        ('Retail', 'Retail'),
        ('Manufacturing', 'Manufacturing'),
        ('Services', 'Services'),
        ('Other', 'Other'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]
    address = [
        ('RENT', 'Rent'),
        ('OWN', 'Own'),

    ]
    loan_type = models.CharField(max_length=10, choices=LOAN_TYPE_CHOICES)
    first_name = models.CharField(max_length=100, validators=[validate_only_letters])
    last_name = models.CharField(max_length=100, validators=[validate_only_letters])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True, validators=[validate_date])
    mobile_number = models.CharField(max_length=10,null=True,blank=True)
    pan_card_number = models.CharField(max_length=10, null=True,blank=True)
    aadhar_card_number = models.CharField(max_length=12, validators=[validate_aadhar_number])
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    
    # Email fields, marked optional
    email_id = models.EmailField(validators=[validate_email], blank=True, null=True) 
 
    current_address_type = models.TextField(choices=address)
    current_address = models.TextField(validators=[validate_address])
    current_address_pincode = models.CharField(max_length=6, validators=[validate_pincode])
    aadhar_address_type = models.TextField(choices=address)
    aadhar_address = models.TextField(validators=[validate_address])
    aadhar_pincode = models.CharField(max_length=6, validators=[validate_pincode])
    running_emis_per_month = models.CharField(max_length=10, validators=[validate_amount])
    income_source = models.CharField(max_length=10, choices=INCOME_SOURCE_CHOICES)

    # Job-related fields
    net_salary_per_month = models.CharField(max_length=10, blank=True, null=True, validators=[validate_amount])
    company_name = models.CharField(max_length=100, blank=True, null=True, validators=[validate_only_letters])
    company_type = models.CharField(max_length=50, choices=COMPANY_TYPE_CHOICES, blank=True, null=True)
    job_joining_date = models.DateField(blank=True, null=True)
    work_email = models.EmailField(blank=True, null=True, validators=[validate_email])
    job_location = models.CharField(max_length=100, blank=True, null=True, validators=[validate_address])
    total_job_experience = models.IntegerField(blank=True, null=True)
    office_address_pincode = models.CharField(max_length=6, blank=True, null=True, validators=[validate_pincode])

    # Business-related fields
    net_income_per_month = models.CharField(max_length=10, blank=True, null=True, validators=[validate_amount])
    business_name = models.CharField(max_length=100, blank=True, null=True, validators=[validate_only_letters])
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES, blank=True, null=True)
    business_establishment_date = models.DateField(blank=True, null=True)
    gst_number = models.CharField(max_length=15, blank=True, null=True, validators=[validate_gst_number])
    
    mother_name = models.CharField(max_length=100, validators=[validate_only_letters])
    father_name = models.CharField(max_length=100, validators=[validate_only_letters])
    nature_of_business = models.CharField(max_length=100, blank=True, null=True)
    turnover_per_year = models.CharField(max_length=10, blank=True, null=True, validators=[validate_amount])
    business_address_pincode = models.CharField(max_length=6, blank=True, null=True, validators=[validate_pincode])
    
    house_plot_purchase_value = models.CharField(max_length=10, default='', validators=[validate_amount])
    required_loan_amount = models.CharField(max_length=10, default='', validators=[validate_amount])
    
    existing_loan_bank_nbfc_name = models.CharField(max_length=100, validators=[validate_only_letters])
    existing_loan_amount = models.CharField(max_length=10, validators=[validate_amount])
    
    # Ref1 and Ref2 fields, marked optional
    ref1_person_name = models.CharField(max_length=200, blank=True, null=True, validators=[validate_only_letters])
    ref1_mobile_number = models.CharField(max_length=10, blank=True, null=True, validators=[validate_mobile_number])
    ref2_person_name = models.CharField(max_length=200, blank=True, null=True, validators=[validate_only_letters])
    ref2_mobile_number = models.CharField(max_length=10, blank=True, null=True, validators=[validate_mobile_number])

    # Co-Applicant Details, with email as optional
    co_applicant_first_name = models.CharField(max_length=100, default='', validators=[validate_only_letters])
    co_applicant_last_name = models.CharField(max_length=100, default='', validators=[validate_only_letters])
    co_applicant_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Other')
    co_applicant_age = models.DateField(max_length=30, validators=[validate_age])
    co_applicant_relationship = models.CharField(max_length=50, default='')
    co_applicant_mobile_number = models.CharField(max_length=10, default='', validators=[validate_mobile_number])
    co_applicant_email_id = models.EmailField(blank=True, null=True, validators=[validate_email])  # optional
    co_applicant_occupation = models.CharField(max_length=100, default='', validators=[validate_only_letters])
    co_applicant_net_income_per_month = models.CharField(max_length=10, default='', validators=[validate_amount])
    dsaref_code=models.CharField(max_length=100,null=True,blank=True)
    franrefCode=models.CharField(max_length=100,null=True,blank=True)
    application_loan_type=models.CharField(max_length=100,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True,null=True,blank=True)
    empref_code=models.CharField(max_length=40,null=True,blank=True)
    application_id=models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self,*args,**kwargs):
        self.name=self.first_name+self.last_name
        self.application_id=self.basicdetailhome.application_id

        print(self.name)
        if not self.franrefCode:
            self.franrefCode="SLNBR1001"
        # self.application_loan_type=""
        super(CustomerProfile,self).save(*args,**kwargs)

class ApplicantDocument(models.Model):
    applicant_profile = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, default=1, related_name='hldocument')

    # Common fields (Required)
    adhar_card_front = models.ImageField(upload_to='documents/', null=False, blank=False, validators=[validate_image_file])
    adhar_card_back = models.ImageField(upload_to='documents/', null=False, blank=False, validators=[validate_image_file])
    pan_card = models.ImageField(upload_to='documents/', null=False, blank=False, validators=[validate_image_file])
    customer_photo = models.ImageField(upload_to='documents/', null=False, blank=False, validators=[validate_image_file])
    home_plot_photo_1 = models.ImageField(upload_to='documents/', null=False, blank=False, validators=[validate_image_file])
    home_plot_photo_2 = models.ImageField(upload_to='documents/', null=False, blank=False, validators=[validate_image_file])
    
    # Optional fields
    home_plot_photo_3 = models.ImageField(upload_to='documents/', null=True, blank=True, validators=[validate_image_file])
    home_plot_photo_4 = models.ImageField(upload_to='documents/', null=True, blank=True, validators=[validate_image_file])
    employee_id_card = models.ImageField(upload_to='documents/', null=True, blank=True, validators=[validate_image_file])

    latest_3_months_banked_statement = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_pdf_file])
    latest_3_months_payslips_1 = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_pdf_file])
    latest_3_months_payslips_2 = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_pdf_file])
    latest_3_months_payslips_3 = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_pdf_file])

    # HLBT fields
    business_proof_1 = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_image_file])
    business_proof_2 = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_image_file])  # Optional
    latest_12_months_banked_statement = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_pdf_file])
    business_office_photo = models.ImageField(upload_to='documents/', null=True, blank=True, validators=[validate_image_file])

    # Required for the first two years, optional for the third year
    latest_3_yrs_itr_1 = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_pdf_file])
    latest_3_yrs_itr_2 = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_pdf_file])
    latest_3_yrs_itr_3 = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_pdf_file])  # Optional
    
    current_address_proof = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_image_file])

    # Business fields
    existing_loan_statement = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_pdf_file])
    other_documents_1 = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_pdf_file])  # Optional
    other_documents_2 = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_pdf_file])  # Optional
    other_documents_3 = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_pdf_file])  # Optional
    other_documents_4 = models.FileField(upload_to='documents/', null=True, blank=True, validators=[validate_pdf_file])  # Optional

    # Co-Applicant Details (Required)
    co_adhar_card_front = models.ImageField(upload_to='documents/', null=False, blank=False, validators=[validate_image_file])
    co_adhar_card_back = models.ImageField(upload_to='documents/', null=False, blank=False, validators=[validate_image_file])
    co_pan_card = models.ImageField(upload_to='documents/', null=False, blank=False, validators=[validate_image_file])
    co_selfie_photo = models.ImageField(upload_to='documents/', null=False, blank=False, validators=[validate_image_file])

    def __str__(self):
        return f"{self.adhar_card_front}"



class HomeApplication(models.Model):
  
    applicant_profile = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE,related_name='applicationverification')
    personal_detail_verification = models.CharField(max_length=50, blank=True, )
    documents_upload_status = models.CharField(max_length=50, blank=True)
    kyc_documents_verification_status = models.CharField(max_length=50, blank=True)
    filed_officer_visit_inspection_status = models.CharField(max_length=50, blank=True)
    eligibility_check_status = models.CharField(max_length=50, blank=True)
    application_fee_paid_status = models.CharField(max_length=50, blank=True)
    tele_verification_status = models.CharField(max_length=50, blank=True)
    bank_login_fee_paid_status = models.CharField(max_length=50, blank=True)
    bank_login_done_status = models.CharField(max_length=50, blank=True)
    credit_manager_visit_status = models.CharField(max_length=50, blank=True)
    bank_nbfc_soft_loan_sanction_letter_issued_status = models.CharField(max_length=50, blank=True)
    legal_technical_completed_status = models.CharField(max_length=50, blank=True)
    final_loan_sanctioned_status = models.CharField(max_length=50, blank=True)
    agreement_signatures_done_status = models.CharField(max_length=50, blank=True)
    enach_auto_debit_done_status = models.CharField(max_length=50, blank=True)
    disbursement_status = models.CharField(max_length=50, blank=True)
    post_documentation_mortgage_status = models.CharField(max_length=50, blank=True)
    cheque_issued_loan_amount_credited_status = models.CharField(max_length=50, blank=True)
    verification_status=models.CharField(max_length=100,blank=True)
    approved_rejected=models.CharField(max_length=50,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    

    def __str__(self):
        return f"Applicant Document: {self.personal_detail_verification}"
    

from datetime import date

class hldisbursementdetails(models.Model):
    verification = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE,blank=True, related_name='disbursementdetail',default='')
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
        return f"{self.bank_nbfc_name}"