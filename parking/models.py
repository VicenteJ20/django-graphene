from django.db import models

# Create your models here.
class ParkingSpot(models.Model):
  sensor_id = models.CharField(max_length=100)
  sensor_status = models.BooleanField(default=False)
  sensor_location = models.CharField(max_length=100)
  sensor_type = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.sensor_id