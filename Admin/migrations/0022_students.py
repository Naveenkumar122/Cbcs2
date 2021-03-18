# Generated by Django 3.1.5 on 2021-03-15 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0021_auto_20210314_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rollno', models.CharField(max_length=50, unique=True)),
                ('Name', models.CharField(max_length=100)),
                ('Batch', models.CharField(max_length=50)),
                ('Department', models.CharField(max_length=10)),
            ],
        ),
    ]
