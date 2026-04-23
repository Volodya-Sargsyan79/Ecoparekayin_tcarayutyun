from django.db import models

# Create your models here.


class CallRecord(models.Model):
    call_id = models.CharField(max_length=100, unique=True)
    caller_number = models.CharField(max_length=20)
    called_number = models.CharField(max_length=20)
    call_start = models.DateTimeField(auto_now_add=True)
    call_duration = models.IntegerField(default=0, help_text="Վայրկյաններով")
    recording_url = models.URLField(blank=True, null=True)
    recording_file = models.FileField(upload_to='recordings/', blank=True, null=True)
    status = models.CharField(max_length=50, default='initiated')
    shift = models.ForeignKey('person.StationShift', related_name='call_records', on_delete=models.CASCADE, verbose_name="Հերթափոխ")
    
    class Meta:
        ordering = ['-call_start']
    
    def __str__(self):
        return f"{self.caller_number} → {self.called_number} ({self.call_start})"