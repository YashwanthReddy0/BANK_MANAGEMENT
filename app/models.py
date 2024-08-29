from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta

# Create your models here.

class Gender(models.Model):
    Gender = models.CharField(max_length=15)

    def __str__(self):
        return self.Gender
    
class Acc_Type(models.Model):
    acc_type = models.CharField(max_length=15)

    def __str__(self):
        return self.acc_type    

class Bank(models.Model):
    FirstName = models.CharField(max_length=35)
    MiddleName = models.CharField(max_length=35) 
    LastName = models.CharField(max_length=35)
    Gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    acc_type = models.ForeignKey(Acc_Type, on_delete=models.CASCADE)
    FatherName = models.CharField(max_length=50)
    MotherName = models.CharField(max_length=50)
    Adhaar_Number = models.CharField(max_length=12, unique=True, db_index=True)
    Address = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    account_number = models.CharField(max_length=15, unique=True, editable=False)
    Pin_Number = models.CharField(max_length=256)
    Balance_Amount = models.BigIntegerField(default=0)
    otp = models.CharField(max_length=6, blank=True, null=True) 
    otp_created_at = models.DateTimeField(blank=True, null=True) 

    def set_pin(self, raw_pin):
        self.Pin_Number = make_password(raw_pin)
        self.save()

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.Pin_Number)
    
    def generate_otp(self):
        import random
        self.otp = f"{random.randint(100000, 999999)}"
        self.otp_created_at = datetime.now()
        self.save()

    def verify_otp(self, otp_input):
        if self.otp == otp_input and self.otp_created_at > datetime.now() - timedelta(minutes=10):
            return True
        return False

    def clear_otp(self):
        self.otp = None
        self.otp_created_at = None
        self.save()
    
    def __str__(self):
        return f'account_number : {self.account_number}'
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is a new instance
            last_account = Bank.objects.order_by('-account_number').first()
            if last_account:
                self.account_number = str(int(last_account.account_number) + 1)
            else:
                self.account_number = "42770823"
        super().save(*args, **kwargs)

class Transaction(models.Model):
    account = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20)  # e.g., 'withdrawal', 'deposit', 'transfer'
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.timestamp}"