from django.urls import path
from .views import (
    GetPersonList,
    GetPersonPhoneList,
    GetPersonAddressList,
    GetPersonCarList,
    GetPersonRelativesList,
    GetPersonStudyList,
    GetPersonSoldierList,
    GetPersonWorkList
)
    

urlpatterns = [
    path('person/', GetPersonList.as_view()),
    path('person/phone/', GetPersonPhoneList.as_view()),
    path('person/address/', GetPersonAddressList.as_view()),
    path('person/car/', GetPersonCarList.as_view()),
    path('person/relatives/', GetPersonRelativesList.as_view()),
    path('person/study/', GetPersonStudyList.as_view()),
    path('person/soldier/', GetPersonSoldierList.as_view()),
    path('person/work/', GetPersonWorkList.as_view())
]


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

        id = request.GET.get('id') or ''

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

        id = request.GET.get('id') or ''

        sql = '''
            SELECT 
                country, 
                city, 
                street, 
                house, 
                apartment, 
                registration 
            FROM 
                person_address
            where person_id = %s;
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

class GetPersonCarList(APIView):
    def get(self, request):

        id = request.GET.get('id') or ''

        sql = '''
            SELECT 
                type, 
                model, 
                year, 
                number 
            FROM 
                person_car 
            WHERE 
                person_id = %s
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
        

class GetPersonStudyList(APIView):
    def get(self, request):
    
        id = request.GET.get('id') or ''

        sql = '''
            SELECT 
                place, 
                educational_institution, 
                facultet, 
                profession, 
                start_year, 
                end_year, 
                img 
            FROM 
                person_study 
            WHERE 
                person_id=%s;
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
        
class GetPersonSoldierList(APIView):
    def get(self, request):
    
        id = request.GET.get('id') or ''

        sql = '''
            SELECT 
                person_soldier.where, 
                from_year, 
                to_year 
            FROM 
                person_soldier
            WHERE 
                person_id=%s;
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
        
        from django.db import models

# Create your models here.
class Person(models.Model):
    img = models.ImageField(upload_to='person', null=True, blank=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    birthday = models.DateField(null=True, blank=True)
    passport = models.CharField(max_length=15, null=True, blank=True)
    id_card = models.CharField(max_length=15, null=True, blank=True)
    hvhh = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self):
        return f'{self.id} {self.first_name} {self.last_name}'
    

class Phone(models.Model):
    person = models.ForeignKey(Person, related_name='phone', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    home = models.BooleanField(default=False)
    mobile = models.BooleanField(default=False)
    viber = models.BooleanField(default=False)
    whatsUp = models.BooleanField(default=False)
    telegram = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.person} {self.phone }'
    

class Car(models.Model):
    person = models.ForeignKey(Person, related_name='car', on_delete=models.CASCADE)
    type = models.CharField(max_length=15)
    model = models.CharField(max_length=10)
    year = models.CharField(max_length=4)
    number = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.person}, {self.type}, {self.model}, {self.year}, {self.number}'
    

class Address(models.Model):
    person = models.ForeignKey(Person, related_name='address', on_delete=models.CASCADE)
    REGISTERED = (
        ("Հաշվառման հասցե", "Հաշվառման"),
        ("Բնակության հասցե", "Բնակության"),
        ("Սեփականություն", "Սեփականություն")
    )
    registration = models.CharField(max_length=20, choices=REGISTERED)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house = models.CharField(max_length=20)
    apartment = models.CharField(max_length=20, blank=True, null=True)
    img = models.ImageField(upload_to='person_documentation', null=True, blank=True)

    def __str__(self):
        return f'{self.country}, {self.city}, {self.street}, {self.house}' + (f', {self.apartment}' if self.apartment else '')


class Study(models.Model):
    person = models.ForeignKey(Person, related_name='study', on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    educational_institution = models.CharField(max_length=255)
    facultet = models.CharField(max_length=255)
    profession = models.CharField(max_length=50)
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=4)
    img = models.ImageField(upload_to='person_study', null=True, blank=True)

    def __str__(self):
        return f'{self.person}, {self.educational_institution}, {self.facultet}'

class Soldier(models.Model):
    person = models.ForeignKey(Person, related_name='soldier', on_delete=models.CASCADE)
    where = models.CharField(max_length=255)
    from_year = models.CharField(max_length=4)
    to_year = models.CharField(max_length=4)

    def __str__(self):
        return f'{self.person}'
    
class Conviction(models.Model):
    person = models.ForeignKey(Person, related_name='conviction', on_delete=models.CASCADE)
    name_article = models.CharField(max_length=255)
    from_year = models.CharField(max_length=4)
    to_year = models.CharField(max_length=4)

class PersonDocumentationImage(models.Model):
    person = models.ForeignKey(Person, related_name='person_documentation', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='person_documentation')

class Relatives(models.Model):
    pal_name = models.CharField(max_length=15)
    person = models.ForeignKey(Person, related_name='relatives_1', on_delete=models.CASCADE)
    relatives = models.ForeignKey(Person, related_name='relatives_2', on_delete=models.CASCADE)
    REGISTERED = (
        ("Հ", "Հարազատներ"),
        ("Բ", "Բարեկամներ"),
        ("Ը", "Ընկերներ"),
        ("Կ", "Կապեր")
    )
    registration = models.CharField(max_length=1, choices=REGISTERED)

    def __str__(self):
        return f'{self.relatives} - {self.pal_name} - {self.person}'
    

class Informations(models.Model):
    person = models.ForeignKey(Person, related_name='informations', on_delete=models.CASCADE)
    sex = models.CharField(max_length=255, null=True, blank=True)
    politics = models.CharField(max_length=255, null=True, blank=True)
    religion = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.person}'

class Employees(models.Model):
    employee = models.ForeignKey(Person, related_name='employee', on_delete=models.CASCADE)
    plase_name = models.CharField(max_length=255)
    position_start = models.CharField(max_length=255)
    data_of_start = models.DateField(null=True, blank=True)
    end_of_start = models.DateField(null=True, blank=True)
    degree = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f'{self.plase_name} {self.position_start}`  {self.employee}'


class VictimsAwards(models.Model):
    employee = models.ForeignKey(Employees, related_name='victims_awards', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    data_of_victims_or_awards = models.DateField(null=True, blank=True)
    

class OfficialProperty(models.Model):
    employee = models.ForeignKey(Employees, related_name='official_property', on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    number = models.CharField(max_length=20)


        REGISTERED = (
        ("Սյունիք", "ՀՀ Սյունիքի մարզային վարչություն"),
        ("Կոտայք և Գեղարքունիք", "ՀՀ Կոտայքի և Գեղարքունիքի մարզային վարչություն"),
        ("Տավուշ", "ՀՀ Տավուշի մարզային վարչություն"),
        ("Լոռի", "ՀՀ Լոռու մարզային վարչություն"),
        ("Վայոց ձոր և Արարատ", "ՀՀ Վայոց ձորի և Արարատի մարզային վարչություն"),
        ("Շիրակ և Արագածոտն", "ՀՀ Շիրակի և Արագածոտնի մարզային վարչություն"),
        ("Երևան և Արմավիր", "Երևան քաղաքի և ՀՀ Արմավիրի մարզային վարչություն")
    )