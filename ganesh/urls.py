
from django.urls import path,include
from ganesh import views
from rest_framework.routers import DefaultRouter
from ganesh.credit_RestApi import credbasicdetailformviewsets,creditDetailviewsets



router=DefaultRouter()
router.register('api_basicdetail',credbasicdetailformviewsets,basename='api_basicdetail'),
router.register('api_credit_appli',creditDetailviewsets,basename='api_credit_appli'),



urlpatterns = [
    path('crebasicdetail/', views.crebasicdetails, name='crebasicdetail'),
    path('cre-fetch-credit-report/', views.cre_fetch_credit_report, name='crefetchcreditreport'),

    path('credit/', views.credit_add, name='credit'),
    path('document_add/<str:application_id>/', views.credit_document_add, name='document_add'),
    path('success/<str:application_id>', views.ccsuccess, name='ccsuccess'), 
    path('credit/<int:pk>/update/', views.update_cred_detail_view, name='update_credit_detail'),
    path('update-document/<int:instance_id>/', views.update_cred_document_detail_view, name='update_document'),
    path('table_view/', views.credit_table_view, name='credit_detail_list'),

    path('credit/<int:pk>/view/', views.view_credit_appli, name='view_credit_appli'),

    path('document_view/', views.view_credit_documents, name='view_documents'),


     path('', include(router.urls)),


path('creditbasicdetailview/',views.credit_basic_detail_view, name='creditbasicview'),

    path('getByRefCode/<str:refCode>',creditDetailviewsets.as_view({"get":"getByRefCode"}),name="get-ref-code"),
    path('getBasicdetailapplicationid/<str:mobileNumber>',credbasicdetailformviewsets.as_view({"get":"getApplicationId"}),name="getApplicationId"),

]










