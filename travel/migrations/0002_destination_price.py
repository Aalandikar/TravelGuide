# Generated by Django 5.0.5 on 2024-06-19 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10000, max_digits=10),
        ),
    ]
