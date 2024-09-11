# Generated by Django 4.2.13 on 2024-09-11 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rental', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='violatenotice',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='violate_notices', to='users.manager'),
        ),
        migrations.AddField(
            model_name='violatenotice',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='violate_notices', to='rental.room'),
        ),
        migrations.AddField(
            model_name='rentalcontact',
            name='bed',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rental_contact', to='rental.bed'),
        ),
        migrations.AddField(
            model_name='rentalcontact',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rental_contacts', to='users.student'),
        ),
        migrations.AddField(
            model_name='post',
            name='room',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='rental.room'),
        ),
        migrations.AddField(
            model_name='electricityandwaterbills',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='electricity_and_water_bills', to='users.manager'),
        ),
        migrations.AddField(
            model_name='electricityandwaterbills',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='electricity_and_water_bills', to='rental.room'),
        ),
        migrations.AddField(
            model_name='billrentalcontact',
            name='rental_contact',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bill_rental_contact', to='rental.rentalcontact'),
        ),
        migrations.AddField(
            model_name='billrentalcontact',
            name='specialist',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bill_rental_contact', to='users.specialist'),
        ),
        migrations.AddField(
            model_name='billrentalcontact',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bill_rental_contact', to='users.student'),
        ),
        migrations.AddField(
            model_name='bed',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beds', to='rental.room'),
        ),
    ]
