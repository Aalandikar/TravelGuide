# Generated by Django 5.0.5 on 2024-06-26 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0005_remove_destination_amount_booking_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
    ]
