from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import *
from .forms import *


import requests
import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse

APIID = "AP100034"
TOKEN = "6b549eed-2af0-488c-a2e1-3d10f37f11c6"

def basicdetailspl(request,instance_id=None):
    instance = get_object_or_404(personalbasicdetail, id=instance_id) if instance_id else None
    application_id=None

    if request.method == 'POST':
        form = plBasicDetailForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            user_details = form.save()
            application_id=user_details.application_id
            
            # Bhanu
            request.session['PLoanExpiryDate']=str(user_details.expiry_at)
            # Bhanu
            
            orderid = str(uuid.uuid4())
            
            # bhanu
            destinationUrl=reverse('personal')
            request.session['plafterurl']=destinationUrl
            request.session['plAppliId']=True
            # bhanu
            
            request.session['application_id']=application_id
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
                return redirect('plfetchcreditreport')
            else:
                return JsonResponse({"status": "error", "message": data.get("mess", "Failed to generate OTP")})
    else:
        form = plBasicDetailForm()

    return render(request, 'admin/basic.html', {'form': form})
def pl_fetch_credit_report(request):
    otp=request.session.get('otp')
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user_details = personalbasicdetail.objects.get(id=user_id)
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
                    loan_application, created = plCibilCheck.objects.get_or_create(user=user_details)
                    if loan_application:
                        loan_application.cibil_score = credit_score
                        loan_application.save()
                    return render(request, 'admin/plcibil_score.html', {'credit_score': credit_score, 'application_id': user_details.application_id})
            else:
                return JsonResponse({"status": "error", "message": data["mess"]})
        else:
            return JsonResponse({"status": "error", "message": "Failed to fetch credit report"})

    return render(request, 'admin/basic.html',{'otp':otp})

def personal_detail_view(request):
    # Get mobile number from session or POST data
    mobile_number = request.session.get('mobile_number','') or request.POST.get('mobile_number','') 
    pan_number=request.session.get('pan_num') 
   
    # bhanu
    refCode=None
    francrefCode=None
    if request.GET.get('refCode'):
       
        refCode=request.GET.get('refCode')
    if request.GET.get('franrefCode'):
       francrefCode=request.GET.get('franrefCode')
     # bhanu

    if request.method == 'POST':
        form = PersonalDetailForm(request.POST, request.FILES)
        
        if form.is_valid():
            loan = form.save(commit=False)
            
            # bhanu
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
            #  bhanu
            lap = personalbasicdetail.objects.filter(phone_number=mobile_number).order_by('-application_id').first()
                
            if lap:
                    loan.basicdetailform = lap
                    loan.mobile_number = mobile_number
                    loan.pan_card_number=pan_number
                    loan.save()  
                    request.session['loanid'] = loan.id
                    
                    # bhanu 
                    
                    if refCode:
                       if refCode.startswith('SLNDSA'):
                        EducommonDsaLogic(request,refCode,loan)
                 
                       elif refCode.startswith('SLNEMP'):
                          eduSalesLogic(request,refCode,loan)
                       else: 
                           superAdmin(request,refCode,loan)
                
                    elif francrefCode:
                            franchiseLogic(request,francrefCode,loan)
                        
                    
                    destinationUrl=reverse('document_detail', kwargs={'application_id': lap.application_id})
                    request.session['plafterurl']=destinationUrl
                    # bhanu
                    
                    return redirect('document_detail', application_id=lap.application_id)
    else:
        # Pre-populate mobile_number field with the session value
        form = PersonalDetailForm(initial={'mobile_number': mobile_number,'pan_number':pan_number})

    return render(request, 'admin/personal_detail_form.html', {'form': form, 'mobile_number': mobile_number,'pan_number':pan_number})
# Bhanu
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
                  
                    response = requests.post(f"{settings.SUPERADMIN_URL}/superadmin/app1/adminApplicationViewsets/", json=context)
                   
                    if response.status_code != 200 or response.status_code != 201:
                       
                        return HttpResponse(f"Invalid Data..{response.status_code}---{response.text}")
                else:
                    
                    return HttpResponse(f"No Admin Found with Id: {loan.dsaref_code}")
# Bhanu

def document_details_view(request, application_id):
    
    basicdetailform = get_object_or_404(personalbasicdetail, application_id=application_id)
    personal_details = get_object_or_404(PersonalDetail, basicdetailform=basicdetailform)

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)  # Create a new record, but don't save yet
            
            instance.personal_detail = personal_details
            instance.save()  # Save the instance with the related personal details
            return redirect('success',application_id=application_id)  # Redirect after saving
       
    else:
        form = DocumentUploadForm()

    return render(request, 'admin/document_upload_form.html', {
        'form': form,
    })
# ====================homelaon=
def basicdetailhl(request,instance_id=None):
    instance = get_object_or_404(homebasicdetail, id=instance_id) if instance_id else None
    application_id=None

    if request.method == 'POST':
        form = HomeBasicDetailForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            user_details = form.save()
            
             # bhanu
            destinationUrl=reverse('customer_profile')
            request.session['hmafterurl']=destinationUrl
            request.session['hmAppliId']=True
            # bhanu
            application_id=user_details.application_id
            # Bhanu
            request.session['HLoanExpiryDate']=str(user_details.expiry_at)
            # Bhanu
            orderid = str(uuid.uuid4())
            request.session['application_id']=application_id
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
                return redirect('hlfetchcreditreport')
            else:
                return JsonResponse({"status": "error", "message": data.get("mess", "Failed to generate OTP")})
    else:
        form = HomeBasicDetailForm()
    return render(request, 'admin/hlbasic.html', {'form': form})
def hl_fetch_credit_report(request):
    otp=request.session.get('otp')
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user_details = homebasicdetail.objects.get(id=user_id)
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
                    loan_application, created = hlCibilCheck.objects.get_or_create(user=user_details)
                    if loan_application:
                        loan_application.cibil_score = credit_score
                        loan_application.save()
                    return render(request, 'admin/hlcibil_score.html', {'credit_score': credit_score, 'application_id': user_details.application_id})
            else:
                return JsonResponse({"status": "error", "message": data["mess"]})
        else:
            return JsonResponse({"status": "error", "message": "Failed to fetch credit report"})

    return render(request, 'admin/hlbasic.html',{'otp':otp})
def customer_profile_view(request):
    mobile_number = request.session.get('mobile_number')
    pan_number=request.session.get('pan_num')
   
    # bhanu
    refCode=None
    francrefCode=None
    if request.GET.get('refCode'):
     
        refCode=request.GET.get('refCode')
    if request.GET.get('franrefCode'):
       francrefCode=request.GET.get('franrefCode')
     # bhanu
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            loan = form.save(commit=False)
             # bhanu
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
            #  bhanu
            lap = homebasicdetail.objects.filter(phone_number=mobile_number).order_by('application_id').first()
            
            if lap:
                
                loan.basicdetailhome = lap
                loan.mobile_number = mobile_number
                loan.pan_card_number=pan_number
                loan.save()  
                request.session['loanid'] = loan.id
                
                # bhanu 
                    
                if refCode:
                       if refCode.startswith('SLNDSA'):
                        EducommonDsaLogic(request,refCode,loan)
                 
                       elif refCode.startswith('SLNEMP'):
                        
                          eduSalesLogic(request,refCode,loan)
                       else: 
                           superAdmin(request,refCode,loan)
                
                elif francrefCode:
                            franchiseLogic(request,francrefCode,loan)
                destinationUrl=reverse('applicant_document_create', kwargs={'application_id': lap.application_id})
                request.session['hmafterurl']=destinationUrl
                # bhanu
                return redirect('applicant_document_create', application_id=lap.application_id)
            else:
              
                return redirect('homebasicdetail')
    else:
        form = CustomerProfileForm()

    return render(request, 'admin/customer_profile_form.html', {'form': form, 'mobile_number':mobile_number,'pan_number':pan_number})
def applicant_document_create_view(request, application_id):
   
    # Fetch the related instances
    basicdetailhome = get_object_or_404(homebasicdetail, application_id=application_id)
    applicant_profile = get_object_or_404(CustomerProfile, basicdetailhome=basicdetailhome)

    if request.method == 'POST':
        form = ApplicantDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)  # Create a new record, but don't save yet
           
            instance.applicant_profile = applicant_profile
            instance.save()  # Save the instance with the related personal details
            return redirect('success',application_id=application_id)  # Redirect after saving
        
    else:
        form = ApplicantDocumentForm()

    return render(request, 'admin/applicant_document_form.html', {
        'form': form,
        'incomesource': applicant_profile.income_source,
        'loan_type': applicant_profile.loan_type,
    })

   
def success(request, application_id):
    return render(request, 'admin/success.html', {'application_id': application_id})

#views and updates==================================================

def update_personal_detail_view(request, pk):
    personal_detail = get_object_or_404(PersonalDetail, pk=pk)
    if request.method == 'POST':
        form = PersonalDetailForm(request.POST, instance=personal_detail)
        if form.is_valid():
            form.save()
            return redirect('update_document_detail', instance_id=personal_detail.id)
    else:
        form = PersonalDetailForm(instance=personal_detail)
    return render(request, 'admin/personal_detail_form.html', {'form': form})

def update_document_detail_view(request, instance_id):
    personal_detail = get_object_or_404(PersonalDetail, id=instance_id)
    document_upload, created = DocumentUpload.objects.get_or_create(personal_detail=personal_detail)
  
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, instance=document_upload)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = DocumentUploadForm(instance=document_upload)

    return render(request, 'admin/document_upload_form.html', {'form': form})
def document_upload_list_view(request):
    document_uploads = DocumentUpload.objects.select_related('personal_detail').all()
    return render(request, 'admin/document_upload_list.html', {'document_uploads': document_uploads})

def view_personal_detail_view(request, pk):
    personal_detail = get_object_or_404(PersonalDetail, pk=pk)
    return render(request, 'admin/view_personal_detail.html', {'personal_detail': personal_detail})

def view_documents_view(request, application_id):
    personal_detail=get_object_or_404(PersonalDetail,application_id=application_id)
    document_upload = get_object_or_404(DocumentUpload, personal_detail=personal_detail)
    return render(request, 'admin/view_documents.html', {'document_upload': document_upload})
    
def update_customer_profile_view(request, pk):
    customer_profile = get_object_or_404(CustomerProfile, pk=pk)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer_profile)
        if form.is_valid():
            form.save()
            return redirect('applicant_document_create', instance_id=customer_profile.id )
    else:
        form = CustomerProfileForm(instance=customer_profile)

    return render(request, 'admin/customer_profile_form.html', {'form': form})

def update_applicant_document_view(request, instance_id):
    applicant_profile = get_object_or_404(CustomerProfile, id=instance_id)
    applicant_document, created = ApplicantDocument.objects.get_or_create(applicant_profile=applicant_profile)

    if request.method == 'POST':
        form = ApplicantDocumentForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ApplicantDocumentForm(instance=applicant_document)

    return render(request, 'admin/applicant_document_form.html', {'form': form})

from django.shortcuts import render

def customer_profile_list_view(request):
    profiles = CustomerProfile.objects.all() 
    profile_with_cibil=[]
    for profile in profiles:
        user_details=profile.basicdetailhome
        cibil_record=hlCibilCheck.objects.filter(user=user_details).first()
        cibil_score=cibil_record.cibil_score if cibil_record else None
        profile_with_cibil.append({
            'profile': profile,
            'cibil_score': cibil_score
        })
    return render(request, 'admin/customer_profile_list.html', {'profile_with_cibil':profile_with_cibil})


def applicant_document_list_view(request):
    applicant_documents = ApplicantDocument.objects.select_related('applicant_profile').all()
    return render(request, 'admin/applicant_document_list.html', {'applicant_documents': applicant_documents})

def view_customer_profile_view(request, pk):
    customer_profile = get_object_or_404(CustomerProfile, pk=pk)
    return render(request, 'admin/view_customer_profile.html', {'customer_profile': customer_profile})

def view_applicant_document_view(request, application_id):
    applicant_profile=get_object_or_404(CustomerProfile,application_id=application_id)
    applicant_document = get_object_or_404(ApplicantDocument, applicant_profile=applicant_profile)
    return render(request, 'admin/view_applicant.html', {'applicant_document': applicant_document})

def personal_list_view(request):
    personal_details = PersonalDetail.objects.all()
    profile_with_cibil=[]
    for profile in personal_details:
        user_details=profile.basicdetailform
        cibil_record=plCibilCheck.objects.filter(user=user_details).first()
        cibil_score=cibil_record.cibil_score if cibil_record else None
        profile_with_cibil.append({
            'profile': profile,
            'cibil_score': cibil_score
        })

    return render(request, 'admin/personal_detail_list.html', {'profile_with_cibil':profile_with_cibil})
from django.shortcuts import render, get_object_or_404, redirect
from .models import PersonalDetail, ApplicationVerification
from .forms import ApplicationVerificationForm  

def personal_verification_add_or_update(request, instance_id):
    personal_detail = get_object_or_404(PersonalDetail, id=instance_id)
    
    applicant_document, created = ApplicationVerification.objects.get_or_create(
        personal_detail=personal_detail
    )

    if request.method == 'POST':
        form = ApplicationVerificationForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            applicant_document = form.save(commit=False)
            applicant_document.save()  
            
            if applicant_document.verification_status == 'Approved':
                return redirect('pldisbursement_details', verification_id=applicant_document.id)  # Use the correct keyword
            else:
                return redirect('success_page')  
        
    else:
        form = ApplicationVerificationForm(instance=applicant_document)
    
    return render(request, 'admin/applyper.html', {
        'form': form,
        'personal_detail': personal_detail  # Pass personal_detail to the template if needed
    })

def personalcustomerverify(request, instance_id):
    # Fetch the loan application based on the given instance_id
    personal_detail = get_object_or_404(PersonalDetail, id=instance_id)
    # Try to get existing verification documents for this loan application
    verfyObj = ApplicationVerification.objects.filter(personal_detail=personal_detail).first()
    
    # Render the record details in the template
    return render(request, 'admin/perview.html', {
        'personal_detail': personal_detail,
        'verfyObj': verfyObj,
})
def pldisbursement_details(request, verification_id):
    # Fetch the ApplicationVerification instance instead of CustomerProfile
    verification = get_object_or_404(PersonalDetail, id=verification_id)
    # Fetch or create the pldisbursementdetails using the correct verification instance
    details, created = pldisbursementdetails.objects.get_or_create(verification=verification)
    form_status = 'not_submitted'

    if request.method == 'POST':
        form = PlDisbursementDetailsForm(request.POST, instance=details)
        if form.is_valid():
            form.save()
            form_status = 'submitted'
            return redirect('pldisbursement_summary')
       
    else:
        form = PlDisbursementDetailsForm(instance=details)

    return render(request, 'admin/pldisbursement_details.html', {
        'details_form': form,
        'form_status': form_status,
    })

def pldisbursement_summary(request):
    details_list = pldisbursementdetails.objects.select_related('verification__disbursementdetail').all()

    return render(request, 'admin/pldisbursementview.html', {
        'details_list': details_list,
    })
def plsuccess(request, application_id):
    goldapp = get_object_or_404(PersonalDetail, basicdetailform__application_id=application_id)
    context = {
        'application_id': application_id,
        'goldapp': goldapp,
    }
    return render(request, 'admin/plsuccess.html', context)

def rejected_pl(request, status):
    return render(request, 'admin/plreject.html', {'status': status})

from django.http import HttpResponse
def home_verification_add(request, instance_id):
    applicant_profile = get_object_or_404(CustomerProfile, id=instance_id)
    
    # Use filter() to handle multiple documents
    applicant_documents = HomeApplication.objects.filter(applicant_profile=applicant_profile)
    
    if applicant_documents.exists():
        applicant_document = applicant_documents.first()  # or any other logic to choose a document
    else:
        applicant_document = HomeApplication(applicant_profile=applicant_profile)

    if request.method == 'POST':
        form = HomeapplicationForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
            return HttpResponse('<h1>success</h1>')
       
    else:
        form = ApplicationVerificationForm(instance=applicant_document)
    
    return render(request, 'admin/applyhome.html', {'form': form})
def homecustomerverify(request, instance_id):
    # Fetch the loan application based on the given instance_id
    applicant_profile = get_object_or_404(CustomerProfile, id=instance_id)
    # Try to get existing verification documents for this loan application
    verfyObj = HomeApplication.objects.filter(applicant_profile=applicant_profile).first()
    
    # Render the record details in the template
    return render(request, 'admin/homeview.html', {
        'applicant_profile': applicant_profile,
        'verfyObj': verfyObj,
}) 
def update_hlverify(request, instance_id):
    applicant_profile = get_object_or_404(CustomerProfile, id=instance_id)
    
    # Get or create HomeApplication related to the applicant profile
    applicant_document, created = HomeApplication.objects.get_or_create(applicant_profile=applicant_profile)

    if request.method == 'POST':
        form = HomeapplicationForm(request.POST, request.FILES, instance=applicant_document)

        if form.is_valid():
            verification = form.save()

            # Check if verification is a HomeApplication instance
            # If verification is approved
            if verification.verification_status == 'Approved' and verification.id:
                return redirect('hldisbursement_details', verification_id=verification.id)
            # Check other fields for approval status
            other_fields_approved = any(
                getattr(verification, field.name) == 'Approved'
                for field in verification._meta.get_fields()
                if field.name != 'verification_status'
            )
            
            if other_fields_approved:
                return redirect('hlpage', status='success')
            else:
                return redirect('hlpage', status='rejected')
        
    else:
        form = HomeapplicationForm(instance=applicant_document)

    return render(request, 'admin/update_home.html', {
        'form': form,
    })


def hldisbursement_details(request, verification_id):
    # Fetch the HomeApplication instance instead of CustomerProfile
    verification = get_object_or_404(CustomerProfile, id=verification_id)
    # Fetch or create the hldisbursementdetails using the correct verification instance
    details, created = hldisbursementdetails.objects.get_or_create(verification=verification)
    form_status = 'not_submitted'
    if request.method == 'POST':
        form = HlDisbursementDetailsForm(request.POST, instance=details)
        if form.is_valid():
            form.save()
            form_status = 'submitted'
            return redirect('hldisbursement_summary')
       
    else:
        form = HlDisbursementDetailsForm(instance=details)

    return render(request, 'admin/hldisbursement_details.html', {
        'details_form': form,
        'form_status': form_status,
    })

def hldisbursement_summary(request):
    details_list = hldisbursementdetails.objects.select_related('verification').all()
    # Optionally, print out the details to verify
    for details in details_list:
       

     return render(request, 'admin/hldisbursementview.html', {
        'details_list': details_list,
})
def hlsuccess(request, application_id):
    goldapp=get_object_or_404(CustomerProfile,basicdetailhome__application_id=application_id)
    context = {
        
        'application_id': application_id,
        'goldapp':goldapp,
        
    }
    return render(request, 'admin/hlsuccess.html', context)

def rejected_hl(request,status):
    return render(request,'admin/hlreject.html',{'status':status})
# =======================homedisend=========================
from django.contrib.auth import authenticate, login

from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if username == 'ravi' and password == 'Ravindra@1':  # Check specific credentials
                    login(request, user)
                    return redirect('dashboard')  # Redirect to the dashboard
                else:
                    form.add_error(None, 'Invalid credentials.')
    else:
        form = LoginForm()

    return render(request, 'main/login.html', {'form': form})

def dashboard(request):
    personal_loans_count = PersonalDetail.objects.count()
    home_loans_count = CustomerProfile.objects.count()
    business_loans_count = 10
    car_loans_count = 40
    educational_loans_count = 80
    other_loans_count = 100
    # Add more counts as needed

    context = {
        'personal_loans_count': personal_loans_count,
        'home_loans_count': home_loans_count,
        'business_loans_count': business_loans_count,
        'car_loans_count': car_loans_count,
        'educational_loans_count': educational_loans_count,
        'other_loans_count': other_loans_count,
        
        # Add more counts to context if needed
    }
    return render(request, 'main/admin.html', context)
    # =====/=====/extert

def per_basic_detail_view(request):
    # Fetch all records to display in a table
    records = personalbasicdetail.objects.all() 
    return render(request, 'perdetails.html', {'records': records})
def home_basic_detail_view(request):
    # Fetch all records to display in a table
    records = homebasicdetail.objects.all()
    return render(request, 'homedetails.html', {'records': records})