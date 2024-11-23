from django.shortcuts import render,redirect
from ravi.models import *
from bhanu.models import Educationalloan
from business.models import BusinessLoan
from seetha.models import CarLoan
from anusha.models import *
from ganesh.models import *
from django.shortcuts import render
from django.http import HttpResponse 
from django.contrib.auth import authenticate, login
import logging

from .models import Application



def dash(request):
    return render(request, 'new_dashboard.html')

def refcount(request):
    business_count = BusinessLoan.objects.filter(dsaref_code__isnull=False).count()
    personal_count = PersonalDetail.objects.filter(dsaref_code__isnull=False).count()
    home_loans_count = CustomerProfile.objects.filter(dsaref_code__isnull=False).count()
    business_loans_count = BusinessLoan.objects.filter(dsaref_code__isnull=False).count()
    car_loans_count = CarLoan.objects.filter(dsaref_code__isnull=False).count()
    educational_loans_count = Educationalloan.objects.filter(dsaref_code__isnull=False).count()
    other_loans_count = LoanApplication.objects.filter(dsaref_code__isnull=False).count()
    credit_card_count = CreditDetail.objects.filter(dsaref_code__isnull=False).count()
    gold_loan_count = Goldloanapplication.objects.filter(dsaref_code__isnull=False).count()
    lap_loans_count = LoanApplication.objects.filter(franrefCode__isnull=False).count()
    total_loans_count = (business_count + personal_count + home_loans_count +
                         lap_loans_count + car_loans_count +
                         educational_loans_count + other_loans_count +
                         credit_card_count + gold_loan_count)


    return render(request, 'application_details.html', {
        'business_count': business_count,
        'personal_count': personal_count,
        'car_loans_count': car_loans_count,
        'home_loans_count': home_loans_count,
        'lap_loans_count': lap_loans_count,
        'educational_loans_count': educational_loans_count,
        'other_loans_count': other_loans_count,
        'credit_card_count': credit_card_count,
        'gold_loan_count': gold_loan_count,
        'total_loans_count': total_loans_count, 


       
    })
    

def dsainscount(request):
    life_insu_count = LifeInsurance.objects.filter(dsaref_code__isnull=False).count()
    gen_insu_count= GeneralInsurance.objects.filter(dsaref_code__isnull=False).count()
    helth_insu_count=healthInsurance.objects.filter(dsaref_code__isnull=False).count()
    all_insu_count =AllInsurance.objects.filter(dsaref_code__isnull=False).count()

    total_insurances =(life_insu_count+gen_insu_count+helth_insu_count+all_insu_count)
    
    return render(request, 'dsains_details.html', {
        'life_insu_count':life_insu_count,
        'gen_insu_count':gen_insu_count,
        'helth_insu_count':helth_insu_count,
        'all_insu_count':all_insu_count,
        'total_insurances': total_insurances,
    })
# /////////////////////////////      franchise   ///////////////////////
                                                            
def fra_refcount(request):
    business_count = BusinessLoan.objects.filter(franrefCode__isnull=False).count()
    personal_count = PersonalDetail.objects.filter(franrefCode__isnull=False).count()


    home_loans_count = CustomerProfile.objects.filter(franrefCode__isnull=False).count()
    business_loans_count = BusinessLoan.objects.filter(franrefCode__isnull=False).count()
    car_loans_count = CarLoan.objects.filter(franrefCode__isnull=False).count()
    educational_loans_count = Educationalloan.objects.filter(franrefCode__isnull=False).count()
    other_loans_count = LoanApplication.objects.filter(franrefCode__isnull=False).count()
    credit_card_count = CreditDetail.objects.filter(franrefCode__isnull=False).count()
    gold_loan_count = Goldloanapplication.objects.filter(franrefCode__isnull=False).count()
    lap_loans_count = LoanApplication.objects.filter(franrefCode__isnull=False).count()

    
    total_loans_count = (business_count + personal_count + home_loans_count +
                         lap_loans_count + car_loans_count +
                         educational_loans_count + other_loans_count +
                         credit_card_count + gold_loan_count)


    return render(request, 'franchisee_applications.html', {
        'business_count': business_count,
        'personal_count': personal_count,
        'car_loans_count': car_loans_count,
        'home_loans_count': home_loans_count,
        'lap_loans_count': lap_loans_count,
        'educational_loans_count': educational_loans_count,
        'other_loans_count': other_loans_count,
        'credit_card_count': credit_card_count,
        'gold_loan_count': gold_loan_count,
        'total_loans_count': total_loans_count, 

    })
    

def farinscount(request):
    life_insu_count = LifeInsurance.objects.filter(franrefCode__isnull=False).count()
    gen_insu_count= GeneralInsurance.objects.filter(franrefCode__isnull=False).count()
    helth_insu_count=healthInsurance.objects.filter(franrefCode__isnull=False).count()
    all_insu_count =AllInsurance.objects.filter(franrefCode__isnull=False).count()

    total_insurances =(life_insu_count+gen_insu_count+helth_insu_count+all_insu_count)
    
    return render(request, 'farins_details.html', {
        'life_insu_count':life_insu_count,
        'gen_insu_count':gen_insu_count,
        'helth_insu_count':helth_insu_count,
        'all_insu_count':all_insu_count,
        'total_insurances': total_insurances,
    })


def sale_refcount(request):
    # Count the number of references for each type of loan
    business_count = BusinessLoan.objects.filter(empref_code__isnull=False).count()
    personal_count = PersonalDetail.objects.filter(empref_code__isnull=False).count()
    home_loans_count = CustomerProfile.objects.filter(empref_code__isnull=False).count()
    lap_loans_count = LoanApplication.objects.filter(empref_code__isnull=False).count()
    car_loans_count = CarLoan.objects.filter(empref_code__isnull=False).count()
    educational_loans_count = Educationalloan.objects.filter(empref_code__isnull=False).count()
    other_loans_count = LoanApplication.objects.filter(empref_code__isnull=False).count()
    credit_card_count = CreditDetail.objects.filter(empref_code__isnull=False).count()
    gold_loan_count = Goldloanapplication.objects.filter(empref_code__isnull=False).count()

    # Calculate total loans count
    total_loans_count = (business_count + personal_count + home_loans_count +
                         lap_loans_count + car_loans_count +
                         educational_loans_count + other_loans_count +
                         credit_card_count + gold_loan_count)

    # Render the template with the counts
    return render(request, 'sales_applications.html', {
        'business_count': business_count,
        'personal_count': personal_count,
        'car_loans_count': car_loans_count,
        'home_loans_count': home_loans_count,
        'lap_loans_count': lap_loans_count,
        'educational_loans_count': educational_loans_count,
        'other_loans_count': other_loans_count,
        'credit_card_count': credit_card_count,
        'gold_loan_count': gold_loan_count,
        'total_loans_count': total_loans_count, 
    })

def saleinscount(request):
    life_insu_count = LifeInsurance.objects.filter(empref_code__isnull=False).count()
    gen_insu_count= GeneralInsurance.objects.filter(empref_code__isnull=False).count()
    helth_insu_count=healthInsurance.objects.filter(empref_code__isnull=False).count()
    all_insu_count =AllInsurance.objects.filter(empref_code__isnull=False).count()

    total_insurances =(life_insu_count+gen_insu_count+helth_insu_count+all_insu_count)
    
    return render(request, 'saleins_details.html', {
        'life_insu_count':life_insu_count,
        'gen_insu_count':gen_insu_count,
        'helth_insu_count':helth_insu_count,
        'all_insu_count':all_insu_count,
        'total_insurances': total_insurances,
    })

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
def all_loans(request):
    employee_id=request.session.get('employee_id')
    username=request.session.get('username')
    # Loan counts
    personal_loans_count = PersonalDetail.objects.count()
    home_loans_count = CustomerProfile.objects.count()
    business_loans_count = BusinessLoan.objects.count()
    car_loans_count = CarLoan.objects.count()
    educational_loans_count = Educationalloan.objects.count()
    other_loans_count = otherloans.objects.count()
    credit_card_count = CreditDetail.objects.count()
    gold_loan_count = Goldloanapplication.objects.count()
    lap_loans_count = LoanApplication.objects.count()

    # Total loan count
    total_loans_count = (
        personal_loans_count + home_loans_count + business_loans_count + 
        car_loans_count + educational_loans_count + other_loans_count + 
        credit_card_count + gold_loan_count+lap_loans_count
    )

    # Insurance counts
    life_insu_count = LifeInsurance.objects.count()
    gen_insu_count = GeneralInsurance.objects.count()
    helth_insu_count = healthInsurance.objects.count()
    all_insu_count = AllInsurance.objects.count()

    # Total insurance count
    total_insu_count = (
        life_insu_count + gen_insu_count + helth_insu_count + all_insu_count
    )

    # Referral loan counts
    business_ref_count = BusinessLoan.objects.filter(dsaref_code__isnull=False).count()
    personal_ref_count = PersonalDetail.objects.filter(dsaref_code__isnull=False).count()
    home_loans_ref_count = CustomerProfile.objects.filter(dsaref_code__isnull=False).count()
    lap_loans_ref_count = LoanApplication.objects.filter(dsaref_code__isnull=False).count()
    car_ref_count = CarLoan.objects.filter(dsaref_code__isnull=False).count()
    educational_ref_count = Educationalloan.objects.filter(dsaref_code__isnull=False).count()
    other_ref_count = LoanApplication.objects.filter(dsaref_code__isnull=False).count()
    credit_ref_count = CreditDetail.objects.filter(dsaref_code__isnull=False).count()
    gold_ref_count = Goldloanapplication.objects.filter(dsaref_code__isnull=False).count()
    
    
  

    # Referral insurance counts
    life_insu_ref_count = LifeInsurance.objects.filter(dsaref_code__isnull=False).count()
    gen_insu_ref_count = GeneralInsurance.objects.filter(dsaref_code__isnull=False).count()
    helth_insu_ref_count = healthInsurance.objects.filter(dsaref_code__isnull=False).count()
    all_insu_ref_count = AllInsurance.objects.filter(dsaref_code__isnull=False).count()


    total_ref_loans_count = (
        business_ref_count + personal_ref_count + home_loans_ref_count + lap_loans_ref_count+ car_ref_count + educational_ref_count + other_ref_count + credit_ref_count + gold_ref_count
    )
    total_ref_insurances_count = (
        life_insu_ref_count + gen_insu_ref_count + helth_insu_ref_count + all_insu_ref_count
    )

# =======================fra=================================================
    business_fref_count = BusinessLoan.objects.filter(franrefCode__isnull=False).count()
    personal_fref_count = PersonalDetail.objects.filter(franrefCode__isnull=False).count()
    home_loans_fref_count = CustomerProfile.objects.filter(franrefCode__isnull=False).count()
    lap_loans_fref_count = LoanApplication.objects.filter(franrefCode__isnull=False).count()
    car_fref_count = CarLoan.objects.filter(franrefCode__isnull=False).count()
    educational_fref_count = Educationalloan.objects.filter(franrefCode__isnull=False).count()
    other_fref_count = LoanApplication.objects.filter(franrefCode__isnull=False).count()
    credit_fref_count = CreditDetail.objects.filter(franrefCode__isnull=False).count()
    gold_fref_count = Goldloanapplication.objects.filter(franrefCode__isnull=False).count()
    
    
  

    # Referral insurance counts
    life_insu_fref_count = LifeInsurance.objects.filter(franrefCode__isnull=False).count()
    gen_insu_fref_count = GeneralInsurance.objects.filter(franrefCode__isnull=False).count()
    helth_insu_fref_count = healthInsurance.objects.filter(franrefCode__isnull=False).count()
    all_insu_fref_count = AllInsurance.objects.filter(franrefCode__isnull=False).count()


    total_fref_loans_count = (
        business_fref_count + personal_fref_count + home_loans_fref_count + lap_loans_fref_count+ car_fref_count + educational_fref_count + other_fref_count + credit_fref_count + gold_fref_count
    )
    total_fref_insurances_count = (
        life_insu_fref_count + gen_insu_fref_count + helth_insu_fref_count + all_insu_fref_count
    )

#..........................sales............................................................
    business_sref_count = BusinessLoan.objects.filter(empref_code__isnull=False).count()
    personal_sref_count = PersonalDetail.objects.filter(empref_code__isnull=False).count()
    home_loans_sref_count = CustomerProfile.objects.filter(empref_code__isnull=False).count()
    lap_loans_sref_count = LoanApplication.objects.filter(empref_code__isnull=False).count()
    car_sref_count = CarLoan.objects.filter(empref_code__isnull=False).count()
    educational_sref_count = Educationalloan.objects.filter(empref_code__isnull=False).count()
    other_sref_count = LoanApplication.objects.filter(empref_code__isnull=False).count()
    credit_sref_count = CreditDetail.objects.filter(empref_code__isnull=False).count()
    gold_sref_count = Goldloanapplication.objects.filter(empref_code__isnull=False).count()
    
    
  

    # Referral insurance counts
    life_insu_sref_count = LifeInsurance.objects.filter(empref_code__isnull=False).count()
    gen_insu_sref_count = GeneralInsurance.objects.filter(empref_code__isnull=False).count()
    helth_insu_sref_count = healthInsurance.objects.filter(empref_code__isnull=False).count()
    all_insu_sref_count = AllInsurance.objects.filter(empref_code__isnull=False).count()


    total_sref_loans_count = (
        business_sref_count + personal_sref_count + home_loans_sref_count + lap_loans_sref_count+ car_sref_count + educational_sref_count + other_sref_count + credit_sref_count + gold_sref_count
    )
    total_sref_insurances_count = (
        life_insu_sref_count + gen_insu_sref_count + helth_insu_sref_count + all_insu_sref_count
    )

    # Context to pass to the template
    context = {
        # Loan data
        'personal_loans_count': personal_loans_count,
        'home_loans_count': home_loans_count,
        'business_loans_count': business_loans_count,
        'car_loans_count': car_loans_count,
        'educational_loans_count': educational_loans_count,
        'other_loans_count': other_loans_count,
        'credit_card_count': credit_card_count,
        'gold_loan_count': gold_loan_count,
        'lap_loans_count': lap_loans_count,
        'total_loans_count': total_loans_count,

        # Insurance data
        'life_insu_count': life_insu_count,
        'gen_insu_count': gen_insu_count,
        'helth_insu_count': helth_insu_count,
        'all_insu_count': all_insu_count,
        'total_insu_count': total_insu_count,

        # dsaReferral loans and insurance data
        'business_ref_count': business_ref_count,
        'personal_ref_count': personal_ref_count,
        'home_loans_ref_count': home_loans_ref_count,
        'lap_loans_ref_count': lap_loans_ref_count,
        'car_ref_count': car_ref_count,
        'educational_ref_count':educational_ref_count,
        'other_ref_count': other_ref_count,
        'credit_ref_count': credit_ref_count,
        'gold_ref_count':  gold_ref_count,
        'total_ref_loans_count': total_ref_loans_count,
        'life_insu_ref_count': life_insu_ref_count,
        'gen_insu_ref_count': gen_insu_ref_count,
        'helth_insu_ref_count': helth_insu_ref_count,
        'all_insu_ref_count': all_insu_ref_count,
        'total_ref_insurances_count': total_ref_insurances_count,


  # fra Referral loans and insurance data
        'business_fref_count': business_fref_count,
        'personal_fref_count': personal_fref_count,
        'home_loans_fref_count': home_loans_fref_count,
        'lap_loans_fref_count': lap_loans_fref_count,
        'car_fref_count': car_fref_count,
        'educational_fref_count':educational_fref_count,
        'other_fref_count': other_fref_count,
        'credit_fref_count': credit_fref_count,
        'gold_fref_count':  gold_fref_count,
        'total_fref_loans_count': total_fref_loans_count,
        'life_insu_fref_count': life_insu_fref_count,
        'gen_insu_fref_count': gen_insu_fref_count,
        'helth_insu_fref_count': helth_insu_fref_count,
        'all_insu_fref_count': all_insu_fref_count,
        'total_fref_insurances_count': total_fref_insurances_count,

        # sale Referral loans and insurance data
        'business_sref_count': business_sref_count,
        'personal_sref_count': personal_sref_count,
        'home_loans_sref_count': home_loans_sref_count,
        'lap_loans_sref_count': lap_loans_sref_count,
        'car_sref_count': car_sref_count,
        'educational_sref_count':educational_sref_count,
        'other_sref_count': other_sref_count,
        'credit_sref_count': credit_sref_count,
        'gold_sref_count':  gold_sref_count,
        'total_sref_loans_count': total_sref_loans_count,
        'life_insu_sref_count': life_insu_sref_count,
        'gen_insu_sref_count': gen_insu_sref_count,
        'helth_insu_sref_count': helth_insu_sref_count,
        'all_insu_sref_count': all_insu_sref_count,
        'total_sref_insurances_count': total_sref_insurances_count,
        'employee_id':employee_id,
        'username':username

    }

    return render(request, 'all_loans.html', context)
import requests
from django.conf import settings
from django.contrib import messages

def login_check(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')

        if not employee_id or not password:
            messages.error(request, "Both employee ID and password are required.")
            return render(request, 'login.html')

        api_url = f"{settings.HR_SOURCE_URL}/api/ho/{employee_id}/loginCheck/"
        payload = {'password': password}

        try:
            # Send POST request to external API with JSON payload
            response = requests.post(api_url, json=payload, headers={"Content-Type": "application/json"})

            # Check the raw response content and status code
            

            if response.status_code == 200:
                response_data = response.json()
                request.session['employee_id'] = response_data['employee_id']
                request.session['username'] = response_data['username']
                request.session['email'] = response_data['email']
                return redirect('all_loans')
            elif response.status_code == 401:
                messages.error(request, "Invalid credentials")
            elif response.status_code == 404:
                messages.error(request, "Employee not found")
            else:
                messages.error(request, "An unexpected error occurred. Please try again later.")

        except requests.RequestException as e:
            messages.error(request, "Could not connect to login server. Please try again.")
            return render(request, 'employeelogin.html')

    return render(request, 'employeelogin.html')


# def logout_view(request):
#     request.session.flush()  # Clears all session data
#     return redirect('login_check')
def Logout(request):

   request.session.clear()
   return redirect('login_check')