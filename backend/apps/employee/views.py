from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

# Create your views here.


class GetRecommendatuinEmployee(APIView):
    def get(self, request):

        first_name = request.GET.get('first_name') or ''
        last_name = request.GET.get('last_name') or ''
        passport = request.GET.get('passport') or ''
        id_card = request.GET.get('id_card') or ''
        hvhh = request.GET.get('hvhh') or ''

        sql = '''
            SELECT * FROM employee_person 
            JOIN employee_employees ON employee_employees.person_id = employee_person.id 
            WHERE employee_person.first_name = %s AND employee_person.last_name = %s
            OR employee_person.passport = %s OR employee_person.id_card = %s or employee_person.hvhh = %s;
        '''

        try:
            cursor = connection.cursor()
            cursor.execute(sql, [
                first_name.capitalize(), 
                last_name.capitalize(), 
                passport.upper(),
                id_card,
                hvhh
            ])
            results = cursor.fetchall()
            
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error using log_error function
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)