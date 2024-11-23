from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from .BusinessRestApi import BusiViewsets,BusiBasicDetailviewset


router=DefaultRouter()
router.register(r'BusiViewsets',BusiViewsets,basename='busi-view-sets')
router.register('busiBasicset',BusiBasicDetailviewset,basename='busiBasicset')


urlpatterns = [
    path('demo',apply_for_business_loan,name="demo"),
    path('document',upload_documents,name="upload-documents"),
    path('business-loans-lists/', business_loan_list, name='business_loan_list'),
    path('business-loan-update/<str:application_id>',business_loan_update,name='business-loan-update'),
    path('business-loan-view/<str:id>',business_loan_view,name='business-loan-view'),
    path('document-upload/<str:application_id>',update_business_loan_document,name='update-documents'),
    path('busapplication-flow/<str:application_id>',busapplicationVerification,name='BusapplicationFlow'),
    path('view-document/<str:application_id>',documentsView,name='documents-view'),
    path('busupdate-verification/<str:application_id>',busupdate_verification,name="busupdate-verification"),
    path('customerProfile/<str:application_id>',customerProfile,name="buscustomer-profile"),
    path('busbasicdetail/',busbasicdetails,name='busbasicdetail'),
    path('bus-fetch-credit-report/', bus_fetch_credit_report, name='busfetchcreditreport'),

    path('businesslistDemo',businesslistDemo,name='businesslistDemo'),
    path('busiSucessPage',busiSucessPage,name='busiSucessPage'),
    path('DummyPurpose',demoPurpose,name='demoPurpose'),
    path('',include(router.urls)),
    
    path('getFranchiseRejectedRecords/<str:refCode>',BusiViewsets.as_view({"get":"getFranchiseRejectedRecords"}),name="get-getFranchiseRejectedRecords"),
    path('getFranchiseApprovedRecords/<str:refCode>',BusiViewsets.as_view({"get":"getFranchiseApprovedRecords"}),name="get-getFranchiseApprovedRecords"),
    path('getByFranchiseRefCode/<str:refCode>',BusiViewsets.as_view({"get":"getByFranchiseRefCode"}),name="get-getByFranchiseRefCode"),
    path('getByRefCode/<str:refCode>',BusiViewsets.as_view({"get":"getByRefCode"}),name="get-ref-code"),
    
    path('getApprovedRecords/<str:refCode>',BusiViewsets.as_view({"get":"getApprovedRecords"}),name="get-getApprovedRecords"),
    path('getRejectedRecords/<str:refCode>',BusiViewsets.as_view({"get":"getRejectedRecords"}),name="BusgetRejectedRecords"),

    path('getBasicdetailapplicationid/<str:mobileNumber>',BusiBasicDetailviewset.as_view({"get":"getApplicationId"}),name="getApplicationId"),
 
    #  Disbursment
    path('Busdisbursement_summary',busdisbursement_summary,name='Busdisbursement_summary'),

    path('busbasicdetailview/',bus_basic_detail_view, name='busbasicview'),
]
