from django.contrib import admin
from django.urls import path
from fire.views import HomePageView, FireStationsList, FireStationCreateView, FireStationUpdateView, FireStationDeleteView, FireTruckList, FireTruckCreateView, FireTruckUpdateView, FireTruckDeleteView, FireFightersList, FireFighterCreateList, FireFighterUpdateView, FireFighterDeleteView, LocationsList, LocationsCreateView, LocationsUpdateView, LocationsDeleteView, IncidentList, IncidentCreateView, IncidentUpdateView, IncidentDeleteView, WeatherConditionsList, WeatherConditionsCreateView, WeatherConditionsUpdateView, WeatherConditionsDeleteView, ChartView, PieCountbySeverity, LineCountByMonth, MultilineIncidentTop3Country, multipleBarbySeverity
from fire import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('dashboard_chart/', ChartView.as_view(), name='dashboard-chart'),
    path('chart/', PieCountbySeverity, name='chart'),
    path('lineChart/', LineCountByMonth, name='chart'),
    path('multilineChart/', MultilineIncidentTop3Country, name='chart'),
    path('multiBarChart/', multipleBarbySeverity, name='chart'),
    path('stations', views.map_station, name='map-station'),
    path('map_incident/', views.map_incident_view, name='map_incident'),

    path('firestation_list/', FireStationsList.as_view(), name='station-list'),
    path('firestation_list/add/', FireStationCreateView.as_view(), name='station-add'),
    path('firestation_list/<pk>/', FireStationUpdateView.as_view(), name='station-update'),
    path('firestation_list/<pk>/delete/', FireStationDeleteView.as_view(), name='station-delete'),
    path('firetruck_list/', FireTruckList.as_view(), name='truck-list'),
    path('firetruck_list/add/', FireTruckCreateView.as_view(), name='truck-add'),
    path('firetruck_list/<pk>/', FireTruckUpdateView.as_view(), name='truck-update'),
    path('firetruck_list/<pk>/delete', FireTruckDeleteView.as_view(), name='truck-delete'),
    path('firefighter_list/', FireFightersList.as_view(), name='fighter-list'),
    path('firefighter_list/add/', FireFighterCreateList.as_view(), name='fighter-add'),
    path('firefighter_list/<pk>/', FireFighterUpdateView.as_view(), name='fighter-update'),
    path('firefighter_list/<pk>/delete', FireFighterDeleteView.as_view(), name='fighter-delete'),
    path('locations_list/', LocationsList.as_view(), name='location-list'),
    path('locations_list/add/', LocationsCreateView.as_view(), name='location-add'),
    path('locations_list/<pk>/', LocationsUpdateView.as_view(), name='location-update'),
    path('locations_list/<pk>/delete', LocationsDeleteView.as_view(), name='location-delete'),
    path('incident_list/', IncidentList.as_view(), name='incident-list'),
    path('incident_list/add/', IncidentCreateView.as_view(), name='incident-add'),
    path('incident_list/<pk>/', IncidentUpdateView.as_view(), name='incident-update'),
    path('incident_list/<pk>/delete', IncidentDeleteView.as_view(), name='incident-delete'),
    path('weatherconditions_list/', WeatherConditionsList.as_view(), name='weather-list'), 
    path('weatherconditions_list/add/', WeatherConditionsCreateView.as_view(), name='weather-add'),
    path('weatherconditions_list/<pk>/', WeatherConditionsUpdateView.as_view(), name="weather-update"),
    path('weatherconditions_list/<pk>/delete', WeatherConditionsDeleteView.as_view(), name='weather-delete'),
]
