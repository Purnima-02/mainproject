"""
URL configuration for ddproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from seetha.views import *
from rest_framework.routers import DefaultRouter
from seetha.carrestapi import *

from django.conf.urls.static import static
from django.conf import  settings

router=DefaultRouter()
router.register('ddproject',CarLoanViewSet,basename='a')

urlpatterns = [
    path('carbasic-details/', carbasicdetail, name='carbasicdetail'),
    path('car-fetch-credit-report/', car_fetch_credit_report, name='carfetchcreditreport'),    #path('success/',success,name='success'),
    path('car-loan-application/',apply_for_car_loan,name='car-loan-application'),
    path('document/',upload_documents,name="cardoc"),
    path('car-loans-list/',car_loan_list, name='car_loan_list'),
    path('car-loan-update/<str:application_id>',car_loan_update,name='car-loan-update'),
    path('car-loan-view/<str:id>',car_loan_view,name='car-loan-view'),
    path('document-upload/<str:application_id>',update_car_loan_document,name='update_documents'),
    path('application-flow/<str:application_id>',carapplicationVerification,name='applicationFlow'),
    path('view-document/<str:application_id>',documentsView,name='documents-view'),
    path('update-verification/<str:application_id>',update_car_verify,name="update-verification"),
    path('customerProfile/<str:application_id>',carcustomerProfile,name="customerprofile"),
    
    path('cardisbursement/<str:verification_id>/', disbursement_cardetails, name='disbursement_cardetails'),
    path('disbursement-summary/', disbursement_carsummary, name='disbursement_carsummary'),

    path('getByRefCode/<str:refCode>',CarLoanViewSet.as_view({"get":"getByRefCode"}),name="get-Carref-code"),
    path('getRejectedRecords/<str:refCode>',CarLoanViewSet.as_view({"get":"getRejectedRecords"}),name="get-CargetRejectedRecords"),
     
    #  Franchise
    path('getFranchiseByRefCode/<str:refCode>',CarLoanViewSet.as_view({"get":"getFranchiseByRefCode"}),name="get-getFranchiseByRefCode"),
    path('getFranchiseRejectedRecords/<str:refCode>',CarLoanViewSet.as_view({"get":"getFranchiseRejectedRecords"}),name="get-getFranchiseRejectedRecords"),
    path('carbasicdetailview/',car_basic_detail_view, name='carbasicview'),

]

urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

 