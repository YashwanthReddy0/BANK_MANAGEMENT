from datetime import timedelta, timezone
import email
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from .forms import BankForm,PinForm
from .models import Bank, Transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Bank
from django.core.mail import send_mail
from random import randint
from django.contrib import messages


def details(request):
    form = BankForm(request.POST)
    account = None
    if form.is_valid():
        if form.is_valid():
            account = form.save(commit=False)
            account.set_pin(form.cleaned_data['Pin_Number'])
            account.save()
            print(account.FirstName)
            return render(request, 'bank.html', {'form': form, 'account': account})
        return redirect('bankdetails')        
    else:
        form = BankForm()
    return render(request, 'bank.html', {'form': form, 'account': account})

def validate_pin(request):
    Balance =None
    id=None
    if request.method =='POST':
        form = PinForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data['account_number']
            Pin_Number = form.cleaned_data['Pin_Number']
            try:
                account_number=Bank.objects.get(account_number=account_number)
                if account_number.check_pin(Pin_Number):
                    
                    Balance=account_number.Balance_Amount
                    id=account_number.id                    
                else:
                    form.add_error('Pin_Number','Invalid Pin')
            except Bank.DoesNotExist:
                form.add_error('account_number','Account Not Found')
    else:
        form =PinForm()
    context = {
    'form':form,
    'Balance':Balance,
    'id':id
    }
    return render(request,'validate.html',context)

def withdraw(request, pk):
    data = Bank.objects.get(id=pk)
    if request.method == 'POST':
        amount = int(request.POST.get('Amount'))
        if amount <= data.Balance_Amount:
            data.Balance_Amount -= amount
            data.save()
         
            Transaction.objects.create(
                account=data,
                transaction_type='withdrawal',
                amount=amount,
                description=f'Withdrawal of Rs.{amount}'
            )
            return HttpResponse('<h1>Transaction Successful</h1>')
        else:
            return HttpResponse('Insufficient Balance')
    return render(request, 'Option.html')

def deposit(request, pk):
    data = Bank.objects.get(id=pk)
    if request.method == 'POST':
        amount = str(int(request.POST.get('Amount')))
        if int(amount) > 0:
            data.Balance_Amount += int(amount)
            data.save()

            Transaction.objects.create(
                account=data,
                transaction_type='Deposit',
                amount=amount,
                description=f'Deposit of Rs.{amount}'
            )
            return HttpResponse('<h1>Transaction Successful</h1>')
            
        else:
            return HttpResponse('Amount must be more than Zero Rupees')
    return render(request, 'Option.html')

def transfer(request, pk):
    
    data = get_object_or_404(Bank, id=pk)
    if request.method == "POST":
       
        acc = request.POST.get('transfer_account_number')  
        amount = request.POST.get('amount')               

        try:
            
            data1 = Bank.objects.get(account_number=acc)
            
            amount = int(amount)

            if data1.account_number == data.account_number:
                return HttpResponse('Unable to transfer to the same account')
            else:
                if amount <= data.Balance_Amount:
                   
                    data1.Balance_Amount += amount
                    data.Balance_Amount -= amount
                    data1.save()
                    data.save()

                    Transaction.objects.create(
                        account=data,
                        transaction_type='transfer',
                        amount=amount,
                        description=f'Transfer of Rs.{amount} to account {data1.account_number}'
                    )
                    Transaction.objects.create(
                        account=data1,
                        transaction_type='deposit',
                        amount=amount,
                        description=f'Received Rs.{amount} from account {data.account_number}'
                    )

                    return HttpResponse('<h1>Transaction Successful</h1>')
                else:
                    return HttpResponse('Insufficient balance')
        except Bank.DoesNotExist:
           
            return HttpResponse('Account number not found')

    return render(request, 'transfer.html')

def forgot_account_number(request):
    account = None
    if request.method == 'POST':
        aadhaar_number = request.POST.get('Adhaar_Number')
        print(f"Received Aadhaar Number: {aadhaar_number}")  

        try:
      
            account = Bank.objects.get(Adhaar_Number=aadhaar_number)
            print(f"Found Account: {account}")  

            send_mail(
    f'Hello {account.FirstName} {account.MiddleName} {account.LastName},\n\n'
    'We have received a request for your account information.\n\n'
    f'Your account number is: {account.account_number}\n'
    f'Account Type: {account.account_type}\n\n'
    'Please keep this information secure and do not share it with anyone.\n'
    'If you did not request this information or if you have any concerns, please contact our support team immediately.\n\n'
    'Thank you for banking with YR BANK OF NEW ZEALAND.\n'
    'Best regards,\n'
    'YR BANK OF NEW ZEALAND',
    'toughestman07@gmail.com',
    [account.email],
    fail_silently=False,
)


        
            return render(request, 'account_details.html', {'account': account})

        except Bank.DoesNotExist:
            messages.error(request, 'Account with this Aadhaar number does not exist.')

    return render(request, 'forgot_account_number.html')





def forgot_pin(request):
    if request.method == 'POST':
        
        account_number = request.POST.get('account_number')

        try:
            
            account = Bank.objects.get(account_number=account_number)
          
            if 'send_email' in request.POST:
                otp = randint(100000, 999999)
                account.otp = otp
                account.save()

                send_mail(
    f'Hello {account.FirstName} {account.MiddleName} {account.LastName}, Welcome to YR BANK OTP VERIFICATION USER WORLD',
    f'Dear {account.FirstName},\n\n'
    'Welcome to YR BANK! We are pleased to assist you with the OTP verification process.\n\n'
    f'Your OTP for PIN Reset is: {otp}\n'
    'Please note that this OTP is valid for 300 seconds and you have only 3 attempts to enter it correctly. '
    'If you fail to enter the OTP correctly within 3 attempts, your account will be blocked for 1 hour.\n\n'
    'Please follow the instructions carefully to ensure a smooth verification process.\n\n'
    'Thank you for reaching out to YR BANK OF NEW ZEALAND.\n'
    'Best regards,\n'
    'YR BANK OF NEW ZEALAND',
    'toughestman07@gmail.com',
    [account.email],
    fail_silently=False,
)

                
                request.session['email'] = account.email
                return redirect('verify_otp')
        
        except Bank.DoesNotExist:
            messages.error(request, 'Account with this account number does not exist.')
    
    return render(request, 'forgot_pin.html')


def verify_otp(request):
    email = request.session.get('email')  

    attempt_count = request.session.get('attempt_count', 0)
    last_attempt_time = request.session.get('last_attempt_time')
    block_duration = timedelta(hours=1) 

    if last_attempt_time:
        last_attempt_time = timezone.datetime.fromisoformat(last_attempt_time)
    else:
        last_attempt_time = timezone.now() - block_duration 

    if attempt_count >= 3 and timezone.now() < last_attempt_time + block_duration:
        remaining_time = (last_attempt_time + block_duration - timezone.now()).seconds // 60
        if remaining_time > 0:
            messages.error(request, f'You have reached the maximum attempts. Try again after {remaining_time} minutes. Your account is blocked for 1 hour.')
            return render(request, 'verify_otp.html', {'email': email, 'blocked': True})

    if request.method == 'POST':
       
        otp_entered = (
            request.POST.get('otp1', '') +
            request.POST.get('otp2', '') +
            request.POST.get('otp3', '') +
            request.POST.get('otp4', '') +
            request.POST.get('otp5', '') +
            request.POST.get('otp6', '')
        )

        try:
            
            account = Bank.objects.get(email=email, otp=otp_entered)
        
            request.session['attempt_count'] = 0
            request.session['last_attempt_time'] = None
            
            return redirect('reset_pin', pk=account.pk) 
        except Bank.DoesNotExist:
            attempt_count += 1
            print(attempt_count)
            request.session['attempt_count'] = attempt_count
            request.session['last_attempt_time'] = timezone.now().isoformat()  

            if attempt_count >= 3:
                messages.error(request, 'You have reached the maximum number of attempts. Your account is blocked for 1 hour.')
                return render(request, 'verify_otp.html', {'email': email, 'blocked': True})
            else:
                messages.error(request, f'Invalid OTP. You have {3 - attempt_count} attempt(s) left.')
                return render(request, 'verify_otp.html', {'email': email})

    return render(request, 'verify_otp.html', {'email': email})




def reset_pin(request, pk):
    if request.method == 'POST':
        new_pin = request.POST.get('new_pin')
        confirm_pin = request.POST.get('confirm_pin')
        email = request.session.get('email')
        if new_pin == confirm_pin:
            account = Bank.objects.get(email=email)
            account.set_pin(new_pin)
            account.otp = None  
            account.save()
            messages.success(request, 'PIN successfully reset.')
            return redirect('validate_pin')
        else:
            messages.error(request, 'PINs do not match.')
    return render(request, 'reset_pin.html')



def transaction_history(request, pk):
    account = Bank.objects.get(id=pk)
    transactions = account.transactions.all().order_by('-timestamp')
    
    context = {
        'account': account,
        'transactions': transactions,
        'id': account.id,
    }
    return render(request, 'history.html', context)