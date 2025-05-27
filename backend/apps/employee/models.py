from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    birthday = models.DateField(null=True, blank=True)
    passport = models.CharField(max_length=15, null=True, blank=True)
    id_card = models.CharField(max_length=15, null=True, blank=True)
    hvhh = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    img = models.ImageField(upload_to='person', null=True, blank=True)

    def __str__(self):
        return f'{self.id} {self.first_name} {self.last_name}'

class DocumentationImage(models.Model):
    person = models.ForeignKey(Person, related_name='documentation_image', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='documentation_image')

class Address(models.Model):
    person = models.ManyToManyField(Person)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house = models.CharField(max_length=20)
    apartment = models.CharField(max_length=20, blank=True, null=True)
    REGISTERED = (
        ("Հ", "Հաշվառման"),
        ("Բ", "Բնակության"),
        ("Ս", "Սեփականություն")
    )
    registration = models.CharField(max_length=1, choices=REGISTERED)

    def __str__(self):
        return f'{self.country}, {self.city}, {self.street}, {self.house}' + (f', {self.apartment}' if self.apartment else '')

class Phone(models.Model):
    person = models.ForeignKey(Person, related_name='phone', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.person} {self.phone }'

class Study(models.Model):
    person = models.ForeignKey(Person, related_name='study', on_delete=models.CASCADE)
    educational_institution = models.CharField(max_length=255)
    facultet = models.CharField(max_length=255)
    profession = models.CharField(max_length=50)
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=4)
    img = models.ImageField(upload_to='documentations')

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

class Property(models.Model):
    person = models.ManyToManyField(Person)
    adress = models.ManyToManyField(Address)

class Car(models.Model):
    person = models.ForeignKey(Person, related_name='car', on_delete=models.CASCADE)
    type = models.CharField(max_length=15)
    model = models.CharField(max_length=10)
    year = models.CharField(max_length=4)
    number = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.type}, {self.model}, {self.year}, {self.number}'

class Informations(models.Model):
    person = models.ForeignKey(Person, related_name='informations', on_delete=models.CASCADE)
    img = models.ManyToManyField(DocumentationImage, null=True, blank=True)
    name = models.CharField(max_length=255)
    about = models.TextField(null=True, blank=True)

class Employees(models.Model):
    person = models.ForeignKey(Person, related_name='employees', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    position_start = models.CharField(max_length=255)
    data_of_start = models.DateField(null=True, blank=True)
    end_of_start = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.name} {self.position_start}`  {self.person}'

class Relatives(models.Model):
    name = models.CharField(max_length=15)
    person = models.ForeignKey(Person, related_name='relatives', on_delete=models.CASCADE)
    employee =  models.ForeignKey(Employees, related_name='relatives', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.employee} - {self.name} - {self.person}'

class VictimsAwards(models.Model):
    person = models.ManyToManyField(Employees)
    name = models.CharField(max_length=100)
    data_of_victims_or_awards = models.DateField(null=True, blank=True)

class OfficialProperty(models.Model):
    person = models.ForeignKey(Employees, related_name='official_property', on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    number = models.CharField(max_length=20)