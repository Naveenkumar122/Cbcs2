# Generated by Django 3.1.5 on 2021-03-17 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0040_custom_admin_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='seats',
            field=models.IntegerField(default=0),
        ),
    ]