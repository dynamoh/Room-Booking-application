from django.db import models
from accounts.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify
# Create your models here.
#
class Customer(models.Model):
    customer_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Customer")
    contact = models.CharField(max_length=12)
    address = models.CharField(max_length=300,blank=True,null=True)
    city = models.CharField(max_length=300,blank=True,null=True)
    profession = models.CharField(max_length=200,blank=True,null=True)
    profile_pic = models.ImageField(upload_to='customer/')

    def __str__(self):
        return self.customer_id.name

class Manager(models.Model):
    manager_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Manager")
    contact = models.CharField(max_length=12)
    address = models.CharField(max_length=300,blank=True,null=True)
    city = models.CharField(max_length=300,blank=True,null=True)
    profile_pic = models.ImageField(upload_to='manager/')

    def __str__(self):
        return self.manager_id.name

class Room(models.Model):
    room_manager = models.ForeignKey(Manager,on_delete=models.CASCADE)
    room_number = models.CharField(max_length=30)
    room_pic = models.ImageField(upload_to = 'room/')
    prior_booking_days = models.IntegerField()
    slug = models.SlugField(null=True,blank=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.room_number)
        super(Room,self).save(*args,**kwargs)

    def __str__(self):
        return self.room_number

class TimeSlot(models.Model):
    room_id = models.ForeignKey(Room,on_delete=models.CASCADE)
    start_time = models.CharField(max_length=10,default="")
    end_time = models.CharField(max_length=10,default="")

    def __str__(self):
        return self.room_id.room_number

class RoomBooked(models.Model):
    customer_booked = models.ForeignKey(Customer,on_delete=models.CASCADE)
    room_timeslot_booked = models.ForeignKey(TimeSlot,on_delete=models.CASCADE)
    booked_for = models.DateField()
    booked_on = models.DateTimeField(default=timezone.now)
