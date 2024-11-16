from django.shortcuts import render
from django.views.generic.list import ListView
from fire.models import Locations, Incident
from django.db import connection
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from datetime import datetime


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