from django.urls import path
from accounts.api.views import (
            customer_registration_view,
            manager_registration_view,
            RoomDetailView,
)

app_name = "useraccount"

urlpatterns = [
    path('register/customer',customer_registration_view,name="registercustomer"),
    path('register/manager',manager_registration_view,name="registermanager"),
    path('<pk>/',RoomDetailView.as_view())
]
