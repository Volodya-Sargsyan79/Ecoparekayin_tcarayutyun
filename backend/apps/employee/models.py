from django.db import models

# Create your models here.
class Employees(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    birthday = models.DateField(null=True, blank=True)
    passport = models.CharField(max_length=15)
    id_card = models.CharField(max_length=15)
    hvhh = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=30)
    img = models.ImageField(upload_to='person')

    def __str__(self):
        return f'{self.name} {self.surname}'

class Address(models.Model):
    employee = models.ManyToManyField(Employees)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    house = models.CharField(max_length=10)
    apartment = models.CharField(max_length=10, blank=True, null=True)

class Property(models.Model):
    employee = models.ManyToManyField(Employees)
    adress = models.ManyToManyField(Address)

class Car(models.Model):
    employee = models.ForeignKey(Employees, related_name='car', on_delete=models.CASCADE)
    type = models.CharField(max_length=15)
    model = models.CharField(max_length=10)
    year = models.CharField(max_length=4)
    number = models.CharField(max_length=10)

class Study(models.Model):
    employee = models.ForeignKey(Employees, related_name='study', on_delete=models.CASCADE)
    educational_institution = models.CharField(max_length=255)
    facultet = models.CharField(max_length=255)
    profession = models.CharField(max_length=50)
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=4)
    img = models.ImageField(upload_to='documentations')

class DocumentationImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='documentations')

class VictimsAwards(models.Model):
    employee = models.ManyToManyField(Employees)
    name = models.CharField(max_length=100)
    data_of_victims_or_awards = models.DateField(null=True, blank=True)

class StartKariera(models.Model):
    employee = models.ForeignKey(Employees, related_name='start_kariera', on_delete=models.CASCADE)
    position_start = models.CharField(max_length=255)
    data_of_start = models.DateField(null=True, blank=True)
    position_end = models.CharField(max_length=255, null=True, blank=True)
    end_of_start = models.DateField(null=True, blank=True)
    img = models.ManyToManyField(DocumentationImage)

class OfficialProperty(models.Model):
    employee = models.ForeignKey(Employees, related_name='official_property', on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    number = models.CharField(max_length=20)

class Informations(models.Model):
    employee = models.ForeignKey(Employees, related_name='informations', on_delete=models.CASCADE)
    img = models.ManyToManyField(DocumentationImage)
    name = models.CharField(max_length=255)
    about = models.TextField()
    

class Phone(models.Model):
    employee = models.ForeignKey(Employees, related_name='phone', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.phone