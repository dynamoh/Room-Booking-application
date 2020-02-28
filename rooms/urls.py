from django.urls import path
from .views import (homepage,create_rooms,rooms_created_by_manager,
                    cancel_booking,room_detail,book_slot,
                    contact_us_add,customer_profile,customer_bookings,
                    show_all_rooms,manager_rooms_detail,delete_timeslot,
                    edit_room_details,manager_booking_details,delete_room)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',homepage,name="homepage"),
    path('create_room/',create_rooms,name="Add_Room"),
    path('rooms/',show_all_rooms,name="Rooms"),
    path('rooms/<str:slug>/',room_detail,name="Room_Detail"),
    path('book/',book_slot,name="Book_Room"),
    path('profile/',customer_profile,name="ProfilePage"),
    path('bookings/',customer_bookings,name="PreviousBookings"),
    path('contact/',contact_us_add,name="ContactUsPage"),
    path('cancel/',cancel_booking,name="CancelBooking"),
    path('manager/rooms/',rooms_created_by_manager,name="ManagerRooms"),
    path('manager/rooms/<str:slug>/',manager_rooms_detail,name="ManagerRoomsDetail"),
    path('delete/',delete_timeslot,name="DeleteTimeslot"),
    path('edit/',edit_room_details,name="EditRoomDetails"),
    path('booking/details/<str:slug>/',manager_booking_details,name="BookingDetails"),
    path('rooms/manager/delete/',delete_room,name="DeleteRoom")
]

if(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
