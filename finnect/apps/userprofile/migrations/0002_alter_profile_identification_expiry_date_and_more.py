# Generated by Django 5.1.5 on 2025-03-01 02:54

import datetime
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='identification_expiry_date',
            field=models.DateField(default=datetime.date(2030, 1, 1), verbose_name='ID or Passport Expiry Date'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='identification_issue_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='ID or Passport Issue Date'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+5599999999', max_length=128, region=None, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='place_of_birth',
            field=models.CharField(default='unknown', max_length=255, verbose_name='Place of Birth'),
        ),
    ]
