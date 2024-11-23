from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CarLoan)
admin.site.register(CarLoanDocument)
admin.site.register(CarApplicationVerification)
admin.site.register(CLBasicDetail)
admin.site.register(CarDisbursementDetails)