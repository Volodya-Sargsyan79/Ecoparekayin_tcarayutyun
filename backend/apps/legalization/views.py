from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

# Create your views here.

class GetRegionList(APIView):
    def get(self, request):

        try:
            cursor = connection.cursor()

            sql = '''
                SELECT person_region.id, person_region.region
                FROM person_region;
            '''
            cursor.execute(sql)

            columns = [col[0] for col in cursor.description]

            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetPrecinctList(APIView):
    def get(self, request):
    
        id = request.GET.get('id') or ''
        try:
            cursor = connection.cursor()

            sql = '''
                SELECT * FROM person_precinct
                WHERE person_precinct.region_id = %s;
            '''
            cursor.execute(sql, [id])

            columns = [col[0] for col in cursor.description]

            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class GetLastEmployee(APIView):

    def get(self, request):
        
        precinct_id = request.GET.get('precinct_id') or ''
        position_id = request.GET.get('position_id') or ''
        try:
            cursor = connection.cursor()

            sql = '''
                SELECT DISTINCT
                    person_employee.id, 
                    name, 
                    surname, 
                    phone 
                FROM person_employee 
                LEFT JOIN person_useraccess 
                ON person_employee.precinct_id = person_useraccess.precinct_id
                WHERE person_employee.precinct_id = %s
                AND person_employee.position_id = %s
            '''
            cursor.execute(sql, [precinct_id, position_id])

            columns = [col[0] for col in cursor.description]

            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  