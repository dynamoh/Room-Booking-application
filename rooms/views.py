from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Customer,Manager,Room,RoomBooked,TimeSlot,ContactUs
from datetime import timedelta,datetime
from django.shortcuts import get_object_or_404,render_to_response
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

# Create your views here.


def homepage(request):
    rooms = Room.objects.all()
    return render(request,'index.html',{'room':rooms})

@login_required
def create_rooms(request):
    if request.method == 'POST' and request.user.manager==True:
        manager = Manager.objects.filter(manager_id = request.user).first()
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('room_type')
        price = request.POST.get('price')
        room_pic = request.FILES.get('room_pic')
        prior_days = request.POST.get('prior_booking_days')
        obj_room = Room.objects.create(room_manager=manager,room_type=room_type,price=price,room_number=room_number,room_pic=room_pic,prior_booking_days=prior_days)
        start_times = request.POST.getlist('fn_start_time')
        end_times = request.POST.getlist('fn_end_time')

        for i in range(0,len(start_times)):
            TimeSlot.objects.create(room_id=obj_room,start_time=str(start_times[i]),end_time=str(end_times[i]))
        return HttpResponseRedirect('/manager/rooms/')
    return render(request,'create_room.html')


@login_required
def show_rooms(request):
    rooms = Room.objects.all()
    return render(request,'show_rooms.html',{'rooms':rooms})


def room_detail(request,slug):
    room = get_object_or_404(Room, slug=slug)
    day = request.POST.get('check_day')
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
        if len(available_slots)==0:
            return render(request,'room_detail.html',{'date':day,'room':room,'no_slots':1,'start_date':start_date,'end_date':end_date})
        return render(request,'room_detail.html',{'date':day,'room':room,'avail_slots':available_slots,'start_date':start_date,'end_date':end_date})
    else:
        slots = TimeSlot.objects.filter(room_id=room)
        return render(request,'room_detail.html',{'room':room,'slots':slots,'start_date':start_date,'end_date':end_date})

@login_required
def book_slot(request):
    if request.user.customer == True:
        room_no = request.POST.get('room_number')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        booked_for = request.POST.get('booked_for')
        room = Room.objects.filter(room_number = room_no).first()
        timeslot = TimeSlot.objects.filter(room_id=room).filter(start_time=start_time).filter(end_time=end_time).first()
        customer = Customer.objects.filter(customer_id=request.user).first()
        RoomBooked.objects.create(room_timeslot_booked=timeslot,booked_for=booked_for,customer_booked=customer)
        return HttpResponseRedirect('/bookings/')
    return HttpResponseRedirect('/')

@login_required
def customer_profile(request):
    if request.user.customer:
        logged_user = Customer.objects.filter(customer_id=request.user).first()
    else:
        logged_user = Manager.objects.filter(manager_id=request.user).first()
    if request.method == 'POST':
        email = request.POST.get('email_id')
        full_name = request.POST.get('full_name')
        contact = request.POST.get('contact')
        profession = request.POST.get('profession')
        address = request.POST.get('address')
        city = request.POST.get('city')
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic!="" and profile_pic!=None:
            if profile_pic != None:
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                uploaded_file_url = fs.url(filename)
            if request.user.customer:
                Customer.objects.filter(customer_id=request.user).update(contact=contact,profession=profession,address=address,city=city,profile_pic=profile_pic)
            else:
                Manager.objects.filter(customer_id=request.user).update(contact=contact,address=address,city=city,profile_pic=profile_pic)
        else:
            if request.user.customer:
                Customer.objects.filter(customer_id=request.user).update(contact=contact,profession=profession,address=address,city=city)
            else:
                Manager.objects.filter(manager_id=request.user).update(contact=contact,address=address,city=city)

        if request.user.customer:
            logged_user = Customer.objects.filter(customer_id=request.user).first()
        else:
            logged_user = Manager.objects.filter(manager_id=request.user).first()
    return render(request,'profile.html',{'logged_user':logged_user})

@login_required
def customer_bookings(request):
    if request.user.customer == True:
        customer_id = Customer.objects.filter(customer_id=request.user).first()
        date = datetime.now().date()
        previous_bookings = RoomBooked.objects.filter(customer_booked=customer_id).filter(booked_for__lte=date).order_by('-booked_on')
        future_bookings = RoomBooked.objects.filter(customer_booked=customer_id).filter(booked_for__gte=date).order_by('-booked_on')
        return render(request,'bookings.html',{'previous_bookings':previous_bookings,'future_bookings':future_bookings})
    return HttpResponseRedirect('/')

def show_all_rooms(request):
    rooms = Room.objects.all()
    return render(request,'rooms.html',{'rooms':rooms})

def contact_us_add(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        ContactUs.objects.create(full_name=full_name,email=email,phone=phone,message=message)
    return HttpResponseRedirect('/')

@login_required
def cancel_booking(request):
    if request.user.customer == True:
        if request.method == 'POST':
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            room_no = request.POST.get('room_no')
            booked_for = request.POST.get('booked_for')
            cust = Customer.objects.filter(customer_id=request.user).first()
            room = Room.objects.filter(room_number=room_no).first()
            timeslot = TimeSlot.objects.filter(room_id=room).filter(start_time=start_time).filter(end_time=end_time).first()
            RoomBooked.objects.filter(customer_booked=cust).filter(room_timeslot_booked=timeslot).filter(booked_for=booked_for).delete()
        return HttpResponseRedirect('/bookings/')
    return HttpResponseRedirect('/')

@login_required
def rooms_created_by_manager(request):
    if request.user.manager == True:
        manager = Manager.objects.filter(manager_id = request.user).first()
        room = Room.objects.filter(room_manager=manager)
        return render(request,'manager_rooms.html',{'room':room})
    return HttpResponseRedirect('/')

@login_required
def manager_rooms_detail(request,slug):
    if request.user.manager == True:
        room = get_object_or_404(Room, slug=slug)
        day = request.POST.get('check_day')
        start_date = datetime.now().strftime ("%Y-%m-%d")
        date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = date + timedelta(days=room.prior_booking_days)
        end_date=datetime.strftime(end_date, "%Y-%m-%d")
        slots = TimeSlot.objects.filter(room_id=room)
        return render(request,'manager_room_detail.html',{'room':room,'slots':slots,'start_date':start_date,'end_date':end_date})
    return HttpResponseRedirect('/')

@login_required
def delete_timeslot(request):
    if request.user.manager == True:
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        room_no = request.POST.get('room_no')
        room = Room.objects.filter(room_number=room_no).first()
        TimeSlot.objects.filter(room_id=room).filter(start_time=start_time).filter(end_time=end_time).delete()
        return HttpResponseRedirect('/manager/rooms/')
    return HttpResponseRedirect('/')

@login_required
def edit_room_details(request):
    if request.user.manager == True:
        if request.method == 'POST':
            manager = Manager.objects.filter(manager_id = request.user).first()
            room_number = request.POST.get('room_number')
            room_type = request.POST.get('room_type')
            price = request.POST.get('price')
            room_pic = request.FILES.get('room_pic')
            prior_days = request.POST.get('prior_booking_days')
            if room_pic!="" and room_pic!=None:
                Room.objects.filter(room_number=room_number).update(room_type=room_type,price=price,prior_booking_days=prior_days,room_pic=room_pic)
            else:
                Room.objects.filter(room_number=room_number).update(room_type=room_type,price=price,prior_booking_days=prior_days)
        return HttpResponseRedirect('/manager/rooms/')
    return HttpResponseRedirect('/')

@login_required
def manager_booking_details(request,slug):
    if request.user.manager == True:
        room = get_object_or_404(Room, slug=slug)
        timeslot = TimeSlot.objects.filter(room_id=room).first()
        bookings = RoomBooked.objects.filter(room_timeslot_booked=timeslot).order_by('-booked_for')
        return render(request,'manager_bookings.html',{'bookings':bookings,'room':room})
    return HttpResponseRedirect('/')

def delete_room(request):
    if request.user.manager == True:
        room_no = request.POST.get('room_no')
        Room.objects.filter(room_number=room_no).delete()
        return HttpResponseRedirect('/manager/rooms')
    return HttpResponseRedirect('/')















    #
