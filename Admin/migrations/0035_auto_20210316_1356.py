# Generated by Django 3.1.5 on 2021-03-16 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0034_auto_20210316_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cdetails1',
            name='cs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.course'),
        ),
    ]
