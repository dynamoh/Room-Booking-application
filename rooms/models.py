from django.db import models
from accounts.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify
# Create your models here.

class Constants:
    ROOMTYPES = {
            ('Single Room','Single Room'),
            ('Family Room','Family Room'),
            ('Delux Suite','Delux Suite'),
    }

class Customer(models.Model):
    customer_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Customer")
    contact = models.CharField(max_length=12,blank=True,null=True)
    address = models.CharField(max_length=300,blank=True,null=True)
    city = models.CharField(max_length=300,blank=True,null=True)
    profession = models.CharField(max_length=200,blank=True,null=True)
    profile_pic = models.ImageField(upload_to='customer/',blank=True,null=True)

    def __str__(self):
        return self.customer_id.name

class Manager(models.Model):
    manager_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Manager")
    contact = models.CharField(max_length=12,blank=True,null=True)
    address = models.CharField(max_length=300,blank=True,null=True)
    city = models.CharField(max_length=300,blank=True,null=True)
    profile_pic = models.ImageField(upload_to='manager/',blank=True,null=True)

    def __str__(self):
        return self.manager_id.name

class Room(models.Model):
    room_manager = models.ForeignKey(Manager,on_delete=models.CASCADE)
    room_number = models.CharField(max_length=30,unique=True)
    room_pic = models.ImageField(upload_to = 'room/')
    room_type = models.CharField(max_length=100,choices= Constants.ROOMTYPES,default='Single Room')
    prior_booking_days = models.IntegerField()
    price = models.IntegerField(default=1000)
    slug = models.SlugField(null=True,blank=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.room_number)
        super(Room,self).save(*args,**kwargs)

    def __str__(self):
        return self.room_number

class TimeSlot(models.Model):
    room_id = models.ForeignKey(Room,on_delete=models.CASCADE,related_name="timeslots")
    start_time = models.CharField(max_length=10,default="")
    end_time = models.CharField(max_length=10,default="")

    class Meta:
        unique_together = ('room_id','start_time','end_time')

    def __str__(self):
        return self.room_id.room_number

class RoomBooked(models.Model):
    customer_booked = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="customerBooked")
    room_timeslot_booked = models.ForeignKey(TimeSlot,on_delete=models.CASCADE,related_name="timeslotBooked")
    booked_for = models.DateField()
    booked_on = models.DateTimeField(default=timezone.now)

class ContactUs(models.Model):
    full_name = models.CharField(max_length=600)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    message = models.TextField()

    def __str__(self):
        return self.full_name
