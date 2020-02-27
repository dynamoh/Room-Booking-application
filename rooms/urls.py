from django.urls import path
from .views import homepage,create_rooms,cancel_booking,show_rooms,room_detail,book_slot,contact_us_add,customer_profile,customer_bookings,show_all_rooms
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
    path('cancel/',cancel_booking,name="CancelBooking")
]

if(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
