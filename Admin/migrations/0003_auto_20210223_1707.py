# Generated by Django 3.1.5 on 2021-02-23 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0002_student_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_detail',
            name='Rollno',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
