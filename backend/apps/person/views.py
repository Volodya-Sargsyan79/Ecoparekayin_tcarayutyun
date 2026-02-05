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
            SELECT * FROM person_community
            WHERE person_community.region_id = %s;
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
            WHERE person_villages.community_id = %s;
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

class GetProtectedAreasList(APIView):
    def get(self, request):
    
        id = request.GET.get('id') or ''

        sql = '''
            SELECT * FROM person_protectedareas
            WHERE person_protectedareas.region_id = %s;
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

class GetReserveList(APIView):
    def get(self, request):
    
        id = request.GET.get('id') or ''

        sql = '''
            SELECT * FROM person_reserve
            WHERE person_reserve.protected_areas_id = %s;
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
        community_id = request.data.get('city_id')
        village_id = request.data.get('village_id')  # ✅ fixed
        street = request.data.get('street')
        house = request.data.get('house')
        apartment = request.data.get('apartment')
        phone = request.data.get('phone')
        unknown_person = request.data.get('unknown_person', False)

        sql = '''
            INSERT INTO person_citizen
            (
                name,
                surname,
                region_id,
                community_id,
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
                    community_id,
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
        

class GetLastEmployee(APIView):
    def get(self, request):

        sql = '''
            SELECT id, name, surname 
            FROM person_employee 
            ORDER BY id DESC 
            LIMIT 1;
        '''

        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]  # <-- Get column names
            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]
            
            print(results)

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error using log_error function
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetLastCitizen(APIView):
    def get(self, request):

        sql = '''
            SELECT id, name, surname, unknown_person 
            FROM person_citizen 
            ORDER BY id DESC 
            LIMIT 1;
        '''

        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]  # <-- Get column names
            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]
            
            print(results)

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error using log_error function
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class AddFireCall(APIView):
    def  post(self, request):

        employee_id = request.data.get('employee_id')
        citizen_id = request.data.get('citizen_id')
        start_of_fire = request.data.get('date_of_fire', False)
        date_and_time = request.data.get('start_of_fire', False)
        from_where = request.data.get('from_where')
        the_source_of_the_fire = request.data.get('the_source_of_the_fire')
        registration = request.data.get('registration')
        region_id = request.data.get('region_id')
        regionArmenia_id = request.data.get('region_id')
        protected_areas_id = request.data.get('protected_areas_id')
        community_id = request.data.get('community_id')
        village_id = request.data.get('village_id')
        cordinat = request.data.get('cordinats')
        call_ain = request.data.get('yesCall', False)
        name = request.data.get('name')
        surname = request.data.get('surname')
        call_of_date = request.data.get('call_of_date')
        why_not = request.data.get('why_not')

        sql = '''
            INSERT INTO person_infoaboutfire
            (
                employee_id,
                citizen_id,
                start_of_fire,
                date_and_time,
                from_where,
                the_source_of_the_fire,
                registration,
                region_id,
                regionArmenia_id,
                protected_areas_id,
                community_id,
                village_id,
                cordinat,
                call_ain,
                name,
                surname,
                call_of_date,
                why_not
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, [
                    employee_id,
                    citizen_id,
                    start_of_fire,
                    date_and_time,
                    from_where,
                    the_source_of_the_fire,
                    registration,
                    region_id,
                    regionArmenia_id,
                    protected_areas_id,
                    community_id,
                    village_id,
                    cordinat,
                    call_ain,
                    name,
                    surname,
                    call_of_date,
                    why_not
                ])

            return Response({"message": "Employee caller added successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)