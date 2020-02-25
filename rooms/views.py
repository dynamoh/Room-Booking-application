from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Customer,Manager,Room,RoomBooked,TimeSlot
from datetime import timedelta,datetime
from django.shortcuts import get_object_or_404,render_to_response
from django.http import HttpResponseRedirect

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
    print(day)
    start_date = datetime.now().strftime ("%Y-%m-%d")
    date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = date + timedelta(days=room.prior_booking_days)
    end_date=datetime.strftime(end_date, "%Y-%m-%d")
    if day!="" and day!=None:
        obj_slot_booked = RoomBooked.objects.filter(booked_for=day)
        booked_timeslots = []
        for i in obj_slot_booked:
            booked_timeslots.append(i.room_timeslot_booked)
        timeslots = TimeSlot.objects.filter(room_id=room)
        all_slots = []
        for i in timeslots:
            all_slots.append(i)
        available_slots = []
        for i in all_slots:
            if i not in booked_timeslots:
                available_slots.append(i)
        print(available_slots)
        return render(request,'room_detail.html',{'date':day,'room':room,'avail_slots':available_slots,'start_date':start_date,'end_date':end_date})
    else:
        slots = TimeSlot.objects.filter(room_id=room)
        return render(request,'room_detail.html',{'room':room,'slots':slots,'start_date':start_date,'end_date':end_date})

def book_slot(request):
    room_no = request.POST.get('room_number')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    booked_for = request.POST.get('booked_for')
    room = Room.objects.filter(room_number = room_no).first()
    timeslot = TimeSlot.objects.filter(room_id=room).filter(start_time=start_time).filter(end_time=end_time).first()
    customer = Customer.objects.filter(customer_id=request.user).first()
    RoomBooked.objects.create(room_timeslot_booked=timeslot,booked_for=booked_for,customer_booked=customer)
    return HttpResponseRedirect('/')
















    #
