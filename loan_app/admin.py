from django.contrib import admin

# Register your models here.
from .models import User, Lender, Borrower, DebtRecords, RepaymentRecords
admin.site.register(User)
admin.site.register(Lender)
admin.site.register(Borrower)
admin.site.register(DebtRecords)
admin.site.register(RepaymentRecords)