from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import (ListAPIView,
                                    RetrieveAPIView,
                                    CreateAPIView,
                                    UpdateAPIView,
                                    DestroyAPIView)
from accounts.api.serializers import (CustomerRegistrationSerializer,
                                    ManagerRegistrationSerializer,
                                    RoomSerializer,
                                    TimeslotSerializer,
                                    BookingSerializer,
                                    customerSerializer)
from rooms.models import (Room,
                        TimeSlot,
                        RoomBooked,
                        Customer)

class CustomerListView(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = customerSerializer

class CustomerDetailView(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = customerSerializer

class RoomDetailView(RetrieveAPIView):
    lookup_field = "slug"
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class TimeslotDetailView(ListAPIView):

    lookup_field = "room_id"

    def get_queryset(self):
        print(self.kwargs['room_id'])
        p = self.kwargs['room_id']
        r = Room.objects.filter(slug=p).first()
        print(r)
        t = TimeSlot.objects.all().filter(room_id=r)
        print(t)
        return TimeSlot.objects.all().filter(room_id=r)

    serializer_class = TimeslotSerializer


class BookingDetailView(ListAPIView):

    lookup_field = "room_timeslot_booked"

    def get_queryset(self):
        print(self.kwargs['room_timeslot_booked'])
        p = self.kwargs['room_timeslot_booked']
        r = Room.objects.filter(slug=p).first()
        b = RoomBooked.objects.all().filter(room_timeslot_booked__room_id=r)
        return RoomBooked.objects.all().filter(room_timeslot_booked__room_id=r)

    serializer_class = BookingSerializer


@api_view(['POST',])
def customer_registration_view(request):
    if request.method == 'POST':
        serializer = CustomerRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered a new user.'
            data['email'] = user.email
            data['name'] = user.name

        else:
            data = serializer.errors
        return Response(data)

@api_view(['POST',])
def manager_registration_view(request):
    if request.method == 'POST':
        serializer = ManagerRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered a new user.'
            data['email'] = user.email
            data['name'] = user.name

        else:
            data = serializer.errors
        return Response(data)
