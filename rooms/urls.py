from django.urls import path
from .views import homepage,create_rooms,show_rooms,room_detail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',homepage,name="homepage"),
    path('create_room/',create_rooms,name="Add_Room"),
    path('rooms/',show_rooms,name="Rooms"),
    path('rooms/<str:slug>/',room_detail,name="Room_Detail"),
]

if(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
