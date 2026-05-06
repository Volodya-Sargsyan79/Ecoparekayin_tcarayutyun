from django.shortcuts import render
from .ami import originate_ami_call
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.conf import settings
from .models import CallRecord
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.utils.timezone import localtime

from django.db import connection
from rest_framework import status


def safe_parse(dt_str):
    if not dt_str:
        return None

    dt = parse_datetime(dt_str)

    if dt is None:
        return None

    # force timezone aware (IMPORTANT)
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_default_timezone())

    return dt


class MakeCallAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'error': 'no phone_number'}, status=400)

        ami_user = "NAV_OKKTA"   # ⚠️ manager.conf user
        ami_pass = "Nav@2026AM!**"
        pbx_ip = "192.168.1.5"

        try:
            res = originate_ami_call(phone_number, ami_user, ami_pass, pbx_ip)

            return Response({
                'status': 'call_sent',
                'call_to': phone_number,
                'pbx_result': res
            })

        except Exception as e:
            return Response({'error': str(e)}, status=500)
        

@csrf_exempt
def upload_call_record(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    file = request.FILES.get('file')
    call_id = request.POST.get('call_id') or None
    caller_number = request.POST.get('caller_number') or ''
    called_number = request.POST.get('called_number') or ''
    call_start = request.POST.get('call_start')  # expect ISO string
    call_end = request.POST.get('call_end')
    call_duration = request.POST.get('call_duration')
    shift_id = request.POST.get('shift_id') or None

    if not file or not call_id:
        return JsonResponse({'error': 'file and call_id required'}, status=400)

    # Try to parse datetimes
    parsed_start = safe_parse(call_start)
    parsed_end = safe_parse(call_end)

    # create or update CallRecord
    record, created = CallRecord.objects.get_or_create(call_id=call_id, defaults={
        'caller_number': caller_number,
        'called_number': called_number,
        'call_start': parsed_start if parsed_start else None,
        'call_end': parsed_end if parsed_end else None,
        'call_duration': int(call_duration) if call_duration else 0,
        'shift_id': shift_id,
        'status': 'recorded',
    })

    # if exists, update basic fields
    if not created:
        record.caller_number = caller_number
        record.called_number = called_number
        record.call_start = parsed_start
        record.call_end = parsed_end
        record.call_duration = int(call_duration or 0)
        record.shift_id = shift_id
        record.status = 'recorded'

    # save file to FileField (Django handles saving to MEDIA_ROOT)
    record.recording_file.save(file.name, file, save=False)
    record.recording_size = file.size
    # Optionally set recording_url (if you want absolute URL)
    try:
        record.recording_url = request.build_absolute_uri(record.recording_file.url)
    except Exception:
        record.recording_url = ''
    record.save()

    return JsonResponse({
        'ok': True,
        'id': record.id,
        'call_id': record.call_id,
        'recording_url': record.recording_url,
        'recording_size': record.recording_size,
    })


class GetCallsList(APIView):
    def get(self, request):
    
        shift_id = request.GET.get('shift_id') or ''

        sql = '''
            SELECT call_start, caller_number, called_number, recording_url 
            FROM ekopatrol.phone_callrecord 
            WHERE shift_id = %s;
        '''

        try:
            cursor = connection.cursor()
            cursor.execute(sql, [shift_id])
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)