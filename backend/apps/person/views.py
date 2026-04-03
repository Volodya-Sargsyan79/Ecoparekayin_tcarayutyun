
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.db import connection
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import os
import uuid
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from .models import Route


class GetRegionList(APIView):
    def get(self, request):

        try:
            cursor = connection.cursor()

            if request.user.id == 1:
                sql = '''
                    SELECT * FROM person_region;
                '''
                cursor.execute(sql)

            else:
                sql = '''
                    SELECT person_region.id, person_region.region 
                    FROM ekopatrol.person_useraccess 
                    JOIN person_region 
                    ON person_useraccess.region_id = person_region.id 
                    LIMIT 1;
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
    permission_classes = [IsAuthenticated]
    def get(self, request):
    
        id = request.GET.get('id') or ''

        try:
            cursor = connection.cursor()

            if request.user.id == 1:
                sql = '''
                    SELECT * FROM person_precinct
                    WHERE person_precinct.region_id = %s;
                '''
                cursor.execute(sql, [id])

            else:
                sql = '''
                    SELECT person_precinct.id, person_precinct.precinct 
                    FROM ekopatrol.person_useraccess 
                    JOIN person_precinct 
                    ON person_useraccess.precinct_id = person_precinct.id 
                    WHERE person_useraccess.user_id = %s;
                '''
                cursor.execute(sql, [request.user.id])

            columns = [col[0] for col in cursor.description]

            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
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


class AddEmployee(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        name = request.data.get('name')
        surname = request.data.get('surname')
        phone = request.data.get('phone')
        camera = request.data.get('camera')
        position_id = request.data.get('position_id')
        precinct_id = request.data.get('precinct_id')
        region_id = request.data.get('region_id')
        created_by_id = request.user.id

        sql = '''
            INSERT INTO person_employee 
            (name, surname, phone, camera, position_id, precinct_id, region_id, created_by_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, [
                    name,
                    surname,
                    phone,
                    camera,
                    position_id,
                    precinct_id,
                    region_id,
                    created_by_id
                ])

            return Response({"message": "Employee caller added successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetLastEmployee(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        id = request.GET.get('id') or ''
        
        try:
            cursor = connection.cursor()

            sql = '''
                SELECT person_employee.id, name, surname, camera, phone 
                FROM person_employee 
                LEFT JOIN person_useraccess 
                ON person_employee.precinct_id = person_useraccess.precinct_id
                WHERE person_employee.precinct_id = %s
                AND person_useraccess.user_id = %s;
            '''
            cursor.execute(sql, [id, request.user.id])

            columns = [col[0] for col in cursor.description]

            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetEmployee(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        
        # id = request.GET.get('id') or ''
        
        try:
            cursor = connection.cursor()

            sql = '''
                SELECT * FROM ekopatrol.person_employee 
                JOIN person_region ON person_employee.region_id = person_region.id 
                JOIN person_precinct ON person_employee.precinct_id = person_precinct.id
                JOIN person_position ON person_employee.position_id = person_position.id 
                WHERE person_employee.id = %s;
            '''
            cursor.execute(sql, [pk])

            columns = [col[0] for col in cursor.description]

            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetLastCar(APIView):
    def get(self, request):
        
        id = request.GET.get('id') or ''
        
        sql = '''
            SELECT *
            FROM person_car
            WHERE person_car.region_id = %s;
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


class GetLastRoute(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.GET.get('id') or ''

        try:
            cursor = connection.cursor()

            sql = '''
                SELECT person_route.id, route_number, route_length, thumbnail
                FROM person_route 
                LEFT JOIN person_useraccess 
                ON person_route.precinct_id = person_useraccess.precinct_id
                WHERE person_route.precinct_id = %s
                AND person_useraccess.user_id = %s;
            '''
            cursor.execute(sql, [id, request.user.id])

            columns = [col[0] for col in cursor.description]

            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetRouteMap(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):  # ✅ accept pk from URL
        try:
            cursor = connection.cursor()

            sql = '''
                SELECT person_route.id, route_number, route_length, image, kmz_file, region, precinct
                FROM person_route
                JOIN person_region ON person_route.region_id = person_region.id
                JOIN person_precinct ON person_route.precinct_id = person_precinct.id
                WHERE person_route.id = %s;
            '''
            cursor.execute(sql, [pk])  
            columns = [col[0] for col in cursor.description]

            row = cursor.fetchone() 

            if not row:
                return Response({'error': 'Route not found'}, status=status.HTTP_404_NOT_FOUND)

            result = dict(zip(columns, row))

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# def route_detail(request, pk):
#     try:
#         route = Route.objects.get(pk=pk)

#         data = {
#             "id": route.id,
#             "route_number": route.route_number,
#             "route_length": route.route_length,
#             "thumbnail": route.thumbnail.url if route.thumbnail else None,
#             "kmz_file": route.kmz_file.url if route.kmz_file else None,
#         }

#         return JsonResponse(data)

#     except Route.DoesNotExist:
#         return JsonResponse({"error": "Not found"}, status=404)


class GetStationShiftList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.GET.get('id') or ''

        try:
            cursor = connection.cursor()
            sql = '''
                SELECT person_stationshift.id, start_shift, end_shift, precinct, car_number, board_number, route_number, route_length, thumbnail 
                FROM ekopatrol.person_stationshift 
                JOIN person_precinct ON person_stationshift.precinct_id = person_precinct.id 
                JOIN person_car ON person_stationshift.car_id = person_car.id
                JOIN person_route ON person_stationshift.route_id = person_route.id
                LEFT JOIN person_useraccess 
                    ON person_stationshift.precinct_id = person_useraccess.precinct_id
                WHERE person_precinct.id = %s
                AND person_useraccess.user_id = %s
                AND DATE(person_stationshift.start_shift) = CURRENT_DATE;
            '''
            cursor.execute(sql, [id, request.user.id])

            columns = [col[0] for col in cursor.description]

            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetStationShift(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            cursor = connection.cursor()
            sql = '''
                SELECT 
                    person_stationshift.id, person_stationshift.start_shift, person_stationshift.end_shift, person_stationshift.route_id,
                    person_car.deviceId, person_car.car_number, person_car.board_number,
                    person_route.route_number, person_route.route_length, person_route.kmz_file,
                    person_region.region,
                    person_precinct.precinct,

                    -- Employee 1
                    e1.name AS employee_01_name, e1.surname AS employee_01_surname, 
                    e1.phone AS employee_01_phone, e1.camera AS employee_01_camera, 
                    p1.position_held AS employee_01_position_held,

                    -- Employee 2
                    e2.name AS employee_02_name, e2.surname AS employee_02_surname, 
                    e2.phone AS employee_02_phone, e2.camera AS employee_02_camera, 
                    p2.position_held AS employee_02_position_held,

                    -- Employee 3
                    e3.name AS employee_03_name, e3.surname AS employee_03_surname, 
                    e3.phone AS employee_03_phone, e3.camera AS employee_03_camera, 
                    p3.position_held AS employee_03_position_held,

                    -- Employee 4
                    e4.name AS employee_04_name, e4.surname AS employee_04_surname, 
                    e4.phone AS employee_04_phone, e4.camera AS employee_04_camera, 
                    p4.position_held AS employee_04_position_held

                FROM ekopatrol.person_stationshift

                JOIN person_car ON person_stationshift.car_id = person_car.id
                JOIN person_region ON person_stationshift.region_id = person_region.id
                JOIN person_precinct ON person_stationshift.precinct_id = person_precinct.id
                JOIN person_route ON person_stationshift.route_id = person_route.id

                LEFT JOIN person_employee e1 ON person_stationshift.employee_01_id = e1.id
                LEFT JOIN person_employee e2 ON person_stationshift.employee_02_id = e2.id
                LEFT JOIN person_employee e3 ON person_stationshift.employee_03_id = e3.id
                LEFT JOIN person_employee e4 ON person_stationshift.employee_04_id = e4.id

                -- Join position table 4 times using aliases p1, p2, p3, p4
                LEFT JOIN person_position p1 ON e1.position_id = p1.id
                LEFT JOIN person_position p2 ON e2.position_id = p2.id
                LEFT JOIN person_position p3 ON e3.position_id = p3.id
                LEFT JOIN person_position p4 ON e4.position_id = p4.id
                WHERE person_stationshift.id = %s;
            '''
            cursor.execute(sql, [pk])

            columns = [col[0] for col in cursor.description]

            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AddStationShift(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        start_shift = request.data.get('start_shift')
        end_shift = request.data.get('end_shift')
        car_id = request.data.get('car_id')
        created_by_id = request.user.id
        employee_01_id = request.data.get('employee_01_id')
        employee_02_id = request.data.get('employee_02_id')
        employee_03_id = request.data.get('employee_03_id') or None
        employee_04_id = request.data.get('employee_04_id') or None
        region_id = request.data.get('region_id')
        precinct_id = request.data.get('precinct_id')
        route_id = request.data.get('route_id')

        try:
            with connection.cursor() as cursor:
                # Ստուգում ենք կա՞ արդեն նույն start_shift և car_id-ով
                cursor.execute('''
                    SELECT COUNT(*) FROM person_stationshift
                    WHERE start_shift = %s AND car_id = %s
                ''', [start_shift, car_id])

                exists = cursor.fetchone()[0]

                if exists:
                    return Response(
                        {"error": "Այս start_shift և car_id-ով գրառում արդեն գոյություն ունի"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Եթե չկա — գրանցում ենք
                cursor.execute('''
                    INSERT INTO person_stationshift 
                    (
                        start_shift, 
                        end_shift, 
                        employee_01_id, 
                        employee_02_id, 
                        employee_03_id, 
                        employee_04_id, 
                        region_id, 
                        precinct_id, 
                        car_id,
                        route_id, 
                        created_by_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', [
                    start_shift,
                    end_shift,
                    employee_01_id,
                    employee_02_id,
                    employee_03_id,
                    employee_04_id,
                    region_id,
                    precinct_id,
                    car_id,
                    route_id,
                    created_by_id
                ])

            return Response({"message": "Employee caller added successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


def create_thumbnail(image, thumb_name):
    img = Image.open(image)
    img = img.convert('RGB')
    img.thumbnail((300, 200))

    thumb_io = BytesIO()
    img.save(thumb_io, 'JPEG', quality=85)

    thumb_path = default_storage.save(
        f'map/{thumb_name}',
        ContentFile(thumb_io.getvalue())
    )

    return thumb_path

class AddRoute(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 🔹 form data
            region_id = int(request.data.get('region_id'))
            precinct_id = int(request.data.get('precinct_id'))
            route_number = request.data.get('route_number')
            route_length = int(request.data.get('route_length'))

            image = request.FILES.get('image')

            file_path = None
            thumbnail_path = None

            if image:
                name, ext = os.path.splitext(image.name)
                unique_id = uuid.uuid4().hex[:6]
                file_name = f"{name}-{unique_id}{ext}"
                file_path = default_storage.save(f'{file_name}', image)
                image.seek(0)
                thumb_name = f"{name}-{unique_id}_thumb.jpg"
                thumbnail_path = create_thumbnail(image, thumb_name)

            sql = '''
                INSERT INTO person_route 
                (region_id, precinct_id, route_number, route_length, image, thumbnail)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''

            with connection.cursor() as cursor:
                cursor.execute(sql, [
                    region_id,
                    precinct_id,
                    route_number,
                    route_length,
                    file_path,
                    thumbnail_path
                ])

            return Response({
                "message": "Route created",
                "image": file_path,
                "thumbnail": thumbnail_path
            }, status=201)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)

        


