from django.shortcuts import render
from .ami import originate_ami_call

from rest_framework.views import APIView
from rest_framework.response import Response


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