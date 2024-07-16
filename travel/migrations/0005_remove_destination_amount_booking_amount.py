# Generated by Django 5.0.5 on 2024-06-20 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0004_destination_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination',
            name='amount',
        ),
        migrations.AddField(
            model_name='booking',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]