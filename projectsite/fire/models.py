from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import now

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    
def validate_not_future(value):
        if value > now():
            raise ValidationError('Future dates are not allowed.')


def validate_not_negative(value):
    if value < 0:
        raise ValidationError('Value cannot be negative.')


class Locations(BaseModel):
    name = models.CharField(max_length=150)
    latitude = models.DecimalField(
        max_digits=22, decimal_places=16, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=22, decimal_places=16, null=True, blank=True)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)  # can be in separate table
    country = models.CharField(max_length=150)  # can be in separate table

    def __str__(self):
        return self.name

class Incident(BaseModel):
    SEVERITY_CHOICES = (
        ('Minor Fire', 'Minor Fire'),
        ('Moderate Fire', 'Moderate Fire'),
        ('Major Fire', 'Major Fire'),
    )
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=now, blank=True, null=True, validators=[validate_not_future])  # Use timezone-aware default
    severity_level = models.CharField(max_length=45, choices=SEVERITY_CHOICES)
    description = models.CharField(max_length=250)

    def __str__(self):
        # Safely handle date_time if it's null
        return f"Incident at {self.location} on {self.date_time.strftime('%Y-%m-%d %H:%M:%S') if self.date_time else 'Unknown'}"


class FireStation(BaseModel):
    name = models.CharField(max_length=150)
    latitude = models.DecimalField(
        max_digits=22, decimal_places=16, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=22, decimal_places=16, null=True, blank=True)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)  # can be in separate table
    country = models.CharField(max_length=150)  # can be in separate table

    def __str__(self):
        return self.name


class Firefighters(BaseModel):
    RANK_CHOICES = (
        ('Probationary Firefighter', 'Probationary Firefighter'),
        ('Firefighter I', 'Firefighter I'),
        ('Firefighter II', 'Firefighter II'),
        ('Firefighter III', 'Firefighter III'),
        ('Driver', 'Driver'),
        ('Captain', 'Captain'),
        ('Battalion Chief', 'Battalion Chief'),
    )
    name = models.CharField(max_length=150)
    rank = models.CharField(max_length=150, choices=RANK_CHOICES)
    experience_level = models.CharField(max_length=150) 
    station = models.ForeignKey(FireStation, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name


class FireTruck(BaseModel):
    truck_number = models.CharField(max_length=150)
    model = models.CharField(max_length=150)
    capacity = models.CharField(max_length=150)  # water
    station = models.ForeignKey(FireStation, on_delete=models.CASCADE)


class WeatherConditions(BaseModel):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_not_negative])
    humidity = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_not_negative])
    wind_speed = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_not_negative])
    weather_description = models.CharField(max_length=150)

    def __str__(self):
        return f"Weather for {self.incident.location} on {self.incident.date_time.strftime('%Y-%m-%d %H:%M:%S')} "