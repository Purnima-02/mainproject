# Generated by Django 5.0.7 on 2024-11-22 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ravi', '0008_homebasicdetail_expiry_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='pan_card_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='personaldetail',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='personaldetail',
            name='pan_card_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
