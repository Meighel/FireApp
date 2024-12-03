from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from fire.models import Locations, Incident, FireStation, Firefighters, FireTruck, WeatherConditions
from fire.forms import FireStationForm, FireTruckForm, LocationsForm, IncidentForm, WeatherConditionsForm
from django.urls import reverse_lazy
from django.db import connection
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from datetime import datetime
from django.shortcuts import render
from geopy.distance import geodesic
from django.contrib import messages


class HomePageView(ListView):
    model = Locations
    context_object_name = 'home'
    template_name = "home.html"

class ChartView(ListView):
    template_name = 'chart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass


def PieCountbySeverity(request):
    query = '''
    SELECT severity_level, COUNT(*) as count
    FROM fire_incident
    GROUP BY severity_level 
    '''
    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    if rows:
        # Construct the directory with severity level as keys and count as values
        data = {severity: count for severity, count in rows}
    else:
        data = {}

    return JsonResponse(data)

def LineCountByMonth(request):
    current_year = datetime.now().year

    incidents_per_month = (
        Incident.objects.filter(date_time__year=current_year)
        .annotate(month=ExtractMonth('date_time'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    result = {month: 0 for month in range(1, 13)}

    for item in incidents_per_month:
        result[item['month']] = item['count']

    month_names = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }

    result_with_month_names = {
        month_names[month]: count for month, count in result.items()
    }

    return JsonResponse(result_with_month_names)

def MultilineIncidentTop3Country(request):

    query = '''
    SELECT
        fl.country,
        strftime('%m', fi.date_time) AS month,
        COUNT(fi.id) AS incident_count
    FROM
        fire_incident fi
    JOIN
        fire_locations fl ON fi.location_id = fl.id
    WHERE
        fl.country IN (
            SELECT
                fl_top.country
            FROM
                fire_incident fi_top
            JOIN
                fire_locations fl_top ON fi_top.location_id = fl_top.id
            WHERE
                strftime('%Y', fi_top.date_time) = strftime('%Y', 'now')
            GROUP BY
                fl_top.country
            ORDER BY
                COUNT(fi_top.id) DESC
            LIMIT 3
        )   
        AND strftime('%Y', fi.date_time) = strftime('%Y', 'now')
    GROUP BY
        fl.country, month
    ORDER BY
        fl.country, month;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Initialize a dictionary to store the result
    result = {}

    # Initialize a set of months from January to December
    months = set(str(i).zfill(2) for i in range(1, 13))

    # Loop through the query results
    for row in rows:
        country = row[0]
        month = row[1]
        total_incidents = row[2]

        # If the country is not in the result dictionary, initialize it with all months set to zero
        if country not in result:
            result[country] = {month: 0 for month in months}

        # Update the incidents count for the corresponding month
        result[country][month] = total_incidents

    # Ensure there are always 3 countries in the result
    while len(result) < 3:
        # Placeholder name for missing countries
        missing_country = f"Country {len(result) + 1}"
        result[missing_country] = {month: 0 for month in months}

    for country in result:
        result[country] = dict(sorted(result[country].items()))

    return JsonResponse(result)

def multipleBarbySeverity(request):
    query = '''
    SELECT
        fi.severity_level,
        strftime('%m', fi.date_time) AS month,
        COUNT(fi.id) AS incident_count
    FROM
        fire_incident fi
    GROUP BY fi.severity_level, month
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    result = {}
    months = {str(i).zfill(2) for i in range(1, 13)}  # Ensure all months are included

    for row in rows:
        severity_level = row[0]
        month = row[1]
        count = row[2]

        if severity_level not in result:
            result[severity_level] = {month: 0 for month in months}

        result[severity_level][month] = count

    # Sort months within each severity level
    for severity_level in result:
        result[severity_level] = dict(sorted(result[severity_level].items()))

    return JsonResponse(result)

def map_station(request):
    fireStations = FireStation.objects.values('name', 'latitude', 'longitude')

    for fs in fireStations:
        fs['latitude'] = float(fs['latitude'])
        fs['longitude'] = float(fs['longitude'])
    
    fireStations_list = list(fireStations)

    context = {
        'fireStations' : fireStations_list,
    }
    
    return render(request, 'map_station.html', context)

def map_incident_view(request):
    incidents = Incident.objects.select_related('location').all().values(
        'location__latitude', 'location__longitude', 'severity_level', 'location__name', 'location__city'
    )

    cities = Locations.objects.values('city').distinct()

    for incident in incidents:
        incident['location__latitude'] = float(incident['location__latitude'])
        incident['location__longitude'] = float(incident['location__longitude'])

    incidents_list = list(incidents)

    return render(request, 'map_incident.html', {
        'incidents': incidents_list,
        'cities': cities,
    })

class FireStationsList(ListView):
    model = FireStation
    context_object_name = 'fire_station'
    template_name = 'firestation_list.html'
    paginate_by = 5

class FireStationCreateView(CreateView):
    model = FireStation
    form_class = FireStationForm
    template_name = 'firestation_add.html'
    success_url = reverse_lazy('station-list')

    def form_valid(self, form):
        messages.success(self.request, 'The station has been successfully added.')

        return super().form_valid(form)
    
class FireStationUpdateView(UpdateView):
    model = FireStation
    form_class = FireStationForm
    template_name = 'firestation_edit.html'
    success_url = reverse_lazy('station-list')

    def form_valid(self, form):
        messages.success(self.request, 'The station has been successfully updated.')

        return super().form_valid(form)

class FireStationDeleteView(DeleteView):
    model = FireStation
    template_name = 'firestation_del.html'
    success_url = reverse_lazy('station-list')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully deleted.')

        return super().form_valid(form)

class FireTruckList(ListView):
    model = FireTruck
    context_object_name = 'fire_truck'
    template_name = 'firetruck_list.html'
    paginate_by = 5

class FireTruckCreateView(CreateView):
    model = FireTruck
    form_class = FireTruckForm
    template_name = 'firetruck_add.html'
    success_url = reverse_lazy('truck-list')

    def form_valid(self, form):
        messages.success(self.request, 'The truck has been successfully added.')

        return super().form_valid(form)
    
class FireTruckUpdateView(UpdateView):
    model = FireTruck
    form_class = FireTruckForm
    template_name = 'firetruck_edit.html'
    success_url = reverse_lazy('truck-list')

    def form_valid(self, form):
        messages.success(self.request, 'The truck has been successfully updated.')

        return super().form_valid(form)
    
class FireTruckDeleteView(DeleteView):
    model = FireTruck
    template_name = 'firetruck_del.html'
    success_url = reverse_lazy('truck-list')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully deleted.')

        return super().form_valid(form)

class IncidentList(ListView):
    model = Incident
    context_object_name = 'incident'
    template_name = 'incident_list.html'
    paginate_by = 5

class IncidentCreateView(CreateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'incident_add.html'
    success_url = reverse_lazy('incident-list')

    def form_valid(self, form):
        messages.success(self.request, 'The incident has been successfully added.')

        return super().form_valid(form)

class IncidentUpdateView(UpdateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'incident_edit.html'
    success_url = reverse_lazy('incident-list')

    def form_valid(self, form):
        messages.success(self.request, 'The incident has been successfully updated.')

        return super().form_valid(form)

class IncidentDeleteView(DeleteView):
    model = Incident
    template_name = 'incident_del.html'
    success_url = reverse_lazy('incident-list')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully deleted.')

        return super().form_valid(form)

class LocationsList(ListView):
    model = Locations
    context_object_name = 'locations'
    template_name = 'locations_list.html'
    paginate_by = 5

class LocationsCreateView(CreateView):
    model = Locations
    form_class = LocationsForm
    template_name = 'locations_add.html'
    success_url = reverse_lazy('locations-list')

    def form_valid(self, form):
        messages.success(self.request, 'The location has been successfully added.')

        return super().form_valid(form)

class LocationsUpdateView(UpdateView):
    model = Locations
    form_class = LocationsForm
    template_name = 'locations_edit.html'
    success_url = reverse_lazy('locations-list')

    def form_valid(self, form):
        messages.success(self.request, 'The location has been successfully updated.')

        return super().form_valid(form)

class LocationsDeleteView(DeleteView):
    model = Locations
    template_name = 'locations_del.html'
    success_url = reverse_lazy('locations-list')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully deleted.')

        return super().form_valid(form)

class WeatherConditionsList(ListView):
    model = WeatherConditions
    context_object_name = 'weather_condition'
    template_name = 'weatherconditions_list.html'
    paginate_by = 5

class WeatherConditionsCreateView(CreateView):
    model = WeatherConditions
    form_class = WeatherConditionsForm
    template_name = 'weatherconditions_add.html'
    success_url = reverse_lazy('weather-list')

    def form_valid(self, form):
        messages.success(self.request, 'The weather condition has been successfully added.')

        return super().form_valid(form)

class WeatherConditionsUpdateView(UpdateView):
    model = WeatherConditions
    form_class = WeatherConditionsForm
    template_name = 'weatherconditions_edit.html'
    success_url = reverse_lazy('weather-list')

    def form_valid(self, form):
        messages.success(self.request, 'The weather condition has been successfully updated.')

        return super().form_valid(form)

class WeatherConditionsDeleteView(DeleteView):
    model = WeatherConditions
    template_name = 'weatherconditions_del.html'
    success_url = reverse_lazy('weather-list')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully deleted.')

        return super().form_valid(form)