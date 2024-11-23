from django.db import models
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
from dateutil.relativedelta import relativedelta


# Create your models here.


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

class edubasicdetailform(models.Model):
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
        return f"{self.fname}"
    
    def save(self,*args,**kwargs):
        self.expiry_at = date.today() + relativedelta(months=3)
        if not self.id:
            max_id = edubasicdetailform.objects.aggregate(models.Max('id'))['id__max']
            if max_id is None:
                self.id = 1001
                self.application_id=f"SLNEL{self.id}"
            else:
                all_ids = set(edubasicdetailform.objects.values_list('id', flat=True))
                for i in range(1001, max_id + 2):
                    if i not in all_ids:
                        self.id = i
                        self.application_id=f"SLNEL{self.id}"
                        break
        super(edubasicdetailform,self).save(*args, **kwargs)
class eduCibilCheck(models.Model):
    user = models.ForeignKey(edubasicdetailform, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6,default='')
    cibil_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)

    def __str__(self):
        return self.cibil_score

    

class Educationalloan(models.Model):
    APPLICANT_TYPE_CHOICES = [
        ('SALARIEDEMPLOYEE', 'Salaried'),
        ('SELFEMPLOYEED', 'SelfEmployeed'),
    ]

    YES_NO_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    RENT_OR_OWN=[
        ('O','OWN'),
        ('R','RENT'),
    ]
   

    basicdetailform=models.OneToOneField(edubasicdetailform, on_delete=models.CASCADE, related_name='eduloan',blank=True,null=True)
    student_name = models.CharField(max_length=100)
    mail_id = models.EmailField()
    mobile_number = models.CharField(max_length=10)
    country = models.CharField(max_length=100,verbose_name="Country Name")
    course = models.CharField(max_length=100)
    university_name = models.CharField(max_length=100,blank=True,null=True)
    score_card = models.FileField(upload_to='score_cards/',blank=True,null=True)
    
    GRE_score = models.DecimalField(max_digits=15, decimal_places=2,blank=True,null=True)
    IELTS_score = models.DecimalField(max_digits=15, decimal_places=2,blank=True,null=True)
    TOEFL_score = models.DecimalField(max_digits=15, decimal_places=2,blank=True,null=True)
    Duolingo_score = models.DecimalField(max_digits=15, decimal_places=2,blank=True,null=True)
    PTE_score = models.DecimalField(max_digits=15, decimal_places=2,blank=True,null=True)
    
    student_work_experience = models.TextField()
    cibil_score = models.IntegerField(blank=True,null=True)
    required_loan_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    backlogs = models.PositiveIntegerField(blank=True,null=True)

    residence_location = models.CharField(max_length=200)
    permanent_location = models.CharField(max_length=200)

    current_adress_type=models.CharField(max_length=1, choices=RENT_OR_OWN,null=True,verbose_name="Current Address Type")
    aadhar_adress_type=models.CharField(max_length=1, choices=RENT_OR_OWN,null=True,verbose_name="Aadhar Address Type")
    own_house = models.CharField(max_length=1, choices=YES_NO_CHOICES,null=True)


    co_applicant_type = models.CharField(max_length=20, choices=APPLICANT_TYPE_CHOICES)

    co_applicant_parent_name = models.CharField(max_length=100,null=True,blank=True)
    co_applicant_company_name = models.CharField(max_length=100, null=True,blank=True)
    co_applicant_salaried_designation = models.CharField(max_length=100, null=True,blank=True)
    co_applicant_salaried_net_pay = models.DecimalField(max_digits=15, decimal_places=2, null=True,blank=True)
    co_applicant_salaried_emis = models.DecimalField(max_digits=15, decimal_places=2, null=True,blank=True,verbose_name="Co applicant running emi in amount per/month")
    co_applicant_salaried_cibil_score = models.IntegerField(null=True,blank=True,verbose_name="Co applicant cibil score")

    co_applicant_self_employed_business_name = models.CharField(max_length=100, null=True,blank=True)
    co_applicant_self_employed_itr_mandatory = models.CharField(max_length=1, choices=YES_NO_CHOICES,null=True,blank=True)
    co_pplicant_self_employed_itr_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    co_applicant_self_employed_business_licence = models.FileField(upload_to='business_licences/', null=True,blank=True)

   
    property_location = models.CharField(max_length=200)
    co_applicant_property_details = models.CharField(max_length=1, choices=YES_NO_CHOICES,verbose_name="Co applicant have own house?")
    property_type = models.CharField(max_length=50, choices=[('House', 'House'), ('Plot', 'Plot'), ('Flat', 'Flat'), ('Apartment', 'Apartment'), ('Open Land', 'Open Land')])
    property_market_value = models.DecimalField(max_digits=15, decimal_places=2,blank=True,null=True)
    property_govt_value = models.DecimalField(max_digits=15, decimal_places=2,blank=True,null=True)
    property_local_government_body = models.CharField(max_length=100,blank=True,null=True)

    # common Fields
    dsaref_code=models.CharField(max_length=100,null=True,blank=True)
    franrefCode=models.CharField(max_length=100,null=True,blank=True)
    empref_code=models.CharField(max_length=100,null=True,blank=True)

    ref1name=models.CharField(max_length=100,null=True,verbose_name="Reference1 Name",blank=True)
    ref1mobilenumber=models.CharField(max_length=100,null=True,verbose_name="Reference1 Mobile Number",blank=True)
    ref2name=models.CharField(max_length=100,null=True,verbose_name="Reference2 Name",blank=True)
    ref2mobilenumber=models.CharField(max_length=100,null=True,verbose_name="Reference2 Mobile Number",blank=True)


    application_loan_type=models.CharField(max_length=100,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True,null=True,blank=True)
    application_id=models.CharField(max_length=200,unique=True,blank=True,null=True)
    required_loan_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    # common Fields

    def __str__(self):
        return f"{self.id}---{self.student_name}"
    

    def save(self,*args,**kwargs):
        self.name=self.student_name 

        self.application_loan_type="Education"
        if not self.franrefCode:
            self.franrefCode="SLNBR1001"
        if not self.id:
            
            max_id = Educationalloan.objects.aggregate(models.Max('id'))['id__max']
            if max_id is None:
                self.id = 1001
               
            else:
                all_ids = set(Educationalloan.objects.values_list('id', flat=True))
                for i in range(1001, max_id + 2):
                    if i not in all_ids:
                        self.id = i
                        
                        break
        super(Educationalloan,self).save(*args, **kwargs)
    
   




class Educationloan_document_upload(models.Model):
        loan = models.OneToOneField(Educationalloan, on_delete=models.CASCADE, related_name='personal_details')
        

        adhar_card_front = models.ImageField(
        upload_to='EDUdocuments/adhar_card/front/',
        
    )
        adhar_card_back = models.ImageField(
        upload_to='EDUdocuments/adhar_card/back/',
       
        
    )
        pan_card = models.ImageField(
        upload_to='EDUdocuments/pan_card/',

       
    )
        customer_photo = models.ImageField(
        upload_to='EDUdocuments/customer_photo/',verbose_name="Student Photo or Selfie"
        
        
    )
        pay_slip_1 = models.FileField(
        upload_to='EDUdocuments/pay_slips/',verbose_name="Co applicant salary pay slip/Business Proof"
       
    )
        pay_slip_2 = models.FileField(
        upload_to='EDUdocuments/pay_slips/',blank=True
       
    )
        pay_slip_3 = models.FileField(
        upload_to='EDUdocuments/pay_slips/',blank=True
       
    )
        bank_statement = models.FileField(
        upload_to='EDUdocuments/bank_statements/',
       
    )
        employee_id_card = models.FileField(
        upload_to='EDUdocuments/employee_id_cards/',blank=True
       
    )
        
        co_applicant_aadharFront=models.ImageField(upload_to='EDUdocuments/CoApplicant_adhar_card/front/',null=True,verbose_name="aadharcard front (JPEG/PNG)")
        co_applicant_aadharBack=models.ImageField(upload_to='EDUdocuments/CoApplicant_adhar_card/back/',null=True,verbose_name="aadharcard back (JPEG/PNG)")
        co_applicant_panCard=models.ImageField(upload_to='EDUdocuments/CoApplicant_pan_card/',null=True,verbose_name="pancard (JPEG/PNG)")
        co_applicant_photo=models.ImageField(upload_to='EDUdocuments/CoApplicant_photo/',null=True,verbose_name="Selfie or Photo (JPEG/PNG)")



        
    

        def __str__(self):
         return f"{self.employee_id_card}"





class ApplicationVerification(models.Model):

    loan= models.OneToOneField(Educationalloan, on_delete=models.CASCADE, related_name='applicationverification',blank=True)
    personal_detail_verifaction=models.CharField(max_length=50,blank=True)
    documents_upload_verification=models.CharField(max_length=50,blank=True)
    documents_verification=models.CharField(max_length=50,blank=True)
    eligibility_check_verification=models.CharField(max_length=50,blank=True)
    bank_login_verification=models.CharField(max_length=50,blank=True)
    loanverification=models.CharField(max_length=50,blank=True,null=True)
    kyc_and_document_verification=models.CharField(max_length=50,blank=True)
    enach_verification=models.CharField(max_length=50,blank=True)
    field_verification=models.CharField(max_length=50,blank=True)
    income_verification=models.CharField(max_length=50,blank=True)
    disbursment_verification=models.CharField(max_length=50,blank=True)
    verification_status=models.CharField(max_length=100,blank=True)
    
from datetime import date, timedelta


class Edudisbursementdetails(models.Model):
    verification = models.OneToOneField(Educationalloan, on_delete=models.CASCADE,blank=True, related_name='disbursementdetail',default='')
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
    
    
    

