# Generated by Django 4.2.13 on 2024-09-16 11:29

import cloudinary.models
from django.db import migrations, models
import django_ckeditor_5.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('price', models.FloatField(blank=True, null=True)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='images')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('status', models.CharField(choices=[('VACUITY', 'Trống'), ('NONVACUITY', 'Không trống')], default='VACUITY', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BillRentalContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('bill_number', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('total', models.FloatField()),
                ('status', models.CharField(choices=[('PAID', 'Đã thanh toán'), ('UNPAID', 'Chưa thanh toán')], default='UNPAID', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ElectricityAndWaterBills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('total_cubic_meters_water', models.FloatField()),
                ('total_electricity', models.FloatField()),
                ('total_amount', models.FloatField()),
                ('status', models.CharField(choices=[('PAID', 'Đã thanh toán'), ('UNPAID', 'Chưa thanh toán')], default='UNPAID', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='images')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RentalContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('rental_number', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('time_rental', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('CANCEL', 'Hủy'), ('PROCESSING', 'Đang xử lý'), ('SUCCESS', 'Thành công'), ('FAIL', 'Thất bại')], default='PROCESSING', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='images')),
                ('number_of_bed', models.IntegerField(blank=True, null=True)),
                ('type', models.CharField(choices=[('NORMAL', 'Phòng thường'), ('SERVICE', 'Phòng dịch vụ')], default='NORMAL', max_length=255)),
                ('room_for', models.CharField(choices=[('MALE', 'Nam'), ('FEMALE', 'Nữ')], default='MALE', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ViolateNotice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('violate_number', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
