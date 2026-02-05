from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.name}'


class RegionArmenia(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.name}'


class Precinct(models.Model):
    region = models.ForeignKey(Region, related_name='precinct', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Community(models.Model):
    region = models.ForeignKey(RegionArmenia, related_name='ցommunity', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.region} {self.name}'


class ProtectedAreas(models.Model):
    region = models.ForeignKey(Region, related_name='protectedareas', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.region} {self.name}'


class Reserve(models.Model):
    protected_areas = models.ForeignKey(ProtectedAreas, related_name='reserve', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.protected_areas} {self.name}'    


class Villages(models.Model):
    community = models.ForeignKey(Community, related_name='villages', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.community} {self.name}'
    

class Position(models.Model):
    position_held = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.position_held}'


class StartCallDate(models.Model):
    start_of_call = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.start_of_call}'


class Employee(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    region = models.ForeignKey(Region, related_name='employee', on_delete=models.CASCADE)
    precinct = models.ForeignKey(Precinct, related_name='employee', on_delete=models.CASCADE, null=True, blank=True)
    position = models.ForeignKey(Position, related_name='employee', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20) 

    def __str__(self):
        return f'{self.name} {self.surname} {self.phone}'


class Citizen(models.Model):
    unknown_person = models.BooleanField(default=False)
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    region = models.ForeignKey(RegionArmenia, related_name='citizen', on_delete=models.CASCADE, null=True, blank=True)
    community = models.ForeignKey(Community, related_name='citizen', on_delete=models.CASCADE, null=True, blank=True)
    village = models.ForeignKey(Villages, related_name='citizen', on_delete=models.CASCADE, null=True, blank=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    house = models.CharField(max_length=20, blank=True, null=True)
    apartment = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.surname} {self.phone}'
    
    
class InfoAboutFire(models.Model):
    employee = models.ForeignKey(Employee, related_name='infoaboutfire', on_delete=models.CASCADE, null=True, blank=True)
    citizen = models.ForeignKey(Citizen, related_name='infoaboutfire', on_delete=models.CASCADE, null=True, blank=True)
    start_of_fire = models.BooleanField(default=False)
    date_and_time = models.DateTimeField(null=True, blank=True)
    from_where = models.CharField(max_length=100, null=True, blank=True)
    the_source_of_the_fire = models.CharField(max_length=250, null=True, blank=True)
    REGISTERED = (
        ("Պ", "Պետական պահպանվող տարածք"),
        ("Հ", "Համայնքային տարածք")
    )
    registration = models.CharField(max_length=1, choices=REGISTERED)
    region = models.ForeignKey(Region, related_name='infoaboutfire', on_delete=models.CASCADE, null=True, blank=True)
    regionArmenia = models.ForeignKey(RegionArmenia, related_name='infoaboutfire', on_delete=models.CASCADE, null=True, blank=True)
    protected_areas = models.ForeignKey(ProtectedAreas, related_name='infoaboutfire', on_delete=models.CASCADE, null=True, blank=True)
    community = models.ForeignKey(Community, related_name='infoaboutfire', on_delete=models.CASCADE, null=True, blank=True)
    reserve = models.ForeignKey(Reserve, related_name='reserve', on_delete=models.CASCADE, null=True, blank=True)
    village = models.ForeignKey(Villages, related_name='infoaboutfire', on_delete=models.CASCADE, null=True, blank=True)
    cordinat = models.CharField(max_length=250, null=True, blank=True)
    call_ain = models.BooleanField(default=False)
    name = models.CharField(max_length=50, null=True, blank=True)
    seurname = models.CharField(max_length=50, null=True, blank=True)
    call_of_date = models.DateTimeField(null=True, blank=True)
    why_not = models.CharField(max_length=250, null=True, blank=True)


class OperationalControlCenter(models.Model):
    infoaboutfire = models.ForeignKey(InfoAboutFire, related_name='operationalcontrolcenter', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    start_of_call = models.ForeignKey(StartCallDate, related_name='operationalcontrolcenter', on_delete=models.CASCADE)
    call_ain = models.DateTimeField(null=True, blank=True)
    ain_name = models.CharField(max_length=100, null=True, blank=True)
    call_region = models.DateTimeField(null=True, blank=True)
    region_name = models.CharField(max_length=100, null=True, blank=True)
    head_of_the_occ = models.DateTimeField(null=True, blank=True)
    head_of_the_occ_name = models.CharField(max_length=100, null=True, blank=True)
    

class EndFire(models.Model):
    infoaboutfire = models.ForeignKey(OperationalControlCenter, related_name='endfire', on_delete=models.CASCADE)
    end_of_fire = models.DateTimeField(null=True, blank=True)
    forest_place_burnt = models.CharField(max_length=4, null=True, blank=True)
    field_place_burnt = models.CharField(max_length=4, null=True, blank=True)
    burnt_trees = models.CharField(max_length=3, null=True, blank=True)
    burnt_animals = models.CharField(max_length=2, null=True, blank=True)
    eps = models.CharField(max_length=250, null=True, blank=True)
    ain = models.CharField(max_length=250, null=True, blank=True)


