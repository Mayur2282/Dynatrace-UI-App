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


def _get_timeframe_range(timeframe):
    """Return ISO timestamps for Dynatrace timeframe (without microseconds)"""
    now = datetime.utcnow().replace(microsecond=0)
    if timeframe == "1h":
        start = now - timedelta(hours=1)
    elif timeframe == "1d":
        start = now - timedelta(days=1)
    elif timeframe == "1w":
        start = now - timedelta(weeks=1)
    else:
        start = now - timedelta(hours=1)
    # Return proper RFC3339 timestamps
    return start.strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%dT%H:%M:%SZ")


def daily_activity(request):
    if request.method == "POST":
        tenant_url = request.POST.get("tenant_url").strip().rstrip("/")

        # Auto-fix wrong domain
        if "apps.dynatrace.com" in tenant_url:
            tenant_url = tenant_url.replace("apps.dynatrace.com", "live.dynatrace.com")
        token = request.POST.get("access_token").strip()
        timeframe = request.POST.get("timeframe")

        start, end = _get_timeframe_range(timeframe)
        # # Old
        # api_url = f"{tenant_url}/api/v2/problems?from={start}&to={end}"

        # New: Include both active and closed
        api_url = f"{tenant_url}/api/v2/problems?from={start}&to={end}&status=OPEN,CLOSED"


        headers = {"Authorization": f"Api-Token {token}"}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json().get("problems", [])
            if not data:
                return render(request, "daily_activity.html", {"message": "No problem data found in this timeframe."})

            # Generate CSV
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(["Problem ID", "Title", "Impact Level", "Status", "Start Time", "End Time"])

            for p in data:
                writer.writerow([
                    p.get("problemId"),
                    p.get("title"),
                    p.get("impactLevel"),
                    p.get("status"),
                    p.get("startTime"),
                    p.get("endTime")
                ])

            buffer.seek(0)
            response_csv = HttpResponse(buffer, content_type='text/csv')
            filename = f"dynatrace_problems_{timeframe}.csv"
            response_csv['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response_csv
        else:
            return render(request, "daily_activity.html", {"message": f"Error: {response.status_code} - {response.text}"})

    return render(request, "daily_activity.html")


def problem_data(request):
    if request.method == "POST":
        tenant_url = request.POST.get("tenant_url").strip().rstrip("/")
        token = request.POST.get("access_token").strip()
        timeframe = request.POST.get("timeframe")

        start, end = _get_timeframe_range(timeframe)
        api_url = f"{tenant_url}/api/v2/problems?from={start}&to={end}"

        headers = {"Authorization": f"Api-Token {token}"}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json().get("problems", [])
            if not data:
                return render(request, "problem_data.html", {"message": "No problem data found."})

            # Generate CSV
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(["Problem ID", "Title", "Impact Level", "Status", "Start Time", "End Time"])

            for p in data:
                writer.writerow([
                    p.get("problemId"),
                    p.get("title"),
                    p.get("impactLevel"),
                    p.get("status"),
                    p.get("startTime"),
                    p.get("endTime")
                ])

            buffer.seek(0)
            response_csv = HttpResponse(buffer, content_type='text/csv')
            filename = f"problem_data_{timeframe}.csv"
            response_csv['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response_csv
        else:
            return render(request, "problem_data.html", {"message": f"Error: {response.status_code} - {response.text}"})

    return render(request, "problem_data.html")


def user_management(request):
    if request.method == "POST":
        tenant_url = request.POST.get("tenant_url").strip().rstrip("/")
        token = request.POST.get("access_token").strip()
        timeframe = request.POST.get("timeframe")

        start, end = _get_timeframe_range(timeframe)
        api_url = f"{tenant_url}/api/v2/users"

        headers = {"Authorization": f"Api-Token {token}"}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json().get("users", [])
            if not data:
                return render(request, "user_management.html", {"message": "No user data found."})

            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(["User ID", "Name", "Email", "Groups"])

            for u in data:
                writer.writerow([
                    u.get("userId"),
                    u.get("displayName"),
                    u.get("email"),
                    ", ".join(u.get("groups", []))
                ])

            buffer.seek(0)
            response_csv = HttpResponse(buffer, content_type='text/csv')
            filename = f"user_data_{timeframe}.csv"
            response_csv['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response_csv
        else:
            return render(request, "user_management.html", {"message": f"Error: {response.status_code} - {response.text}"})

    return render(request, "user_management.html")



