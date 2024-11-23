from django.db import models
import re
from datetime import date, timedelta
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator
import random
import string
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone
from django.db.models import Max
from dateutil.relativedelta import relativedelta


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
    # bhanu
   
    record=busbasicdetailform.objects.filter(phone_number=value).last()
    if record:
     
     if not date.today() > record.expiry_at:
        raise ValidationError('Mobile Number Already Exists...')

def validate_aadhar_number(value):
      # Convert the value to a string
    if len(value) != 12 or not value.isdigit():
        
        raise ValidationError('Invalid Aadhar number format. It should be exactly 12 digits and contain only numbers.')

def validate_pincode(value):
    pattern = r'^\d{6}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid pincode format')



def validate_amount(value):
    if len(str(value)) > 10:
        raise ValidationError('Amount must be lessthan 10 digits.')
    
def validate_date(value):
    if value  > timezone.now().date():
        raise ValidationError('Date should be in past or present')
    
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




    


class busbasicdetailform(models.Model):
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



    def __str__(self):
        return f"{self.full_name}"
    
    def save(self,*args,**kwargs):
        
        self.expiry_at = date.today() + relativedelta(months=3)
        
        if not self.id:
            max_id = busbasicdetailform.objects.aggregate(models.Max('id'))['id__max']
            if max_id is None:
                self.id = 1001
                self.application_id=f"SLNBL{self.id}"
            else:
                all_ids = set(busbasicdetailform.objects.values_list('id', flat=True))
                for i in range(1001, max_id + 2):
                    if i not in all_ids:
                        self.id = i
                        self.application_id=f"SLNBL{self.id}"
                        break
        super(busbasicdetailform,self).save(*args, **kwargs)
        

class busCibilCheck(models.Model):
    user = models.ForeignKey(busbasicdetailform, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6,default='')
    cibil_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)


class BusinessLoan(models.Model):
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]

    BUSINESS_TYPE_CHOICES = [
        ('Sole Proprietorship', 'Sole Proprietorship'),
        ('Partnership', 'Partnership'),
        ('Private Limited Company', 'Private Limited Company'),
        ('Public Limited Company', 'Public Limited Company'),
        ('LLP', 'Limited Liability Partnership'),
        ('Others', 'Others'),
    ]

    YES_NO_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]

    RENT_OR_OWN=[
        ('O','OWN'),
        ('R','RENT'),
    ]
    basicdetailform=models.OneToOneField(busbasicdetailform, on_delete=models.CASCADE, related_name='busiloan',blank=True,null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=10)
    pan_card_number = models.CharField(max_length=10)
    aadhar_card_number = models.CharField(max_length=12)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    email_id = models.EmailField()
    current_adress_type=models.CharField(max_length=1, choices=RENT_OR_OWN,null=True)
    current_address = models.TextField()
    current_address_pincode = models.IntegerField()
    aadhar_adress_type=models.CharField(max_length=1, choices=RENT_OR_OWN,null=True)
    aadhar_address = models.TextField()
    aadhar_pincode = models.IntegerField()
    running_emis_amount_per_month = models.DecimalField(max_digits=15, decimal_places=2)
    net_income_per_month = models.DecimalField(max_digits=15, decimal_places=2)
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES)
    business_establishment_date = models.DateField()
    has_gst_certificate = models.CharField(max_length=1, choices=YES_NO_CHOICES)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    mother_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    nature_of_business = models.CharField(max_length=200)
    turnover_in_lakhs_per_year = models.DecimalField(max_digits=15, decimal_places=2)
    business_address = models.TextField()
    business_address_pincode = models.IntegerField()
    total_job_experience= models.CharField(max_length=200,null=True)
    required_loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    # ref_1_person_name = models.CharField(max_length=100)
    # ref_1_person_mobile_number = models.CharField(max_length=15)
    # ref_2_person_name = models.CharField(max_length=100)
    # ref_2_person_mobile_number = models.CharField(max_length=15)
    
    own_house = models.CharField(max_length=1, choices=YES_NO_CHOICES)
    remarks = models.TextField(null=False)
    ref1name=models.CharField(max_length=100,null=True,verbose_name="Reference1 Name",blank=True)
    ref1mobilenumber=models.CharField(max_length=100,null=True,verbose_name="Reference1 Mobile Number",blank=True)
    ref2name=models.CharField(max_length=100,null=True,verbose_name="Reference2 Name",blank=True)
    ref2mobilenumber=models.CharField(max_length=100,null=True,verbose_name="Reference2 Mobile Number",blank=True)

    # name=models.CharField(max_length=100,null=True,blank=True)
    application_id=models.CharField(max_length=200,unique=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    
    dsaref_code=models.CharField(max_length=100,null=True,blank=True)
    franrefCode=models.CharField(max_length=100,null=True,blank=True)
    empref_code=models.CharField(max_length=100,null=True,blank=True)

    application_loan_type = models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True,null=True,blank=True)
    expiry_at=models.DateField(null=True,blank=True)

    def __str__(self):
        return f"{self.id}={self.first_name} {self.last_name} - {self.business_name}"
    

    def save(self,*args,**kwargs):
        self.name=self.first_name+self.last_name
        self.application_loan_type="Business"
        
        self.expiry_at = date.today() + relativedelta(months=3)
        
       
        if not self.franrefCode:
            self.franrefCode="SLNBR1001"
        if not self.id:
            
            max_id = BusinessLoan.objects.aggregate(models.Max('id'))['id__max']
            if max_id is None:
                self.id = 1001
            else:
                all_ids = set(BusinessLoan.objects.values_list('id', flat=True))
                for i in range(1001, max_id + 2):
                    if i not in all_ids:
                        self.id = i
                        break
        super(BusinessLoan,self).save(*args, **kwargs)

    
class Busdisbursementdetails(models.Model):
    verification = models.OneToOneField(BusinessLoan, on_delete=models.CASCADE,blank=True, related_name='disbursementdetail',default='')
    bank_nbfc_name=models.CharField(max_length=50)
    bank_loginid=models.CharField(max_length=20)
    location=models.CharField(max_length=20)
    loan_amount=models.CharField(max_length=20)
    disbursement_date=models.DateField(default=date.today)
    tenure=models.CharField(max_length=50)
    roi=models.CharField(max_length=50)
    insurance=models.CharField(max_length=50)
    net_disbursement=models.CharField(max_length=50)
    bank_person_name=models.CharField(max_length=50)
    mobile_no=models.CharField(max_length=10)
    comment=models.TextField(max_length=500)
    

    def _str_(self):
        return f"{self.bank_nbfc_name}-{self.verification.basic_detail}"



class BusinessLoanDocument(models.Model):
    loan = models.OneToOneField(BusinessLoan, on_delete=models.CASCADE, related_name='BussinessLoandocuments',blank=True)
    aadhar_card_front = models.ImageField(upload_to='BussinessLoandocuments/aadhar/')
    aadhar_card_back = models.ImageField(upload_to='BussinessLoandocuments/aadhar/')
    pan_card = models.ImageField(upload_to='BussinessLoandocuments/pan/')
    customer_photo = models.ImageField(upload_to='BussinessLoandocuments/customer_photos/')
    business_proof_1 = models.FileField(upload_to='BussinessLoandocuments/business_proofs/')
    business_proof_2 = models.FileField(upload_to='BussinessLoandocuments/business_proofs/',blank=True)
    latest_12_months_bank_statement = models.FileField(upload_to='BussinessLoandocuments/bank_statements/')
    business_office_photo = models.ImageField(upload_to='BussinessLoandocuments/business_office_photos/')
    latest_3_yrs_itr_1 = models.FileField(upload_to='BussinessLoandocuments/itr/',blank=True)
    latest_3_yrs_itr_2 = models.FileField(upload_to='BussinessLoandocuments/itr/',blank=True)
    latest_3_yrs_itr_3 = models.FileField(upload_to='BussinessLoandocuments/itr/',blank=True)
    current_address_proof = models.FileField(upload_to='BussinessLoandocuments/address_proofs/')
    other_document_1 = models.FileField(upload_to='BussinessLoandocuments/other/',blank=True)
    other_document_2 = models.FileField(upload_to='BussinessLoandocuments/other/',blank=True)
   

    co_applicant_aadharFront=models.ImageField(upload_to='BussinessLoandocuments/CoApplicant_adhar_card/front/',null=True,verbose_name="aadharcard front (JPEG/PNG)")
    co_applicant_aadharBack=models.ImageField(upload_to='BussinessLoandocuments/CoApplicant_adhar_card/back/',null=True,verbose_name="aadharcard back (JPEG/PNG)")
    co_applicant_panCard=models.ImageField(upload_to='BussinessLoandocuments/CoApplicant_pan_card/',null=True,verbose_name="pancard (JPEG/PNG)")
    co_applicant_photo=models.ImageField(upload_to='BussinessLoandocuments/CoApplicant_photo/',null=True,verbose_name="Selfie or Photo (JPEG/PNG)")


    def __str__(self):
        return f"Documents{self.loan.id}"
    
    

class Insurance(models.Model):
    insurance_name=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    mobile_number=models.CharField(max_length=15, unique=True)
    email_id = models.EmailField()
    messgae=models.TextField()

    def __str__(self) :
        return f"{self.insurance_name} -{self.name}"




class ApplicationVerification(models.Model):

    loan= models.OneToOneField(BusinessLoan, on_delete=models.CASCADE, related_name='applicationverification',blank=True)
    personal_detail_verifaction=models.CharField(max_length=50,blank=True)
    documents_upload_verification=models.CharField(max_length=50,blank=True)
    documents_verification=models.CharField(max_length=50,blank=True)
    eligibility_check_verification=models.CharField(max_length=50,blank=True)
    bank_login_verification=models.CharField(max_length=50,blank=True)
    loanverification=models.CharField(max_length=50,blank=True,null=True)
    kyc_and_document_verification=models.CharField(max_length=50,blank=True)
    enach_verification=models.CharField(max_length=50,blank=True)
    fieldverification=models.CharField(max_length=50,blank=True)
    incomeverification=models.CharField(max_length=50,blank=True)
    disbursment_verification=models.CharField(max_length=50,blank=True)
    verification_status=models.CharField(max_length=100,blank=True)


  

