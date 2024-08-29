from django.contrib import admin
from .models import Bank,Acc_Type,Gender
# Register your models here.

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    ...

@admin.register(Acc_Type)
class Acc_typeAdmin(admin.ModelAdmin):
    ...

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    ...
