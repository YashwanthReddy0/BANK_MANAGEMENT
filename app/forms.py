from django import forms
from .models import Bank,Gender,Acc_Type

class BankForm(forms.ModelForm):
    Pin_Number = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Bank
        fields = ['FirstName','MiddleName','LastName','Gender','acc_type','FatherName','MotherName','email','Adhaar_Number','Address','phoneNumber','Pin_Number','Balance_Amount']

class PinForm(forms.Form):
    account_number = forms.CharField(max_length=15)
    Pin_Number = forms.CharField(widget=forms.PasswordInput)
