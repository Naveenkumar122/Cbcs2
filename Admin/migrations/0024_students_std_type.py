# Generated by Django 3.1.5 on 2021-03-15 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0023_departments'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='std_type',
            field=models.ForeignKey(default=22, on_delete=django.db.models.deletion.CASCADE, to='Admin.student_type'),
            preserve_default=False,
        ),
    ]
