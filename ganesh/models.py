from django.db import models
from django.core.validators import EmailValidator
import random
import string
import re
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Max
from dateutil.relativedelta import relativedelta




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
        raise ValidationError('Invalid pincode format')

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


from datetime import date
def validate_age(date_of_birth):
    if not isinstance(date_of_birth, date):
        raise ValidationError('Invalid date format.')
    
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    
    if not (18 <= age <= 70):
        raise ValidationError('Age must be between 18 and 70 years.')
def validate_address(value):
    
    has_letter = re.search(r'[A-Za-z]', value)
    has_digit = re.search(r'\d', value)

    if not (has_letter and has_digit):
        raise ValidationError('Address must contain both letters and digits.')

    
def validate_email(value):
    if "@" not in value:
        raise ValidationError('Invalid email address.')

    local_part, domain = value.split('@')
    
    if domain != "gmail.com":
        raise ValidationError('Email domain must be gmail.com.')
    
    if not re.search(r'[a-zA-Z]', local_part):
        raise ValidationError('Email must contain at least one letter before @gmail.com.')
    


class credbasicdetailform(models.Model):
    EXIST_CARD_CHOICES = [
        ('YES', 'yes'),
        ('NO', 'no'),

    ]
   
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
    otp = models.CharField(max_length=6, blank=True, null=True)
    application_id = models.CharField(max_length=100, blank=True, unique=True)
    created_at=models.DateField(auto_now_add=True)
    terms_accepted=models.BooleanField(default=False)
    existing_creditcard_holder =models.CharField(max_length=10,choices=EXIST_CARD_CHOICES)
    card_limit = models.IntegerField(null=True,blank=True,validators=[validate_amount])
    card_belonging_bank_name = models.CharField(max_length=25,null=True,blank=True,validators=[validate_only_letters])
    expiry_at=models.DateField(null=True,blank=True)

    def __str__(self):
        return f"{self.application_id}"
    def save(self, *args, **kwargs):
        self.expiry_at = date.today() + relativedelta(months=3)

        if not self.application_id:
            last_entry = credbasicdetailform.objects.filter(application_id__startswith='SLNCC').aggregate(Max('application_id'))
            last_number = last_entry.get('application_id__max', None)

            if last_number:
                try:
                    last_number_int = int(last_number[5:])  
                    new_number = last_number_int + 1
                except ValueError:
                    new_number = 1001
            else:
                new_number = 1001

            self.application_id = f"SLNCC{new_number:04d}"

        print(f"Saving GoldBasicDetail with application_id: {self.application_id}")
        
        
        super(credbasicdetailform, self).save(*args, **kwargs)
        
class creCibilCheck(models.Model):
    user = models.ForeignKey(credbasicdetailform, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6,default='')
    cibil_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)


from datetime import date, timedelta



class CreditDetail(models.Model):
    basicdetailform = models.OneToOneField(credbasicdetailform, on_delete=models.CASCADE)
  
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
    mobile_number = models.CharField(max_length=10, validators=[validate_mobile_number])  # Required
    pan_card_number = models.CharField(max_length=10, validators=[validate_pan])  # Required
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
    ref1_name = models.CharField(max_length=200, validators=[validate_only_letters])  # Required
    ref1_mobile = models.CharField(max_length=10, validators=[validate_mobile_number])  # Required
    ref2_name = models.CharField(max_length=200, validators=[validate_only_letters], blank=True, null=True)  # Optional
    ref2_mobile = models.CharField(max_length=10, validators=[validate_mobile_number], blank=True, null=True)  # Optional
    own_house = models.CharField(max_length=10,choices=own_house)  # Required
    dsaref_code=models.CharField(max_length=100,null=True,blank=True)
    franrefCode=models.CharField(max_length=100,null=True,blank=True)
    empref_code=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateField(auto_now_add=True,null=True,blank=True)

    def save(self,*args,**kwargs):
        
        
        if not self.franrefCode:
            self.franrefCode="SLNBR1001"
        super(CreditDetail,self).save(*args,**kwargs)
   

   
    
    def __str__(self):
        return f"ApplicationVerification for {self.first_name} - Status: {self.last_name}"


class creditDocumentUpload(models.Model):
    personal_detail = models.OneToOneField(CreditDetail, on_delete=models.CASCADE,related_name='pldocument')
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