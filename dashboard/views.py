import csv
import io
import requests
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')



def daily_activity(request):
    if request.method == 'POST':
        tenant_url = request.POST.get('tenant_url')
        access_token = request.POST.get('access_token')
        timeframe = request.POST.get('timeframe')
        # Here we'll later add logic to download Dynatrace report based on timeframe
        # For now just pass the inputs back to the template
        context = {
            'tenant_url': tenant_url,
            'access_token': access_token,
            'timeframe': timeframe,
            'message': 'Report logic placeholder'
        }
        return render(request, 'daily_activity.html', context)
    return render(request, 'daily_activity.html')

def problem_data(request):
    return render(request, 'problem_data.html')

def user_management(request):
    return render(request, 'user_management.html')

