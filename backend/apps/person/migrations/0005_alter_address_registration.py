# Generated by Django 5.2.1 on 2025-06-09 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0004_alter_address_registration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='registration',
            field=models.CharField(choices=[('Հ', 'Հաշվառման'), ('Բ', 'Բնակության'), ('Ս', 'Սեփականություն')], max_length=15),
        ),
    ]
