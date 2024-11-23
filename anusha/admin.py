from django.contrib import admin
from .models import *

admin.site.register(basicdetailform)
@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'loan_type', 'income_source','basic_detail')
    search_fields = ('first_name', 'last_name', 'pan_card_number', 'aadhar_card_number','created_at')

admin.site.register(lapDocumentUpload)
admin.site.register(Goldloanapplication)
# admin.site.register(OTP)
admin.site.register(lapApplicationVerification)
admin.site.register(disbursementdetails)
admin.site.register(otherbasicdetailform)
admin.site.register(otherloans)
admin.site.register(dsa)
admin.site.register(franchise)
# ==========bhanu====================




