from django.contrib import admin
from django.urls import path
from ppk import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('new_dashboard/',views.dash,name='new_dashbord'),
    path('all_loans/',views.all_loans,name='all_loans'),
    
    
    path('dsa_Refcount/',views. refcount, name='dsa_Refcount'),
    path('fra_Refcount/',views. fra_refcount, name='fra_Refcount'),
    path('sale_Refcount/',views. sale_refcount, name='sale_Refcount'),
    path('dsa_inscount/',views. dsainscount, name='dsa_inscount'),
    path('far_inscount/',views. farinscount, name='far_inscount'),
    path('sale_inscount/',views. saleinscount, name='sale_inscount'),
    path('login/check/', views.login_check, name='login_check'),  # Route for the login API call
    path('logout/', views.Logout, name='logout'),




]



