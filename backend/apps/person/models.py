from io import BytesIO
from django.core.files import File
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.conf import settings
from PIL import Image
import zipfile
import uuid
import os

# Create your models here.

class Region(models.Model):
    region = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.region}'


class Precinct(models.Model):
    region = models.ForeignKey(Region, related_name='precinct', on_delete=models.CASCADE)
    precinct = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.precinct}'


class Position(models.Model):
    position_held = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.position_held}'


class Car(models.Model):
    car_number = models.CharField(max_length=7)
    board_number = models.IntegerField()
    deviceId = models.IntegerField(unique=True, null=True, blank=True)
    region = models.ForeignKey(Region, related_name='car', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.car_number} {self.board_number}'

def extract_kml(kmz_path, extract_to):
    with zipfile.ZipFile(kmz_path, 'r') as z:
        z.extractall(extract_to)
    
class Route(models.Model):
    registration_day = models.DateField(auto_now_add=True)
    region = models.ForeignKey(Region, related_name='route', on_delete=models.CASCADE)
    precinct = models.ForeignKey(Precinct, related_name='route', on_delete=models.CASCADE)
    route_number = models.CharField(max_length=15)
    route_length = models.IntegerField()
    image = models.ImageField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='map/', null=True, blank=True)
    kmz_file = models.FileField(upload_to='kmz/', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='route', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.image: 
            self.thumbnail = self.make_thumbnail(self.image)
        super().save(*args, **kwargs)
    
        if self.kmz_file:
            extract_path = os.path.join(settings.MEDIA_ROOT, "kml", str(self.id))
            os.makedirs(extract_path, exist_ok=True)

            with zipfile.ZipFile(self.kmz_file.path, 'r') as z:
                z.extractall(extract_path)

            kml_file = None

            for root, dirs, files in os.walk(extract_path):
                for file in files:
                    if file.endswith('.kml'):
                        kml_file = os.path.join(root, file)
                        break

            if kml_file:
                final_path = os.path.join(extract_path, "doc.kml")
                os.replace(kml_file, final_path)

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img = img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    
    def __str__(self):
        return f'{self.registration_day} {self.precinct} {self.route_number} երթուղի'
   

class Employee(models.Model):
    name = models.CharField(max_length=50, verbose_name="Անուն")
    surname = models.CharField(max_length=50, verbose_name="Ազգանուն")
    region = models.ForeignKey(Region, related_name='employee', on_delete=models.CASCADE, verbose_name="Վարչություն")
    precinct = models.ForeignKey(Precinct, related_name='employee', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Տեղամաս")
    position = models.ForeignKey(Position, related_name='employee', on_delete=models.CASCADE, verbose_name="Պաշտոն")
    phone = models.CharField(max_length=9, null=True, blank=True, verbose_name="Հեռ.")
    camera = models.IntegerField(unique=True, verbose_name="Տեսախցիկ")
    image = models.ImageField(upload_to='person/', null=True, blank=True, verbose_name="Նկար")
    birth_day = models.DateField(null=True, blank=True, verbose_name="Ծննդյան ամսաթիվ")
    order_day = models.DateField(null=True, blank=True, verbose_name="Հրամանի ամսաթիվ")
    residential_address = models.CharField(max_length=250, null=True, blank=True, verbose_name="Բնակության հասցե")
    service_number = models.CharField(max_length=5, null=True, blank=True, verbose_name="Ծառայողական համար")
    passport = models.CharField(max_length=10, null=True, blank=True, verbose_name="Անձնագիր")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='employee', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.image:
            self.image = self.make_thumbnail(self.image)
        super().save(*args, **kwargs)

    def make_thumbnail(self, image, size=(300, 400)):
        img = Image.open(image)
        img = img.convert('RGB')
        img = img.resize(size) 

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        image = File(thumb_io, name=image.name)

        return image

    def __str__(self):
        return f'{self.camera} {self.position} {self.name} {self.surname} {self.phone}'
    

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'pdf/{uuid.uuid4()}.{ext}'   # 🔥 unique անուն


class StationShift(models.Model):
    start_shift = models.DateTimeField(verbose_name="Հերթափոխի սկիզբ")
    end_shift = models.DateTimeField(verbose_name="Հերթափոխի ավարտ")

    region = models.ForeignKey('Region', related_name='stationshift', on_delete=models.CASCADE, verbose_name="Մարզ")
    precinct = models.ForeignKey('Precinct', related_name='stationshift', on_delete=models.CASCADE, verbose_name="Տեղամաս")

    employee_01 = models.ForeignKey('Employee', related_name='stationshift', on_delete=models.CASCADE, verbose_name="Հերթափոխ 1")
    employee_02 = models.ForeignKey('Employee', related_name='stationshift_02', on_delete=models.CASCADE, verbose_name="Հերթափոխ 2")
    employee_03 = models.ForeignKey('Employee', related_name='stationshift_03', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Հերթափոխ 3")
    employee_04 = models.ForeignKey('Employee', related_name='stationshift_04', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Հերթափոխ 4")

    car = models.ForeignKey('Car', related_name='stationshift', on_delete=models.CASCADE, verbose_name="Ծառայողական մեքենան")
    route = models.ForeignKey('Route', related_name='stationshift', on_delete=models.CASCADE, verbose_name="Երթուղի")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='stationshift', on_delete=models.CASCADE, verbose_name="Գրանցող օգտատեր")

    def __str__(self):
        return f'{self.start_shift} {self.end_shift} {self.car} {self.route}'


class InformationForShift(models.Model):
    text_info = models.TextField(null=True, blank=True, verbose_name="Հերթափոխի վերաբերյալ տեղեկություն")
    pdf_file = models.FileField(upload_to='pdf/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True, blank=True, verbose_name="Հերթափոխի վերաբերյալ զեկուցագիր")
    shift = models.ForeignKey('StationShift', related_name='informationforshift', on_delete=models.CASCADE, verbose_name="Հերթափոխ")


class UserAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    precinct = models.ForeignKey(Precinct, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'
    
class LunchTime(models.Model):
    start_lanch = models.TimeField(null=True, blank=True)
    end_lanch = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    shift = models.ForeignKey('StationShift', related_name='lunchtime', on_delete=models.CASCADE, verbose_name="Հերթափոխ")
    



