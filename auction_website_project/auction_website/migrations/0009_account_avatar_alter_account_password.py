# Generated by Django 4.2.1 on 2023-05-10 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_website', '0008_alter_account_city_alter_account_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='avatar',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='account',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
