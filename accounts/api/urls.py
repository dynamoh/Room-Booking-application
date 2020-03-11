from django.urls import path
from accounts.api.views import (
            customer_registration_view,
            manager_registration_view,
            RoomDetailView,
            TimeslotDetailView,
            BookingDetailView,
            CustomerListView,
            CustomerDetailView
)

app_name = "useraccount"

urlpatterns = [
    path('customers/',CustomerListView.as_view()),
    path('customers/<int:pk>/',CustomerDetailView.as_view()),
    path('register/customer',customer_registration_view,name="registercustomer"),
    path('register/manager',manager_registration_view,name="registermanager"),
    path('room/<str:slug>/',RoomDetailView.as_view()),
    path('timeslot/<str:room_id>/',TimeslotDetailView.as_view()),
    path('bookings/<str:room_timeslot_booked>/',BookingDetailView.as_view())
]
