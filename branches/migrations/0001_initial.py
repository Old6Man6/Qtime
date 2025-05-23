# Generated by Django 5.2.1 on 2025-05-19 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Branch name')),
                ('location', models.CharField(blank=True, max_length=255, null=True, verbose_name='Location')),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True, verbose_name='Phone number')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Service name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('duration_minutes', models.PositiveIntegerField(verbose_name='Duration (minutes)')),
                ('price', models.DecimalField(decimal_places=0, help_text='Enter the price in Toman, without decimals', max_digits=12, verbose_name='Price (Toman)')),
            ],
        ),
    ]
