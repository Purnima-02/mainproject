
from django.urls import path,include,re_path
from anusha import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from .lap_api import *
from anusha.InsuranceRestApi import AllInsuViewsets,GeneralInsuViewsets,HealthInsuViewsets,LifeInsuViewsets


router=DefaultRouter()
router.register('goldapi',goldviewset,basename='gold-view-set')
router.register('lapapi',LapViewSet,basename='lap-view-set')
router.register('otherapi',otherviewset,basename='other-view-set')

# Insurance Rest Apis
router.register('allInsuranceapi',AllInsuViewsets,basename='allInsuranceapi')
router.register('GeneralInsuranceapi',GeneralInsuViewsets,basename='GeneralInsuranceapi')
router.register('LifeInsuranceapi',LifeInsuViewsets,basename='LifeInsuranceapi')
router.register('healthInsuranceapi',HealthInsuViewsets,basename='healthInsuranceapi')

router.register('dsaapi',dsaViewSet,basename='dsa-view-set')
router.register('franchise_api',franchiseViewSet,basename='franchise-view-set')

urlpatterns = [

    
    path('viewinsurance/',views.allinsurance_view,name='insuranceview'),
    path('viewlifeinsurance/',views.lifeinsurance_view,name='insurancelifeview'),
    path('viewgeninsurance/',views.generalinsurance_view,name='insurancegenview'),
    path('viewhealthinsurance/',views.healthinsurance_view,name='insurancehealthview'),
    # path('basicdetail/<int:instance_id>/',views.basicdetails,name='basicdetail_add'),
    path('generate-verify-otp/', views.generate_verify_otp_view, name='generate-verify-otp'),

# ====================================.===========
    path('basicdetail/',views.basicdetails,name='basicdetail'),
    path('fetch-credit-report/', views.fetch_credit_report, name='fetchcreditreport'),
    path('lapapply/', views.lap_add, name='lapapply'),

    # path('lapapply/<int:instance_id>/', views.lap_add, name='lapapply_add'),
    path('lapdoc/<str:application_id>', views.lap_document_add, name='lapdoc'),
    path('success/<str:application_id>', views.success, name='success'),
    path('lapverify/<int:instance_id>/', views.lap_verification_add, name='lapverify'),
    path('lapverify/<int:instance_id>/update/', views.update_lapverify, name='updatverify'),
    path('disbursement/<str:verification_id>/', views.disbursement_details, name='disbursement_details'),    
    path('disbursement-summary/', views.disbursement_summary, name='disbursement_summary'),
    path('lapverify/<int:instance_id>/view', views.lapcustomerverify, name='viewcustomerverify'),  
    path('lapapply/<int:pk>/update/', views.update_lap, name='update_lap'),
    path('lapview/', views.lapview, name='lapview'),
    path('lapapply/<int:pk>/view/', views.lapbuttview, name='viewbutt'),  

    path('doclap/<int:instance_id>/update/', views.update_lapdoc, name='update_doc'),
    path('doclap/', views.lapdocview, name='docview'),
    path('doclap/<str:application_id>/', views.lapdocbutt, name='viewdocbutt'),

    # =============================================================================
    path('goldloan/', views.goldloanapplication, name='goldloan'),
    path('goldview/', views.goldview, name='goldview'),

    # path('goldloan/<int:pk>/view/', views.goldbuttview, name='goldviewbutt'), 
    path('goldsuccess/<str:application_id>', views.goldsuccess, name='goldsuccess'),
    path('goldbasicdetail/',views.goldbasicdetails,name='goldbasicdetail'),
    path('gold-fetch-credit-report/', views.gold_fetch_credit_report, name='goldfetchcreditreport'),
    path('otherloan/', views.otherloanapplication, name='otherloan'),
    path('otherview/', views.otherview, name='otherview'),
    # path('goldloan/<int:pk>/view/', views.goldbuttview, name='goldviewbutt'), 
    path('othersuccess/<str:application_id>', views.othersuccess, name='othersuccess'),
    path('otherbasicdetail/',views.otherbasicdetails,name='otherbasicdetail'),
    path('other-fetch-credit-report/', views.other_fetch_credit_report, name='otherfetchcreditreport'),
    #=============================================  

    path('rejected/<str:status>',views.rejected_msg,name='page'),
#     ===========================================================
    path('',views.index,name='index'),
    path('about/',views.About,name='about'),
    path('allinsurance/',views.Allinsurance,name='allinsurance'),
    path('commonInsuranceGet/<str:refCode>',views.commonInsuranceGet,name='commonInsuranceGet'),

    path('bussinessLoan/',views.BussinessLoan,name='bussinessloan'),
    path('carloan/',views.Carloan,name='carloan'),
    path('contact/',views.contact,name='contact'),
    path('creditpage/',views.creditpage,name='creditpage'),
    path('dsa/',views.dsa,name='dsa'),
    path('educationalloan/',views.educationalloan,name='educationalloan'),
    path('franchise/',views.franchise_add,name='franchise'),
    path('generalinsurance/',views.Generalinsurance,name='generalinsurance'),
    path('gold/',views.GoldLoan,name='gold'),
    path('healthinsurance/',views.Healthinsurance,name='healthinsurance'),
    path('lifeinsurance/',views.Lifeinsurance,name='lifeinsurance'),
    path('loanagainstproperty/',views.LoanAgainstProperty,name='lap'),
    path('newcarloan/',views.NewCarLoan,name='newcar'),
    path('personalloans/',views.Personalloans,name='personalloans'),
    path('usedcarloan/',views.UsedCarLoan,name='usedcar'),
    path('homeloan/',views.HomeLoan,name='homeloan'),
    # path('customersupport/',views.customer_support,name='customer_support'),

    # ==============bhanu==================================================
    path('',include(router.urls)),

    path('getdisbursementdetails/',LapViewSet.as_view({'get':'get_disbursement_details'}),name='get-details'),

    path('getByRefCode/<str:refCode>',LapViewSet.as_view({"get":"getByRefCode"}),name="get-Lapref-code"),
    
    # Franchise...
    path('getFranchiseByRefCode/<str:refCode>',LapViewSet.as_view({"get":"getFranchiseByRefCode"}),name="get-getFranchiseByRefCode"),

    path('getdisbursementdetails/',LapViewSet.as_view({'get':'get_disbursement_details'}),name='get-details'), 
    # Bhanu
    path('commonInsuranceGet/<str:refCode>',views.commonInsuranceGet,name='commonInsuranceGet'),
    path('franchiseInsuranceGet/<str:refCode>',views.franchiseInsuranceGet,name='franchiseInsuranceGet'),
# Bhanu   

 #=====================basic detail view===================================================================
    path('goldbasicdetailview/',views.gold_basic_detail_view, name='goldbasicview'),
    path('otherbasicdetailview/',views.other_basic_detail_view, name='otherbasicview'),
    path('lapbasicdetailview/',views.lap_basic_detail_view, name='lapbasicview'),

    path('dsa/<str:dsa_id>/', dsaViewSet.as_view({'get': 'get_by_dsa_registerid'}), name='dsa-get-by-registerid'),
    path('branch/<str:franchise_id>/', dsaViewSet.as_view({'get': 'get_by_franchiseid'}), name='franchise-get-by-registerid'),


]