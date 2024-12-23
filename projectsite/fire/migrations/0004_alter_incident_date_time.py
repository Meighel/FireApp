# Generated by Django 4.2.11 on 2024-12-04 03:47

from django.db import migrations, models
import django.utils.timezone
import fire.models


class Migration(migrations.Migration):

    dependencies = [
        ('fire', '0003_alter_incident_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='date_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, validators=[fire.models.validate_not_future]),
        ),
    ]
