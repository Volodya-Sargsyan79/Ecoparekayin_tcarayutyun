from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

# Create your views here.


class GetEmployeeList(APIView):
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
            columns = [col[0] for col in cursor.description]  # <-- Get column names
            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]
            
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error using log_error function
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetEmployeeRelativesList(APIView):
    def get(self, request):

        id = request.GET.get('id') or ''

        sql = '''
            SELECT 
                employee_person.id,
                employee_relatives.name, 
                employee_person.first_name, 
                employee_person.last_name, 
                employee_person.birthday, 
                employee_person.passport, 
                employee_person.id_card,
                employee_person.hvhh,
                employee_person.img FROM employee_employees JOIN employee_relatives ON employee_relatives.employee_id = employee_employees.id
            JOIN employee_person ON employee_person.id = employee_relatives.person_id
            WHERE employee_employees.id = %s
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
        

class GetEmployeePalsList(APIView):
    def get(self, request):

        id = request.GET.get('id') or ''

        sql = '''
            SELECT 
                employee_person.id,
                employee_pals.name, 
                employee_person.first_name, 
                employee_person.last_name, 
                employee_person.birthday, 
                employee_person.passport, 
                employee_person.id_card,
                employee_person.hvhh,
                employee_person.img FROM employee_employees JOIN employee_pals ON employee_pals.employee_id = employee_employees.id
            JOIN employee_person ON employee_person.id = employee_pals.person_id
            WHERE employee_employees.id = %s
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
        
class GetEmployeeFriendsList(APIView):
    def get(self, request):

        id = request.GET.get('id') or ''

        sql = '''
            SELECT 
                employee_person.id,
                employee_friends.name, 
                employee_person.first_name, 
                employee_person.last_name, 
                employee_person.birthday, 
                employee_person.passport, 
                employee_person.id_card,
                employee_person.hvhh,
                employee_person.img FROM employee_employees JOIN employee_friends ON employee_friends.employee_id = employee_employees.id
            JOIN employee_person ON employee_person.id = employee_friends.person_id
            WHERE employee_employees.id = %s
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
        
class GetEmployeeRelationList(APIView):
    def get(self, request):

        id = request.GET.get('id') or ''

        sql = '''
            SELECT 
                employee_person.id,
                employee_relation.name, 
                employee_person.first_name, 
                employee_person.last_name, 
                employee_person.birthday, 
                employee_person.passport, 
                employee_person.id_card,
                employee_person.hvhh,
                employee_person.img FROM employee_employees JOIN employee_relation ON employee_relation.employee_id = employee_employees.id
            JOIN employee_person ON employee_person.id = employee_relation.person_id
            WHERE employee_employees.id = %s
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