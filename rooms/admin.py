from django.contrib import admin
from .models import Customer,Manager,Room,TimeSlot,RoomBooked,ContactUs
# Register your models here.

admin.site.register(Customer)
admin.site.register(Manager)
admin.site.register(Room)
admin.site.register(RoomBooked)
admin.site.register(TimeSlot)
admin.site.register(ContactUs)
