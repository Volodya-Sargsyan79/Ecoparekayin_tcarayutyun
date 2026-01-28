from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

# Create your views here.

# @api_view(['POST'])
# def create_fire_call(request):
#     StartCallDate.objects.create()
#     return Response({"status": "ok"})

class AddCallDate(APIView):
    def post(self, request):
        sql = '''
            INSERT INTO person_startcalldate () VALUES ();
        '''

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)

            return Response(
                {"message": "Call date added"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetRegionList(APIView):
    def get(self, request):

        sql = '''
            SELECT * FROM person_region;
        '''

        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]  # <-- Get column names
            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]
            
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error using log_error function
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetPrecinctList(APIView):
    def get(self, request):
    
        id = request.GET.get('id') or ''

        sql = '''
            SELECT * FROM person_precinct
            WHERE person_precinct.region_id = %s;
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
        

class GetPositionList(APIView):
    def get(self, request):

        sql = '''
            SELECT * FROM person_position;
        '''

        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]  # <-- Get column names
            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]
            
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error using log_error function
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddEmployeeCaller(APIView):
    def post(self, request):

        name = request.data.get('name')
        surname = request.data.get('surname')
        phone = request.data.get('phone')
        position_id = request.data.get('position_id')
        precinct_id = request.data.get('precinct_id')
        region_id = request.data.get('region_id')

        sql = '''
            INSERT INTO person_employee 
            (name, surname, phone, position_id, precinct_id, region_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, [
                    name,
                    surname,
                    phone,
                    position_id,
                    precinct_id,
                    region_id
                ])

            return Response({"message": "Employee caller added successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetRegionArmeniaList(APIView):
    def get(self, request):

        sql = '''
            SELECT * FROM person_regionarmenia;
        '''

        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]  # <-- Get column names
            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]
            
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error using log_error function
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetCitiesList(APIView):
    def get(self, request):
    
        id = request.GET.get('id') or ''

        sql = '''
            SELECT * FROM person_cities
            WHERE person_cities.region_id = %s;
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
        
class GetVillagesList(APIView):
    def get(self, request):
    
        id = request.GET.get('id') or ''

        sql = '''
            SELECT * FROM person_villages
            WHERE person_villages.city_id = %s;
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
        
class AddCitizenCaller(APIView):
    def post(self, request):
        
        name = request.data.get('name')
        surname = request.data.get('surname')
        region_id = request.data.get('region_id')
        city_id = request.data.get('city_id')
        village_id = request.data.get('village_id')  # ✅ fixed
        street = request.data.get('street')
        house = request.data.get('house')
        apartment = request.data.get('apartment')
        phone = request.data.get('phone')
        unknown_person = request.data.get('unknown_person', False)

        print("DATA:", request.data)  # Debug

        sql = '''
            INSERT INTO person_citizen
            (
                name,
                surname,
                region_id,
                city_id,
                village_id,
                street,
                house,
                apartment,
                phone,
                unknown_person
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, [
                    name,
                    surname,
                    region_id,
                    city_id,
                    village_id,
                    street,
                    house,
                    apartment,
                    phone,
                    unknown_person
                ])

            return Response({"message": "Employee caller added successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)