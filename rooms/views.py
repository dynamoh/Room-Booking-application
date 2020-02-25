from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Customer,Manager,Room,RoomBooked,TimeSlot
from datetime import timedelta,datetime
from django.shortcuts import get_object_or_404,render_to_response

# Create your views here.

@login_required
def homepage(request):
    return render(request,'home.html')

@login_required
def create_rooms(request):
    if request.method == 'POST' and request.user.manager==True:
        manager = Manager.objects.filter(manager_id = request.user).first()
        room_number = request.POST.get('room_number')
        room_pic = request.FILES.get('room_pic')
        prior_days = request.POST.get('prior_booking_days')
        obj_room = Room.objects.create(room_manager=manager,room_number=room_number,room_pic=room_pic,prior_booking_days=prior_days)
        start_times = request.POST.getlist('fn_start_time')
        end_times = request.POST.getlist('fn_end_time')

        print(start_times)
        print(end_times)
        for i in range(0,len(start_times)):
            TimeSlot.objects.create(room_id=obj_room,start_time=str(start_times[i]),end_time=str(end_times[i]))

    return render(request,'create_room.html')


@login_required
def show_rooms(request):
    rooms = Room.objects.all()
    return render(request,'show_rooms.html',{'rooms':rooms})

def room_detail(request,slug):
    room = get_object_or_404(Room, slug=slug)
    print(room)
    print(slug)
    day = request.POST.get('check_day')
    slots = TimeSlot.objects.filter(room_id=room)
    start_date = datetime.now().strftime ("%Y-%m-%d")
    date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = date + timedelta(days=room.prior_booking_days)
    end_date=datetime.strftime(end_date, "%Y-%m-%d")
    return render(request,'room_detail.html',{'room':room,'slots':slots,'start_date':start_date,'end_date':end_date})

















    #
