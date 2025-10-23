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