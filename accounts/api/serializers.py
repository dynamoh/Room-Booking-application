from rest_framework import serializers
from accounts.models import User
from rooms.models import Customer,Manager
from rooms.models import Room,TimeSlot,RoomBooked

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email','name','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = User(
                email=self.validated_data['email'],
                name= self.validated_data['name'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match'})

        user.set_password(password)
        user.save()
        Customer.objects.create(customer_id=user)
        return user

class ManagerRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email','name','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = User(
                email=self.validated_data['email'],
                name= self.validated_data['name'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match'})

        user.set_password(password)
        user.manager=True
        user.customer=False
        user.save()
        Manager.objects.create(manager_id=user)
        return user

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_number','room_type','price','prior_booking_days','room_manager','timeslots']

class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['start_time','end_time']
        lookup_field = "room_id"

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooked
        fields = ['customer_booked','room_timeslot_booked','booked_for','booked_on']
        lookup_field = "room_timeslot_booked"
