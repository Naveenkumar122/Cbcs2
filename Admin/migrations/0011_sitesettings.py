# Generated by Django 3.1.5 on 2021-03-08 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0010_courseseats'),
    ]

    operations = [
        migrations.CreateModel(
            name='siteSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
            ],
        ),
    ]
