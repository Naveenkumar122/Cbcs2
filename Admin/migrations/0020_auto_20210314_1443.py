# Generated by Django 3.1.5 on 2021-03-14 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0019_auto_20210314_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin_detail',
            name='role',
            field=models.CharField(default='Admin', max_length=15),
        ),
    ]