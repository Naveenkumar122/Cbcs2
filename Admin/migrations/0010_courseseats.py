# Generated by Django 3.1.5 on 2021-03-08 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0009_course_coursetype'),
    ]

    operations = [
        migrations.CreateModel(
            name='courseSeats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseCode', models.CharField(max_length=10, unique=True)),
                ('seats', models.IntegerField()),
            ],
        ),
    ]
