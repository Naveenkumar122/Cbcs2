# Generated by Django 3.1.5 on 2021-02-23 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='student_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rollno', models.CharField(max_length=10)),
                ('Name', models.CharField(max_length=100)),
                ('Type', models.CharField(max_length=20)),
                ('Batch', models.CharField(max_length=10)),
            ],
        ),
    ]
