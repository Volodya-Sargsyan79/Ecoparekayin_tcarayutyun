from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
import calendar
from datetime import datetime, timedelta

# Create your views here.



class ScheduleView(APIView):
    
    def get(self, request):
        year = int(request.GET.get("year", 2026))
        month = int(request.GET.get("month", 3))
        start_hour = int(request.GET.get("start_hour", 9))
        shift_hours = 12

        employees = request.GET.getlist("employees") or [f"Ա{i}" for i in range(1, 17)]
        vehicles = request.GET.getlist("vehicles") or [str(1000+i) for i in range(1, 3)]

        if len(employees) < 2:
            return Response({"error": "Աշխատողների թիվը պետք է առնվազն 2 լինի"}, status=400)

        days_in_month = calendar.monthrange(year, month)[1]

        available_from = {e: datetime(year, month, 1, 0, 0) - timedelta(hours=48) for e in employees}

        schedule = []

        for day in range(1, days_in_month + 1):
            day_date = datetime(year, month, day)
            for vehicle in vehicles:

                day_shift = [e for e in employees if (day_date + timedelta(hours=start_hour) - available_from[e]).total_seconds() >= 24*3600][:2]


                night_shift = [e for e in employees if (day_date + timedelta(hours=start_hour+shift_hours) - available_from[e]).total_seconds() >= 48*3600][:2]


                day_time = f"{start_hour:02d}:00 - {(start_hour+shift_hours)%24:02d}:00"
                night_time = f"{(start_hour+shift_hours)%24:02d}:00 - {start_hour:02d}:00"

                schedule.append(
                    f"{day}-րդ օր {vehicle} մեքենա՝ օր: {' '.join(day_shift) or 'դատարկ'} {day_time}, "
                    f"գիշեր: {' '.join(night_shift) or 'դատարկ'} {night_time}"
                )

                for e in day_shift:
                    available_from[e] = day_date + timedelta(hours=start_hour + shift_hours) + timedelta(hours=24)  # 12+24 հանգիստ
                for e in night_shift:
                    available_from[e] = day_date + timedelta(hours=start_hour + 2*shift_hours) + timedelta(hours=24)  # 12+48 հանգիստ

        return Response(schedule)