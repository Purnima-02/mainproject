from django.db import models
from django.utils import timezone
import re
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator
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


class CLBasicDetail(models.Model):
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

    #created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.application_id}"

    def save(self, *args, **kwargs):
        self.expiry_at = date.today() + relativedelta(months=3)

        if not self.application_id:
            last_entry = CLBasicDetail.objects.filter(application_id__startswith='SLNCL').aggregate(Max('application_id'))
            last_number = last_entry.get('application_id__max', None)

            if last_number:
                try:
                    last_number_int = int(last_number[5:])  
                    new_number = last_number_int + 1
                except ValueError:
                    new_number = 1001
            else:
                new_number = 1001

            self.application_id = f"SLNCL{new_number:04d}"

        print(f"Saving CLBasicDetail with application_id: {self.application_id}")
        
        
        super(CLBasicDetail, self).save(*args, **kwargs)
from datetime import timedelta
class carCibilCheck(models.Model):
    user = models.ForeignKey(CLBasicDetail, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6,default='')
    cibil_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)

class CarLoan(models.Model):

    CAR_LOAN_TYPE_CHOICES = [
    ('NEW', 'New'),
    ('USED', 'Used')
    ]

    INCOME_SOURCE_CHOICES = [
        ('Job', 'Job'),
        ('Business', 'Business'),
    ]

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

    COMPANY_TYPE_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
        ('government', 'Government'),
        ('self_employed', 'Self Employed'),
        ('other', 'Other')
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
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    ADDRESS_TYPE_CHOICES = [
        ('RENT', 'Rent'),
        ('OWN', 'Own'),
    ]
    
    carbasic_detail = models.OneToOneField(CLBasicDetail, on_delete=models.CASCADE,blank=True,null=True)
    # personal details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=10)
    # car loan type
    car_loan_type = models.CharField(max_length=4, choices=CAR_LOAN_TYPE_CHOICES,null=True )
    # used car
    car_vehicle_no = models.CharField(max_length=15,null=True,blank=True)
    car_company_name = models.CharField(max_length=50,null=True,blank=True)
    variant = models.CharField(max_length=50, null=True,blank=True)
    model_year = models.IntegerField(blank=True, null=True)
    existing_loan = models.BooleanField(default=False)
    existing_loan_bank_name = models.CharField(max_length=100, blank=True, null=True)
    existing_loan_amount_in_rs =models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    # new car
    car_purchase_value_in_RS = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    quotation_value_on_ex_showroom = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    downpayment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    showroom_quotation = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    varient = models.CharField(max_length=50, null=True,blank=True)
    car_model_year = models.IntegerField(blank=True, null=True)
    # common fields    
    pan_card_number = models.CharField(max_length=10)
    aadhar_card_number = models.CharField(max_length=12)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    email_id = models.EmailField(blank=True)
    current_address = models.TextField()
    current_address_pincode = models.IntegerField()
    current_address_type = models.CharField(max_length=4,choices=ADDRESS_TYPE_CHOICES,null=True,blank=True)
    aadhar_address_type = models.CharField(max_length=4,choices=ADDRESS_TYPE_CHOICES,null=True,blank=True)
    aadhar_address = models.TextField()
    aadhar_pincode = models.IntegerField()
    running_emis_amount_per_month = models.DecimalField(max_digits=15, decimal_places=2)
    required_loan = models.DecimalField(max_digits=15, decimal_places=2, null=True,blank=True)
    #income source
    income_source = models.CharField(max_length=10, choices=INCOME_SOURCE_CHOICES)
    #job fields
    net_salary_per_month = models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES,blank=True)
    job_designation = models.CharField(max_length=100,null=True,blank=True)
    job_joining_date = models.DateField(null=True,blank=True)
    job_location = models.CharField(max_length=100,null=True,blank=True)
    total_job_experience_in_months = models.IntegerField(null=True, blank=True)
    work_email = models.EmailField(blank=True)
    office_address = models.TextField(null=True,blank=True)
    #bussiness fiedls
    business_name = models.CharField(max_length=200,null=True,blank=True)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES,null=True,blank=True)
    net_income_per_month = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    business_establishment_date = models.DateField(null=True,blank=True)
    gst_certificate = models.CharField(max_length=3, choices=YES_NO_CHOICES,blank=True, null=True)
    gst_number = models.CharField(max_length=15,blank=True)
    mother_name = models.CharField(max_length=100,null=True,blank=True)
    father_name = models.CharField(max_length=100,null=True,blank=True)
    nature_of_business = models.CharField(max_length=200,null=True,blank=True)
    turnover_in_lakhs_per_year = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    business_address = models.TextField(null=True,blank=True)
    business_address_pincode = models.PositiveBigIntegerField(null=True,blank=True)
    ref1_person_name = models.CharField(max_length=100,null=True,blank=True)
    ref_1_person_mobile_number = models.CharField(max_length=10,null=True,blank=True)
    ref2_person_name = models.CharField(max_length=100,null=True,blank=True)
    ref_2_person_mobile_number = models.CharField(max_length=10,null=True,blank=True)
    remarks = models.TextField(null=True,blank=True)

    
    # common Fields
    dsaref_code=models.CharField(max_length=100,null=True,blank=True)
    franrefCode=models.CharField(max_length=100,null=True,blank=True)
    empref_code=models.CharField(max_length=100,null=True,blank=True)
    application_loan_type=models.CharField(max_length=100,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True,null=True,blank=True)
    application_id=models.CharField(max_length=200,unique=True,blank=True,null=True)
    required_loan_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    

    def __str__(self):
        return f"{self.id}={self.first_name} {self.last_name}"
        
  

    def save(self, *args, **kwargs):
        if not self.franrefCode:
            self.franrefCode="SLNBR1001"
        if self.car_vehicle_no is not None:
            self.application_loan_type="USED CAR"

        else:
            self.application_loan_type="NEW CAR"

        self.name=self.first_name+self.last_name
        
        # Only generate a new application_id if it doesn't exist
        if not self.application_id:
            max_id = CarLoan.objects.aggregate(models.Max('id'))['id__max']
            if max_id is None:
                self.id = 1001  # Start the ID from 1001
            else:
                all_ids = set(CarLoan.objects.values_list('id', flat=True))
                # Find the first available ID greater than or equal to 1001
                for i in range(1001, max_id + 2):
                    if i not in all_ids:
                        self.id = i
                        break

            # Now generate the application_id with the SLNCL prefix
            self.application_id = f"SLNCL{self.id}"

        super(CarLoan, self).save(*args, **kwargs)


class CarLoanDocument(models.Model):
    loan = models.OneToOneField(CarLoan, on_delete=models.CASCADE, related_name='CarLoandocuments',blank=True)
    car_rc_front = models.ImageField(upload_to='documents/')
    car_rc_back = models.ImageField(upload_to='documents/')
    aadhaar_card_front = models.ImageField(upload_to='documents/')
    aadhaar_card_back = models.ImageField(upload_to='documents/')
    pan_card = models.ImageField(upload_to='documents/')
    customer_photo = models.ImageField(upload_to='documents/')
    #job documents
    payslip1 = models.FileField(upload_to='documents/',null=True,blank=True)
    payslip2 = models.FileField(upload_to='documents/',blank=True)
    payslip3 = models.FileField(upload_to='documents/' ,blank=True)
    bank_statement = models.FileField(upload_to='documents/',null=True,blank=True)
    employee_id_card = models.FileField(upload_to='documents/',blank=True)
    #business documents
    business_proof_1 = models.FileField(upload_to='documents/',null=True,blank=True)
    business_proof_2 = models.FileField(upload_to='documents/',blank=True)
    latest_12_months_bank_statement = models.FileField(upload_to='documents/',null=True,blank=True)
    business_office_photo = models.FileField(upload_to='documents/',null=True,blank=True)
    latest_3_yrs_itr_1 = models.FileField(upload_to='documents/',null=True,blank=True)
    latest_3_yrs_itr_2 = models.FileField(upload_to='documents/',null=True,blank=True)
    latest_3_yrs_itr_3 = models.FileField(upload_to='documents/',blank=True)
    current_address_proof = models.FileField(upload_to='documents/',blank=True)
    existing_loan_statement = models.FileField(upload_to='documents/',null=True,blank=True)
    other_document_1 = models.FileField(upload_to='documents/',blank=True)
    other_document_2 = models.FileField(upload_to='documents/',blank=True)
    

    def __str__(self):
        return f"Documents for {self.loan.id}"


class CarApplicationVerification(models.Model):
    
    application_date = models.DateTimeField(auto_now_add=True)
    loan= models.OneToOneField(CarLoan, on_delete=models.CASCADE, related_name='applicationverification',blank=True)
    personal_detail_verification=models.CharField(max_length=50,blank=True)
    documents_upload_verification=models.CharField(max_length=50,blank=True)
    documents_verification=models.CharField(max_length=50,blank=True)
    eligibility_check_verification=models.CharField(max_length=50,blank=True)
    bank_login_verification=models.CharField(max_length=50,blank=True)
    valuation=models.CharField(max_length=50,blank=True)
    credit_manager_inspection=models.CharField(max_length=50,blank=True)
    kyc_and_documents_verification=models.CharField(max_length=50,blank=True)
    enach_verification=models.CharField(max_length=50,blank=True)
    disbursment_verification=models.CharField(max_length=50,blank=True)
    post_documentation=models.CharField(max_length=50,blank=True)
    rc_card_submission =models.CharField(max_length=50,blank=True)
    verification_status=models.CharField(max_length=50,blank=True)
    
   #verification_status
    def __str__(self):
         return f"Applicant Document: {self.personal_detail_verification}"
    


from datetime import date

class CarDisbursementDetails(models.Model):
    verification = models.OneToOneField(CarLoan, on_delete=models.CASCADE,blank=True, related_name='disbursementdetail',default='')
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
    
    

    def __str__(self):
        return f"{self.bank_nbfc_name}-{self.verification.carbasic_detail}"