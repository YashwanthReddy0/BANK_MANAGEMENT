# Generated by Django 5.0.7 on 2024-08-27 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_bank_otp_attempts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bank',
            old_name='Address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='bank',
            old_name='Adhaar_Number',
            new_name='adhaar_number',
        ),
        migrations.RenameField(
            model_name='bank',
            old_name='Balance_Amount',
            new_name='balance_amount',
        ),
        migrations.RenameField(
            model_name='bank',
            old_name='FatherName',
            new_name='father_name',
        ),
        migrations.RenameField(
            model_name='bank',
            old_name='FirstName',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='bank',
            old_name='Gender',
            new_name='gender',
        ),
        migrations.RenameField(
            model_name='bank',
            old_name='LastName',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='bank',
            old_name='MiddleName',
            new_name='middle_name',
        ),
        migrations.RenameField(
            model_name='bank',
            old_name='MotherName',
            new_name='mother_name',
        ),
        migrations.RenameField(
            model_name='bank',
            old_name='phoneNumber',
            new_name='phone_number',
        ),
        migrations.RenameField(
            model_name='bank',
            old_name='Pin_Number',
            new_name='pin_number',
        ),
        migrations.RenameField(
            model_name='gender',
            old_name='Gender',
            new_name='gender',
        ),
        migrations.AddField(
            model_name='bank',
            name='otp_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bank',
            name='otp_blocked_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('W', 'Withdraw'), ('D', 'Deposit'), ('T', 'Transfer')], max_length=1)),
                ('amount', models.BigIntegerField()),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.bank')),
            ],
        ),
    ]
