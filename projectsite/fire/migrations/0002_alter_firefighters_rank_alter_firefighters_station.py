# Generated by Django 4.2.11 on 2024-11-15 14:02

import fire.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fire', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firefighters',
            name='rank',
            field=models.CharField(choices=[('Probationary Firefighter', 'Probationary Firefighter'), ('Firefighter I', 'Firefighter I'), ('Firefighter II', 'Firefighter II'), ('Firefighter III', 'Firefighter III'), ('Driver', 'Driver'), ('Captain', 'Captain'), ('Battalion Chief', 'Battalion Chief')], max_length=150),
        ),
        migrations.AlterField(
            model_name='firefighters',
            name='station',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fire.firestation'),
        ),

        migrations.AlterField(
            model_name='incident',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True, validators=[fire.models.validate_not_future]),
        ),
        migrations.AlterField(
            model_name='weatherconditions',
            name='humidity',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[fire.models.validate_not_negative]),
        ),
        migrations.AlterField(
            model_name='weatherconditions',
            name='temperature',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[fire.models.validate_not_negative]),
        ),
        migrations.AlterField(
            model_name='weatherconditions',
            name='wind_speed',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[fire.models.validate_not_negative]),
        ),
    ]
