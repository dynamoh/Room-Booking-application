from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import (ListAPIView,
                                    RetrieveAPIView,
                                    CreateAPIView,
                                    UpdateAPIView,
                                    DestroyAPIView)
from accounts.api.serializers import CustomerRegistrationSerializer,ManagerRegistrationSerializer,RoomSerializer
from rooms.models import Room


class RoomDetailView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


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
