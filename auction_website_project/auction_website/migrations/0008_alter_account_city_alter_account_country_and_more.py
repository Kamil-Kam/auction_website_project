# Generated by Django 4.2.1 on 2023-05-09 20:06

import auction_website.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_website', '0007_rename_password1_account_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='city',
            field=models.CharField(max_length=30, validators=[auction_website.validators.validate_name]),
        ),
        migrations.AlterField(
            model_name='account',
            name='country',
            field=models.CharField(max_length=20, validators=[auction_website.validators.validate_name]),
        ),
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[auction_website.validators.validate_email]),
        ),
        migrations.AlterField(
            model_name='account',
            name='firstname',
            field=models.CharField(max_length=20, validators=[auction_website.validators.validate_name]),
        ),
        migrations.AlterField(
            model_name='account',
            name='postcode',
            field=models.CharField(max_length=10, validators=[auction_website.validators.validate_postcode]),
        ),
        migrations.AlterField(
            model_name='account',
            name='street',
            field=models.CharField(max_length=30, validators=[auction_website.validators.validate_name]),
        ),
        migrations.AlterField(
            model_name='account',
            name='surname',
            field=models.CharField(max_length=20, validators=[auction_website.validators.validate_name]),
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=20, unique=True, validators=[auction_website.validators.validate_username]),
        ),
    ]
