from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

# Create your views here.


class GetPersonList(APIView):
    def get(self, request):

        id = request.GET.get('id') or ''
        first_name = request.GET.get('first_name') or ''
        last_name = request.GET.get('last_name') or ''
        passport = request.GET.get('passport') or ''
        id_card = request.GET.get('id_card') or ''
        hvhh = request.GET.get('hvhh') or ''

        sql = '''
            SELECT * FROM person_person 
            WHERE person_person.id = %s or  person_person.first_name = %s AND person_person.last_name = %s
            OR person_person.passport = %s OR person_person.id_card = %s or person_person.hvhh = %s;
        '''

        try:
            cursor = connection.cursor()
            cursor.execute(sql, [
                id,
                first_name.capitalize(), 
                last_name.capitalize(), 
                passport.upper(),
                id_card,
                hvhh
            ])
            columns = [col[0] for col in cursor.description]  # <-- Get column names
            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]
            
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error using log_error function
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetPersonPhoneList(APIView):
    def get(self, request):

        id = request.GET.get('person_id') or ''

        sql = '''
            SELECT 
                person_phone.phone, 
                person_phone.home, 
                person_phone.mobile, 
                person_phone.viber, 
                person_phone.whatsUp, 
                person_phone.telegram 
            FROM 
                person_phone
            WHERE 
                person_phone.person_id = %s
        '''

        try:
            cursor = connection.cursor()
            cursor.execute(sql, [
                id,
            ])
            columns = [col[0] for col in cursor.description]  # <-- Get column names
            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]
            
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error using log_error function
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetPersonAddressList(APIView):
    def get(self, request):

        id = request.GET.get('person_id') or ''

        sql = '''
            SELECT 
                person_address.country, 
                person_address.city, 
                person_address.street, 
                person_address.house, 
                person_address.apartment, 
                person_address.registration 
            FROM 
                ekopatrol.person_address
            where person_address.person_id = %s;
        '''

        try:
            cursor = connection.cursor()
            cursor.execute(sql, [
                id,
            ])
            columns = [col[0] for col in cursor.description]  # <-- Get column names
            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]
            
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error using log_error function
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetPersonRelativesList(APIView):
    def get(self, request):

        id = request.GET.get('id') or ''
        registration = request.GET.get('registration') or ''

        sql = '''
            SELECT 
                person_person.id,
                person_relatives.pal_name, 
                person_person.first_name, 
                person_person.last_name, 
                person_person.birthday, 
                person_person.passport, 
                person_person.id_card,
                person_person.hvhh,
                person_person.img
            FROM 
                person_relatives 
            JOIN 
                person_person 
            ON
                person_person.id = person_relatives.person_id
            WHERE
                person_relatives.relatives_id = %s 
            AND 
                person_relatives.registration = %s
        '''

        try:
            cursor = connection.cursor()
            cursor.execute(sql, [id, registration])
            columns = [col[0] for col in cursor.description]  # <-- Get column names
            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]
            
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error using log_error function
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetPersonWorkList(APIView):
    def get(self, request):

        id = request.GET.get('id') or ''

        sql = '''
           SELECT 
                person_person.id,
                person_employees.plase_name,
                person_employees.position_start,
                person_employees.data_of_start,
                person_employees.end_of_start,
                person_employees.degree,
                person_person.first_name, 
                person_person.last_name 
            FROM 
                person_employees
            JOIN 
                person_person
            ON 
                person_person.id=person_employees.employee_id
            WHERE 
                person_person.id=%s
        '''

        try:
            cursor = connection.cursor()
            cursor.execute(sql, [id])
            columns = [col[0] for col in cursor.description]  # <-- Get column names
            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]
            
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error using log_error function
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        