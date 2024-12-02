from django.contrib import admin
from django.urls import path
from fire.views import HomePageView, IncidentList, ChartView, PieCountbySeverity, LineCountByMonth, MultilineIncidentTop3Country, multipleBarbySeverity
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

    path('incident_list/', IncidentList.as_view(), name='incident-list'),
]
