from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
import logging
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from ravi.models import *
from business.models import *
from bhanu.models import *
from bhanu.forms import *
from business.forms import *
from seetha.models import CarLoan
from ganesh.models import CreditDetail

from django.views.decorators.csrf import csrf_exempt

# =================================goldloan start===================================

import requests
import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse

APIID = "AP100034"
TOKEN = "6b549eed-2af0-488c-a2e1-3d10f37f11c6"

def goldbasicdetails(request,instance_id=None):
    instance = get_object_or_404(goldbasicdetailform, id=instance_id) if instance_id else None
    application_id=None

    if request.method == 'POST':
        form = goldBasicDetailForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            user_details = form.save()
            application_id=user_details.application_id
            
            # Bhanu
            request.session['GoldLoanExpiryDate']=str(user_details.expiry_at)
            # Bhanu
            
            orderid = str(uuid.uuid4())
            request.session['application_id']=application_id
            destinationUrl=reverse('goldloan')
            request.session['Goldafterurl']=destinationUrl
            request.session['goldAppliId']=True
            request.session['orderid'] = orderid
            request.session['user_id'] = user_details.id
            request.session['mobile_number']=user_details.phone_number
            request.session['pan_num']=user_details.pan_num
            
            payload = {
                "apiid": APIID,
                "token": TOKEN,
                "methodName": "UATCreditScoreOTP",
                "orderid": orderid,
                "phone_number": user_details.phone_number
            }

            response = requests.post("https://apimanage.websoftexpay.com/api/Uat_creditscore_OTP.aspx", json=payload)
            data = response.json()

            if response.status_code == 200 and data.get("status") == "success":
                otp = data["data"].split(":")[1]
                user_details.otp = otp  
                user_details.orderid = orderid
                user_details.save()
            
                request.session['otp']=otp
                return redirect('goldfetchcreditreport')
            else:
                return JsonResponse({"status": "error", "message": data.get("mess", "Failed to generate OTP")})
    else:
        form = BasicDetailForm()

    return render(request, 'customer/goldbasicdetail.html', {'form': form})
def gold_fetch_credit_report(request):
    otp=request.session.get('otp')
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user_details = goldbasicdetailform.objects.get(id=user_id)
        otp = request.POST.get('otp').strip()  
       
        payload = {
            "apiid": APIID,
            "token": TOKEN,
            "methodName": "UATcreditscore",
            "orderid": request.session.get('orderid'),  
            "fname": user_details.fname,
            "lname": user_details.lname,
            "Dob": user_details.Dob.isoformat() if isinstance(user_details.Dob, date) else user_details.Dob,
            "phone_number": user_details.phone_number,
            "pan_num": user_details.pan_num,
            "application_id":user_details.application_id,
            "otp": otp 
            
        }
        
        response = requests.post("https://apimanage.websoftexpay.com/api/Uat_credit_score.aspx", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                if 'Dob' in data["data"]:
                    dob = data["data"]['Dob']
                    if isinstance(dob, date):
                        data["data"]['Dob'] = dob.isoformat()
                credit_score = data["data"].get("ScoreValue")
                
                if credit_score:
                    loan_application, created = goldCibilCheck.objects.get_or_create(user=user_details)
                    if loan_application:
                        loan_application.cibil_score = credit_score
                        loan_application.save()
                    return render(request, 'customer/goldcibil_score.html', {'credit_score': credit_score, 'application_id': user_details.application_id})
            else:
                return JsonResponse({"status": "error", "message": data["mess"]})
        else:
            return JsonResponse({"status": "error", "message": "Failed to fetch credit report"})

    return render(request, 'customer/goldbasicdetail.html',{'otp':otp})

 
def goldloanapplication(request):
    mobile_number = request.session.get('mobile_number','')  
    pan_number=request.session.get('pan_num','')
    
     # Bhanu
    refCode=None
    francrefCode=None
    if request.GET.get('refCode'):
        
        refCode=request.GET.get('refCode')
    if request.GET.get('franrefCode'):
       francrefCode=request.GET.get('franrefCode')
    # Bhanu

    if request.method == 'POST':
        form = goldform(request.POST, request.FILES)
        if form.is_valid():
            loan = form.save(commit=False)
            
             # Bhanu
    
            if refCode:
              if refCode.startswith('SLNDSA'):
                 loan.dsaref_code=refCode
                 loan.franrefCode=francrefCode
              elif refCode.startswith('SLNEMP'):
                 loan.empref_code=refCode
                 loan.franrefCode=francrefCode
              else:
                 loan.empref_code=refCode
                 loan.franrefCode=francrefCode
            else:
                 loan.franrefCode=francrefCode

            # Bhanu
            
            goldbasicdetail=goldbasicdetailform.objects.filter(phone_number=mobile_number).order_by('-application_id').first()
            if goldbasicdetail:
                loan.goldbasicdetail=goldbasicdetail
                loan.mobile_number=mobile_number
                loan.Pan_number=pan_number  
                loan.save()
                request.session['loanid'] = loan.id
                
                # Bhanu
                
                if refCode:
                      if refCode.startswith('SLNDSA'):
                        EducommonDsaLogic(request,refCode,loan)
                 
                      elif refCode.startswith('SLNEMP'):
                    
                        eduSalesLogic(request,refCode,loan)
                      else:
                        superAdmin(request,refCode,loan)
                
                elif francrefCode:
                    franchiseLogic(request,francrefCode,loan)
                      
                
                destinationUrl=reverse('goldsuccess', kwargs={'application_id': goldbasicdetail.application_id})
                request.session['goldafterurl']=destinationUrl
                
                # Bhanu
                    
                return redirect('goldsuccess', application_id=goldbasicdetail.application_id)
    else:
        form = goldform()
    return render(request, 'customer/goldloan.html', {'form': form, 'mobile_number':mobile_number,'pan_number': pan_number})
def goldsuccess(request, application_id):
    
    goldapp=get_object_or_404(Goldloanapplication,goldbasicdetail__application_id=application_id)
    context = {
        
        'application_id': application_id,
        'goldapp':goldapp,   
    }
    return render(request, 'customer/goldsuccess.html', context)

# ========================================goldloan end ===============================

# ===========================otherloan start================================

import requests
import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse

APIID = "AP100034"
TOKEN = "6b549eed-2af0-488c-a2e1-3d10f37f11c6"
def otherbasicdetails(request,instance_id=None):
    instance = get_object_or_404(otherbasicdetailform, id=instance_id) if instance_id else None
    application_id=None

    if request.method == 'POST':
        form = OtherBasicDetailForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            user_details = form.save()
            application_id=user_details.application_id
            orderid = str(uuid.uuid4())
            request.session['application_id']=application_id
            
            # Bhanu
            request.session['OtherLoanExpiryDate']=str(user_details.expiry_at)
            # Bhanu
            
            destinationUrl=reverse('otherloan')
            request.session['otherafterurl']=destinationUrl
            request.session['otherAppliId']=True
            request.session['orderid'] = orderid
            request.session['user_id'] = user_details.id
            request.session['mobile_number']=user_details.phone_number
            request.session['pan_num']=user_details.pan_num
            
            payload = {
                "apiid": APIID,
                "token": TOKEN,
                "methodName": "UATCreditScoreOTP",
                "orderid": orderid,
                "phone_number": user_details.phone_number
            }

            response = requests.post("https://apimanage.websoftexpay.com/api/Uat_creditscore_OTP.aspx", json=payload)
            data = response.json()

            if response.status_code == 200 and data.get("status") == "success":
                otp = data["data"].split(":")[1]
                user_details.otp = otp  
                user_details.orderid = orderid
                user_details.save()
               
                request.session['otp']=otp
                return redirect('otherfetchcreditreport')
            else:
                return JsonResponse({"status": "error", "message": data.get("mess", "Failed to generate OTP")})
    else:
        form = OtherBasicDetailForm()

    return render(request, 'customer/otherbasicdetail.html', {'form': form})
def other_fetch_credit_report(request):
    otp=request.session.get('otp')
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user_details = otherbasicdetailform.objects.get(id=user_id)
        otp = request.POST.get('otp').strip()  
        
        payload = {
            "apiid": APIID,
            "token": TOKEN,
            "methodName": "UATcreditscore",
            "orderid": request.session.get('orderid'),  
            "fname": user_details.fname,
            "lname": user_details.lname,
            "Dob": user_details.Dob.isoformat() if isinstance(user_details.Dob, date) else user_details.Dob,
            "phone_number": user_details.phone_number,
            "pan_num": user_details.pan_num,
            "application_id":user_details.application_id,
            "otp": otp 
            
        }
        
        response = requests.post("https://apimanage.websoftexpay.com/api/Uat_credit_score.aspx", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                if 'Dob' in data["data"]:
                    dob = data["data"]['Dob']
                    if isinstance(dob, date):
                        data["data"]['Dob'] = dob.isoformat()
                credit_score = data["data"].get("ScoreValue")
                
                if credit_score:
                    loan_application, created = otherCibilCheck.objects.get_or_create(user=user_details)
                    if loan_application:
                        loan_application.cibil_score = credit_score
                        loan_application.save()
                    return render(request, 'customer/othercibil_score.html', {'credit_score': credit_score, 'application_id': user_details.application_id})
            else:
                return JsonResponse({"status": "error", "message": data["mess"]})
        else:
            return JsonResponse({"status": "error", "message": "Failed to fetch credit report"})

    return render(request, 'customer/otherbasicdetail.html',{'otp':otp})



def otherloanapplication(request):
    mobile_number = request.session.get('mobile_number', '') 
    pan_number = request.session.get('pan_num', '') 

    refCode = None
    francrefCode = None
    if request.GET.get('refCode'):
        refCode = request.GET.get('refCode')
    if request.GET.get('franrefCode'):
        francrefCode = request.GET.get('franrefCode')

    if request.method == 'POST':
        form = otherloansform(request.POST, request.FILES)
        if form.is_valid():
            loan = form.save(commit=False)

            if refCode:
                if refCode.startswith('SLNDSA'):
                    loan.dsaref_code = refCode
                    loan.franrefCode = francrefCode
                elif refCode.startswith('SLNEMP'):
                    loan.empref_code = refCode
                    loan.franrefCode = francrefCode
                else:
                    loan.empref_code = refCode
                    loan.franrefCode = francrefCode
            else:
                if francrefCode:
                    loan.franrefCode = francrefCode

            otherbasicdetail = otherbasicdetailform.objects.filter(phone_number=mobile_number).order_by('-application_id').first()
            
            if otherbasicdetail:
                loan.otherbasicdetail = otherbasicdetail
                loan.mobile_number = mobile_number
                loan.pan_number = pan_number
                loan.save()  
                
                request.session['loanid'] = loan.id
                # Bhanu
                if refCode:
                      if refCode.startswith('SLNDSA'):
                        EducommonDsaLogic(request,refCode,loan)
                 
                      elif refCode.startswith('SLNEMP'):
                        eduSalesLogic(request,refCode,loan)
                      else:
                        superAdmin(request,refCode,loan)
                        
                elif francrefCode:
                    franchiseLogic(request,francrefCode,loan)
                destinationUrl = reverse('othersuccess', kwargs={'application_id': otherbasicdetail.application_id})
                request.session['lapafterurl'] = destinationUrl

                return redirect('othersuccess', application_id=otherbasicdetail.application_id)
            else:
              
                return redirect('otherbasicdetail')
    else:
        form = otherloansform()

    return render(request, 'customer/otherloan.html', {'form': form, 'mobile_number': mobile_number, 'pan_number': pan_number})
def othersuccess(request, application_id):
    goldapp=get_object_or_404(otherloans,otherbasicdetail__application_id=application_id)
    context = {
        
        'application_id': application_id,
        'goldapp':goldapp,
        
    }
    return render(request, 'customer/othersuccess.html', context)
def otherview(request):
    customer_profiles = otherloans.objects.all()

    profiles_with_cibil = []

    for profile in customer_profiles:
        user_details = profile.otherbasicdetail

        cibil_record = otherCibilCheck.objects.filter(user=user_details).first()
        cibil_score = cibil_record.cibil_score if cibil_record else None
        
        profiles_with_cibil.append({
            'profile': profile,
            'cibil_score': cibil_score
        })

    return render(request, 'customer/viewotherloan.html', {
        'profiles_with_cibil': profiles_with_cibil  
    })
# ============================================================otherloan  end======================

APIID = "AP100034"
TOKEN = "6b549eed-2af0-488c-a2e1-3d10f37f11c6"

def basicdetails(request,instance_id=None):
    instance = get_object_or_404(basicdetailform, id=instance_id) if instance_id else None
    application_id=None

    if request.method == 'POST':
        form = BasicDetailForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            user_details = form.save()
            application_id=user_details.application_id
            
            # Bhanu
            request.session['LAPLoanExpiryDate']=str(user_details.expiry_at)
            # Bhanu
            
            orderid = str(uuid.uuid4())
            request.session['application_id']=application_id
            destinationUrl=reverse('lapapply')
            request.session['Lapafterurl']=destinationUrl
            request.session['lapAppliId']=True
            request.session['orderid'] = orderid
            request.session['user_id'] = user_details.id
            request.session['mobile_number'] = user_details.phone_number
            request.session['pan_num']=user_details.pan_num

            
            payload = {
                "apiid": APIID,
                "token": TOKEN,
                "methodName": "UATCreditScoreOTP",
                "orderid": orderid,
                "phone_number": user_details.phone_number
            }

            response = requests.post("https://apimanage.websoftexpay.com/api/Uat_creditscore_OTP.aspx", json=payload)
            data = response.json()

            if response.status_code == 200 and data.get("status") == "success":
                otp = data["data"].split(":")[1]
                user_details.otp = otp  
                user_details.orderid = orderid
                user_details.save()
               
                request.session['otp']=otp
                return redirect('fetchcreditreport')
            else:
                return JsonResponse({"status": "error", "message": data.get("mess", "Failed to generate OTP")})
    else:
        form = BasicDetailForm()

    return render(request, 'customer/basicdetailform.html', {'form': form})
def fetch_credit_report(request):
    otp=request.session.get('otp')
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user_details = basicdetailform.objects.get(id=user_id)
        otp = request.POST.get('otp').strip()  
       
        payload = {
            "apiid": APIID,
            "token": TOKEN,
            "methodName": "UATcreditscore",
            "orderid": request.session.get('orderid'),  
            "fname": user_details.fname,
            "lname": user_details.lname,
            "Dob": user_details.Dob.isoformat() if isinstance(user_details.Dob, date) else user_details.Dob,
            "phone_number": user_details.phone_number,
            "pan_num": user_details.pan_num,
            "application_id":user_details.application_id,
            "otp": otp 
            
        }
        
        response = requests.post("https://apimanage.websoftexpay.com/api/Uat_credit_score.aspx", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                if 'Dob' in data["data"]:
                    dob = data["data"]['Dob']
                    if isinstance(dob, date):
                        data["data"]['Dob'] = dob.isoformat()
                credit_score = data["data"].get("ScoreValue")
                
                if credit_score:
                    # Save the credit score to the corresponding LoanApplication
                    loan_application, created = CibilCheck.objects.get_or_create(user=user_details)
                    if loan_application:
                        loan_application.cibil_score = credit_score
                        loan_application.save()
                    return render(request, 'customer/cibil_score.html', {'credit_score': credit_score, 'application_id': user_details.application_id})
            else:
                return JsonResponse({"status": "error", "message": data["mess"]})
        else:
            return JsonResponse({"status": "error", "message": "Failed to fetch credit report"})

    return render(request, 'customer/basicdetailform.html',{'otp':otp})
def lap_add(request):
    mobile_number = request.session.get('mobile_number','') 
    pan_number=request.session.get('pan_num','') 
    
    # Bhanu
    refCode=None
    francrefCode=None
    if request.GET.get('refCode'):
       
        refCode=request.GET.get('refCode')
    if request.GET.get('franrefCode'):
       francrefCode=request.GET.get('franrefCode')
    # Bhanu

    if request.method == 'POST':
        form = LoanApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            loan = form.save(commit=False)  
      
            # Bhanu
    
            if refCode:
              if refCode.startswith('SLNDSA'):
                 
                 loan.dsaref_code=refCode
                 loan.franrefCode=francrefCode
              elif refCode.startswith('SLNEMP'):
                 loan.empref_code=refCode
                 loan.franrefCode=francrefCode
              else:
                 loan.empref_code=refCode
                 loan.franrefCode=francrefCode
            else:
                
                 loan.franrefCode=francrefCode

            # Bhanu
            basic_detail=basicdetailform.objects.filter(phone_number=mobile_number).order_by('-application_id').first()
            if basic_detail:
                    loan.basic_detail = basic_detail
                    loan.mobile_number = mobile_number
                    loan.pan_card_number = pan_number
                    loan.save()  
                    request.session['loanid'] = loan.application_id
                    
                    # Bhanu
                    if refCode:
                      if refCode.startswith('SLNDSA'):
                        EducommonDsaLogic(request,refCode,loan)
                 
                      elif refCode.startswith('SLNEMP'):
                        eduSalesLogic(request,refCode,loan)
                      else:
                        superAdmin(request,refCode,loan)
                
                    elif francrefCode:
                        franchiseLogic(request,francrefCode,loan)
                    destinationUrl = reverse('lapdoc', kwargs={'application_id': basic_detail.application_id})
                    request.session['lapafterurl'] = destinationUrl
                    # Bhanu
                    return redirect('lapdoc', application_id=basic_detail.application_id)
    else:
        form = LoanApplicationForm()

    return render(request, 'customer/LAPform.html', {'form': form, 'mobile_number': mobile_number,'pan_number':pan_number})
from django.shortcuts import render

# Bhanu
def franchiseLogic(request,refCode,businessObj):
                getDsa = requests.get(f"{settings.FRANCHISE_URL}franchise/api/getDsa/{refCode}") 
                if getDsa.status_code == 200:
                    dsaid_list = getDsa.json()
                    if dsaid_list:
                        dsaid = dsaid_list[0]  
                    else:
                        return HttpResponse(f"No FRANCHISE data found with Id: {refCode}")
                    
                    context = {
                        'dsa': dsaid.get('id'),
                        'cust_applicationId': businessObj.application_id
                    }
                    response = requests.post(f"{settings.FRANCHISE_URL}franchise/api/DSA_Appli_Viewsets/", json=context)
                    
                    if response.status_code != 200 or response.status_code != 201:
                        
                        return HttpResponse(f"Invalid Data..{response.status_code}---{response.text}")
                else:
                    return HttpResponse(f"No Franchise Found with Id: {businessObj.dsaref_code}")

def EducommonDsaLogic(request,refCode,loan):
                getDsa = requests.get(f"{settings.DSA_URL}dsa/api/getDsa/{refCode}") #http://127.0.0.1:8001/dsa/getDsa/SLN1001
                if getDsa.status_code == 200:
                    dsaid_list = getDsa.json()
                    if dsaid_list:
                        dsaid = dsaid_list[0]  # ExtrAct the first dictionary
                    else:
                        return HttpResponse(f"No DSA data found with Id: {refCode}")
                    
                    context = {
                        'dsa': dsaid.get('id'),
                        'cust_applicationId': loan.application_id
                    }
                    response = requests.post(f"{settings.DSA_URL}dsa/api/DSA_Appli_Viewsets/", json=context)
                    
                    if response.status_code == 200 or response.status_code == 201:
                        return redirect('upload-documents')
                    else:
                        return HttpResponse(f"Invalid Data..{response.status_code}---{response.text}")
                else:
                    return HttpResponse(f"No DSA Found with Id: {loan.dsaref_code}")
             
def eduSalesLogic(request,refCode,loan):
                getDsa1 = requests.get(f"{settings.SALES_URL}sa/api/getDsa/{refCode}") #http://127.0.0.1:8004/dsa/getDsa/SLN1001
              
                if getDsa1.status_code == 200:
                    dsaid_list1 = getDsa1.json()
                    if dsaid_list1:
                        dsaidd = dsaid_list1[0]  # ExtrAct the first dictionary
                    else:
                        return HttpResponse(f"No Sales data found with Id: {refCode}")
                  
                    context = {
                        'dsa': dsaidd.get('id'),
                        'cust_applicationId': loan.application_id
                    }
                    response = requests.post(f"{settings.SALES_URL}sa/api/DSA_Appli_Viewsets/", json=context)
                   
                    if response.status_code == 200 or response.status_code == 201:
                        return redirect('upload-documents')
                    else:
                        return HttpResponse(f"Invalid Data..{response.status_code}---{response.text}")
                else:
                    return HttpResponse(f"No Sales Found with Id: {refCode}")

def superAdmin(request,refCode,loan):
               
                getDsa = requests.get(f"{settings.SUPERADMIN_URL}/superadmin/app1/getAdmin/{refCode}") #http://127.0.0.1:8001/dsa/getDsa/SLN1001
                if getDsa.status_code == 200:
                    dsaid_list = getDsa.json()
                    if dsaid_list:
                        
                        dsaid = dsaid_list[0]  # ExtrAct the first dictionary
                    else:
                        return HttpResponse(f"No Admin data found with Id: {refCode}")
                   
                    context = {
                        'connection': dsaid.get('id'),
                        'customer_applicationId': loan.application_id
                    }
                 
                    response = requests.post(f"{settings.SUPERADMIN_URL}/superadmin/app1/adminApplicationViewsets", json=context)
                  
                    if response.status_code != 200 or response.status_code != 201:
                        
                        return HttpResponse(f"Invalid Data..{response.status_code}---{response.text}")
                else:
                    
                    return HttpResponse(f"No Admin Found with Id: {loan.dsaref_code}")


# Bhanu

def lap_document_add(request, application_id): 
       
    basic_detail = get_object_or_404(basicdetailform, application_id=application_id)
    personal_details = get_object_or_404(LoanApplication, basic_detail=basic_detail)
    
    if request.method == 'POST':
        form = LapDocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)  
           
            instance.personal_details = personal_details
            instance.save()

            return redirect('success', application_id=application_id)
        else:
            print(form.errors)
     
    else:
        form = LapDocumentUploadForm()

    return render(request, 'customer/lapdoc.html', {
        'form': form,
        'incomesource': personal_details.income_source,
        'loan_type': personal_details.loan_type,
    })


# ====================================================================================================
def success(request, application_id):   
    application = get_object_or_404(LoanApplication, basic_detail__application_id=application_id)
    context = {
        'application': application,
        'application_id': application_id,        
    }
    return render(request, 'customer/success.html', context)

def rejected_msg(request,status):
    return render(request,'customer/reject.html',{'status':status})
# ====================================================================================================
from django.http import QueryDict

from django.db.models import Prefetch
from django.shortcuts import render

def lapview(request):
    customer_profiles = LoanApplication.objects.all() # Using the related_name defined in goldCibilCheck
    verification_status = {}
    form_valid_status = {}
    credit_scores = {}
    profiles_with_cibil=[]

    # Get the status query parameter
    status_query = request.GET.get('status', None)

    for profile in customer_profiles:
        user_details=profile.basic_detail
        verification_exists = lapApplicationVerification.objects.filter(loan=profile).exists()
        verification_status[profile.id] = verification_exists
        details = disbursementdetails.objects.filter(verification=profile).first()
        form = DisbursementDetailsForm(instance=details)
        form_valid_status[profile.id] = form.is_valid()
        if status_query == 'submitted':
            form_valid_status[profile.id] = True
        cibil_record = CibilCheck.objects.filter(user=user_details).first()
        cibil_score = cibil_record.cibil_score if cibil_record else None

        profiles_with_cibil.append({
            'profile':profile,
            'cibil_score': cibil_score
        })
    return render(request, 'customer/lap_view.html', {
        'customer_profiles': customer_profiles,
        'verification_status': verification_status,
        'form_valid_status': form_valid_status,
        'profiles_with_cibil':profiles_with_cibil
    })
#views and updates==================================================
def update_lap(request, pk):
    customer_profile = get_object_or_404(LoanApplication, pk=pk)
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST, instance=customer_profile)
        if form.is_valid():
            form.save()
            # Assuming your URL pattern uses 'pk' and not 'instance_id'
            return redirect('update_doc', instance_id=customer_profile.id)
    else:
        form = LoanApplicationForm(instance=customer_profile)

    return render(request, 'customer/LAPform.html', {'form': form})
def update_lapdoc(request, instance_id):
    personal_details = get_object_or_404(LoanApplication, id=instance_id)
    applicant_document, created = lapDocumentUpload.objects.get_or_create(personal_details=personal_details)

    if request.method == 'POST':
        form = LapDocumentUploadForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
        
            return HttpResponse('<h1>Updated succesfully</h1>')
      
    else:
        form = LapDocumentUploadForm(instance=applicant_document)

    return render(request, 'customer/lapdoc.html', {
        'form': form,
        
        'incomesource': personal_details.income_source,
        'loan_type': personal_details.loan_type,
    })

def lapdocview(request):
    applicant_documents = lapDocumentUpload.objects.select_related('personal_details').all()
    return render(request, 'customer/docview.html', {'applicant_documents': applicant_documents})

def lapbuttview(request, pk):
    customer_profile = get_object_or_404(LoanApplication, pk=pk)
    return render(request, 'customer/lap_viewbutton.html', {'customer_profile': customer_profile})
#change

def lapdocbutt(request, application_id):
    personal_details=get_object_or_404(LoanApplication,application_id=application_id)
    applicant_document = get_object_or_404(lapDocumentUpload,personal_details=personal_details)
    return render(request, 'customer/view_docbutt.html', {'applicant_document': applicant_document})

def goldview(request):
    customer_profiles = Goldloanapplication.objects.all()
    profiles_with_cibil = []
    for profile in customer_profiles:
        user_details = profile.goldbasicdetail

        cibil_record = goldCibilCheck.objects.filter(user=user_details).first()
        cibil_score = cibil_record.cibil_score if cibil_record else None
        
        profiles_with_cibil.append({
            'profile': profile,
            'cibil_score': cibil_score
        })

    return render(request, 'customer/viewgoldloan.html', {
        'profiles_with_cibil': profiles_with_cibil  
    })
from django.conf import settings
def generate_otp():
    """Generate a 6-digit OTP."""
    return ''.join(random.choices(string.digits, k=6))

def send_otp(email, otp_code):
    """Send OTP code to the provided email."""
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp_code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def generate_verify_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email') 
        otp = request.POST.get('otp')
        
        if otp:
            try:
                otp_entry = OTP.objects.get(otp=otp, expires_at__gte=timezone.now())
                request.session['email'] = otp_entry.email
                return redirect('index')
            except OTP.DoesNotExist:
                return render(request, 'customer/generate_verify_otp.html', {
                    'form': OTPForm(), 
                    'error': 'Invalid or expired OTP',
                    'email': email
                })    
        if email:
            otp_code = generate_otp()
            OTP.objects.create(email=email, otp=otp_code, expires_at=timezone.now() + timezone.timedelta(minutes=5))
            send_otp(email, otp_code)
            return render(request, 'customer/generate_verify_otp.html', {
                'form': OTPForm(),
                'email': email
            })
    
    return render(request, 'customer/generate_verify_otp.html', {
        'form': OTPForm()
    })

def index(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'index.html', {
        'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,
        'email': email,'cc':cc,
    })
def lap_verification_add(request, instance_id):
    loan = get_object_or_404(LoanApplication, id=instance_id)
    
    applicant_documents = lapApplicationVerification.objects.filter(loan=loan)
    if applicant_documents.exists():
        applicant_document = applicant_documents.first()  
    else:
        applicant_document = lapApplicationVerification(loan=loan)
    
    if request.method == 'POST':
        form = lapApplicationVerifyForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
            return redirect('success') 
        
         
    else:
        form = lapApplicationVerifyForm(instance=applicant_document)
    
    return render(request, 'customer/lapappliverify.html', {
        'form': form,
    })
def update_lapverify(request, instance_id):
    loan = get_object_or_404(LoanApplication, id=instance_id)
    
    applicant_document, created = lapApplicationVerification.objects.get_or_create(loan=loan)

    if request.method == 'POST':
        form = lapApplicationVerifyForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            verification = form.save()

            if verification.verification_status == 'Approved':
                return redirect('disbursement_details', verification_id=loan.application_id)  
            
            other_fields_approved = any(
                getattr(verification, field.name) == 'Approved'
                for field in verification._meta.get_fields()
                if field.name != 'verification_status'
            )
            
            if other_fields_approved:
                return redirect('page', status='success')
            else:
                return redirect('page', status='rejected')
        
    else:
        form = lapApplicationVerifyForm(instance=applicant_document)

    return render(request, 'customer/updateverify.html', {
        'form': form,
    })
def disbursement_details(request, verification_id):
    modelClass=LoanApplication
    relationModelClass=disbursementdetails
    formClass=DisbursementDetailsForm
    reDirectUrl='disbursement_summary'
    
    if verification_id.startswith('SLNEL'):
        modelClass=Educationalloan
        relationModelClass=Edudisbursementdetails
        formClass=EduDisbursementDetailsForm
        reDirectUrl='Edudisbursement_summary'
    elif verification_id.startswith('SLNBL'):
        modelClass=BusinessLoan
        relationModelClass=Busdisbursementdetails
        formClass=BusDisbursementDetailsForm
        reDirectUrl='Busdisbursement_summary'   
    verification = get_object_or_404(modelClass, application_id=verification_id)
    details, created = relationModelClass.objects.get_or_create(verification=verification)
    form_status = 'not_submitted'
    if request.method == 'POST':
        form = formClass(request.POST, instance=details)
        if form.is_valid():
            form.save()
            form_status = 'submitted'
            return redirect(reDirectUrl)
       
    else:
        form = DisbursementDetailsForm(instance=details)

    return render(request, 'customer/disbursement_details.html', {
        'details_form': form,'form_status':form_status,})
def disbursement_summary(request):
    details_list = disbursementdetails.objects.select_related('verification').all()

    # Optionally, print out the details to verify
    for details in details_list:
        
     return render(request, 'customer/disbursementview.html', {
        'details_list': details_list,
    })
def lapcustomerverify(request, instance_id):
    loan = get_object_or_404(LoanApplication, id=instance_id)
    verfyObj = lapApplicationVerification.objects.filter(loan=loan).first()
    session_email = request.session.get('email')
    application_id = None
    if session_email and session_email == loan.email_id:
        application_id = loan.application_id
    
    return render(request, 'customer/customerverify.html', {
        'loan': loan,
        'verfyObj': verfyObj,
        'application_id': application_id,  
    })
def custom_logout(request):
    logout(request)
    return redirect('send_otp') 

from rest_framework.response import Response
from django.db.models import Q
from django.apps import apps

def commonInsuranceGet(request,refCode):
    
    allInsurance=AllInsurance.objects.filter(Q(dsaref_code__icontains=refCode) |
               Q(franrefCode__icontains=refCode)  |
               Q(empref_code=refCode)).count()
    
    lifeInsurance=LifeInsurance.objects.filter(Q(dsaref_code__icontains=refCode) |
               Q(franrefCode__icontains=refCode)  |
               Q(empref_code=refCode)).count()
    
    generalInsurance=GeneralInsurance.objects.filter(Q(dsaref_code__icontains=refCode) |
               Q(franrefCode__icontains=refCode)  |
               Q(empref_code=refCode)).count()
    
    healthInsuranc=healthInsurance.objects.filter(Q(dsaref_code__icontains=refCode) |
               Q(franrefCode__icontains=refCode)  |
               Q(empref_code=refCode)).count()
    
    totalInsurance=allInsurance+lifeInsurance+generalInsurance+healthInsuranc
    
    return JsonResponse({'allInsurance':allInsurance,'lifeInsurance':lifeInsurance,'generalInsurance':generalInsurance,'healthInsurance':healthInsuranc,'totalInsurance':totalInsurance},status=200)
def franchiseInsuranceGet(request,refCode):
    
    allInsurance=AllInsurance.objects.filter(dsaref_code=None,franrefCode=refCode,empref_code=None).count()
    
    lifeInsurance=LifeInsurance.objects.filter(dsaref_code=None,franrefCode=refCode,empref_code=None).count()
    
    generalInsurance=GeneralInsurance.objects.filter(dsaref_code=None,franrefCode=refCode,empref_code=None).count()
    
    healthInsuranc=healthInsurance.objects.filter(dsaref_code=None,franrefCode=refCode,empref_code=None).count()
    
    totalInsurance=allInsurance+lifeInsurance+generalInsurance+healthInsuranc
   
    
    return JsonResponse({'allInsurance':allInsurance,'lifeInsurance':lifeInsurance,'generalInsurance':generalInsurance,'healthInsurance':healthInsuranc,'totalInsurance':totalInsurance},status=200)
# bhanu
def LoanAgainstProperty(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'LoanAgainstProperty.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})
from django.shortcuts import render

# Create your views here.

def About(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'About.html', {'email': email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})
def Allinsurance(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
  
    form=InsuranceForm()
    if request.method=='POST':
        form=InsuranceForm(request.POST)
        form.save()
        return HttpResponse("data saved")
    return render(request,'AllInsurance.html',{'form':form,'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})

def allinsurance_view(request):
    all=AllInsurance.objects.all()
    return render(request,'customer/view_insurance.html',{'all':all})
def lifeinsurance_view(request):
    life=LifeInsurance.objects.all()
    return render(request,'customer/view_lifeinsurance.html',{'life':life})

def generalinsurance_view(request):
    general=GeneralInsurance.objects.all()
    return render(request,'customer/view_generalinsurance.html',{'general':general})
    

def healthinsurance_view(request):
    health=healthInsurance.objects.all()
    return render(request,'customer/view_healthinsurance.html',{'health':health})
def Generalinsurance(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    form=genInsuranceForm()
    if request.method=='POST':
        form=genInsuranceForm(request.POST)
        form.save()
        return HttpResponse("data saved")

    return render(request, 'GeneralInsurance.html',{'form':form,'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})
def Healthinsurance(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    email = request.session.get('email')
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    form=healthInsuranceForm()
    if request.method=='POST':
        form=healthInsuranceForm(request.POST)
        form.save()
        return HttpResponse("data saved")
    else:
        
     return render(request, 'HealthInsurance.html',{'form':'form','email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})

def Lifeinsurance(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)

    form=lifeInsuranceForm
    if request.method == 'POST':
       form = lifeInsuranceForm(request.POST)
       if form.is_valid():
          form.save()
          return HttpResponse("Data saved")
    
           
       
    return render(request, 'LifeInsurance.html',{'form':form,'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})
def BussinessLoan(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'BussinessLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})
def Carloan(request):   
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'CarLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})
def contact(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent.")
            return redirect('contact') 
    else:
        form = ContactForm()
    return render(request, 'contact.html',{'form':form,'email': email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})
def creditpage(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'creditpage.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})
@csrf_exempt
def dsa(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    if request.method == 'POST':
        form = dsaform(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<h1>succesfully registered</h1>')  # Change to your actual success URL
       
    else:
        form = dsaform()
    return render(request, 'dsa.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc,'form':form})
def educationalloan(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'Educationalloan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})
@csrf_exempt
def franchise_add(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    form=franchiseform()
    if request.method == 'POST':
        form = franchiseform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('<h1>succesfully registered</h1>')  # Change to your actual success URL
       
    else:
        form = franchiseform()
    return render(request, 'franchise.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc,'form':form})
def GoldLoan(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'GoldLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})
def HomeLoan(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'HomeLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})
def LoanAgainstProperty(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'LoanAgainstProperty.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})

def NewCarLoan(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'NewCarLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})
def Personalloans(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'Personalloans.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})

def UsedCarLoan(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'UsedCarLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc})
def homeloan(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    cl=CarLoan.objects.filter(email_id=email)
    cc=CreditDetail.objects.filter(email=email)
    return render(request, 'HomeLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,'cl':cl,'cc':cc,'url':f"{settings.CUSTOMER_SUPPORT_URL}ticket_create/"})
#gold basicdetail  view+===============================================

def gold_basic_detail_view(request):
    # Fetch all records to display in a table
    records = goldbasicdetailform.objects.all()
    return render(request, 'golddetail.html', {'records': records})
#othre basicdetail  view+===============================================

def other_basic_detail_view(request):
    # Fetch all records to display in a table
    records = otherbasicdetailform.objects.all()
    return render(request, 'otherdetail.html', {'records': records})

#lap basicdetail view===========================================================
def lap_basic_detail_view(request):
    # Fetch all records to display in a table
    records = basicdetailform.objects.all()
    return render(request, 'lapdetails.html', {'records': records})


