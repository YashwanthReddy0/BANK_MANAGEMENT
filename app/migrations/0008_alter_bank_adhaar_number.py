# Generated by Django 5.0.7 on 2024-08-28 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='Adhaar_Number',
            field=models.CharField(db_index=True, max_length=12, unique=True),
        ),
    ]
