from django.test import TestCase, Client
from django.urls import reverse
from rooms.models import Customer,Manager,Room,RoomBooked,TimeSlot,ContactUs
from accounts.models import User
from datetime import timedelta,datetime
import json

class ManagerTestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.customer_user = User.objects.create(name="customer",
                                                email="customer@gmail.com",
                                                customer=True,
                                                manager=False)

        self.customer_user.set_password('abcd@1234')
        self.customer_user.save()

        self.manager_user = User.objects.create(name="manager",
                                                email="manager@gmail.com",
                                                customer=False,
                                                manager=True)

        self.manager_user.set_password('abcd@1234')
        self.manager_user.save()

        self.customer  = Customer.objects.create(customer_id=self.customer_user,
                                                contact="8859634789",
                                                address="House no. 21 street no. x,annapurna",
                                                city="Indore",
                                                profession="Student",
                                                profile_pic="")
        self.manager  = Manager.objects.create(manager_id=self.manager_user,
                                                contact="8859634789",
                                                address="House no. 21 street no. x,annapurna",
                                                city="Indore",
                                                profile_pic="")

        self.client.login(email='manager@gmail.com',password='abcd@1234')

        self.room1 = Room.objects.create(room_manager=self.manager,
                                        room_number='A-301',
                                        room_pic="",
                                        room_type="Single Room",
                                        prior_booking_days=10,
                                        price=1999)
        self.room2 = Room.objects.create(room_manager=self.manager,
                                        room_number='A-302',
                                        room_pic="",
                                        room_type="Family Room",
                                        prior_booking_days=15,
                                        price=2999)
        self.room3 = Room.objects.create(room_manager=self.manager,
                                        room_number='A-303',
                                        room_pic="",
                                        room_type="Delux Suite",
                                        prior_booking_days=20,
                                        price=3999)
        self.timeslot11 = TimeSlot.objects.create(room_id=self.room1,
                                                start_time="14:00",
                                                end_time="20:00")
        self.timeslot12 = TimeSlot.objects.create(room_id=self.room1,
                                                start_time="02:00",
                                                end_time="10:00")
        self.timeslot13 = TimeSlot.objects.create(room_id=self.room1,
                                                start_time="10:00",
                                                end_time="12:00")
        self.timeslot21 = TimeSlot.objects.create(room_id=self.room2,
                                                start_time="04:00",
                                                end_time="07:00")
        self.timeslot22 = TimeSlot.objects.create(room_id=self.room2,
                                                start_time="08:00",
                                                end_time="12:00")
        self.timeslot23 = TimeSlot.objects.create(room_id=self.room2,
                                                start_time="14:00",
                                                end_time="16:00")
        self.timeslot31 = TimeSlot.objects.create(room_id=self.room3,
                                                start_time="6:00",
                                                end_time="10:00")
        self.timeslot32 = TimeSlot.objects.create(room_id=self.room3,
                                                start_time="14:00",
                                                end_time="20:00")
        self.timeslot33 = TimeSlot.objects.create(room_id=self.room3,
                                                start_time="20:00",
                                                end_time="23:00")


    def test_rooms_list_get(self):
        response = self.client.get(reverse('homepage'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'index.html')

    def test_create_rooms_post_request(self):
        response = self.client.post(reverse('Add_Room'),{'room_number':'A-3011',
                                                        'room_type':"Single Room",
                                                        'prior_booking_days':10,
                                                        'price':1999,
                                                        'room_pic':"",
                                                        'fn_start_time':{'14:00','02:00','10:00'},
                                                        'fn_end_time':{'20:00','10:00','12:00'}})

        self.assertEquals(response.status_code,302)
        self.assertEquals(Room.objects.filter(room_number='A-3011').first().room_type,'Single Room')

    def test_rooms_created_by_manager_get_request(self):
        response = self.client.get(reverse('ManagerRooms'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'manager_rooms.html')
        self.assertEquals(response.context['room'].count(),3)

    def test_manager_rooms_detail_get_request(self):
        response = self.client.get(reverse('ManagerRoomsDetail',args=['a-301']))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'manager_room_detail.html')
        self.assertEquals(response.context['room'].room_number,'A-301')

    def test_delete_timeslot_post_request(self):
        TimeSlot.objects.create(room_id=self.room1,start_time="20:00",end_time="23:00")
        response = self.client.post(reverse('DeleteTimeslot'),{'start_time':'20:00',
                                                                'end_time':'23:00',
                                                                'room_no':'A-301'})
        self.assertEquals(TimeSlot.objects.all().count(),9)

    def test_edit_room_details_post_request(self):
        response = self.client.post(reverse('EditRoomDetails'),{'room_number':'A-301',
                                                                'room_type':'Delux Suite',
                                                                'price':4999,
                                                                'prior_booking_days':25,
                                                                'room_pic':''})
        self.assertEquals(response.status_code,302)
        self.assertEquals(Room.objects.filter(room_number='A-301').first().price,4999)
        self.assertEquals(Room.objects.filter(room_number='A-301').first().room_type,'Delux Suite')

    def test_manager_booking_details_get_request(self):
        RoomBooked.objects.create(customer_booked=self.customer,room_timeslot_booked=self.timeslot11,booked_for='2020-03-09')
        response = self.client.get(reverse('BookingDetails',args=['a-301']))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'manager_bookings.html')
        self.assertEquals(response.context['bookings'][0].room_timeslot_booked.room_id.room_number,'A-301')

    def test_delete_room_post_request(self):
        Room.objects.create(room_manager=self.manager,
                                        room_number='A-309',
                                        room_pic="",
                                        room_type="Single Room",
                                        prior_booking_days=20,
                                        price=2999)
        response = self.client.post(reverse('DeleteRoom'),{'room_no':'A-309'})
        self.assertEquals(Room.objects.all().count(),3)


class CustomerTestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.customer_user = User.objects.create(name="customer",
                                                email="customer@gmail.com",
                                                customer=True,
                                                manager=False)

        self.customer_user.set_password('abcd@1234')
        self.customer_user.save()

        self.manager_user = User.objects.create(name="manager",
                                                email="manager@gmail.com",
                                                customer=False,
                                                manager=True)

        self.manager_user.set_password('abcd@1234')
        self.manager_user.save()

        self.customer  = Customer.objects.create(customer_id=self.customer_user,
                                                contact="8859634789",
                                                address="House no. 21 street no. x,annapurna",
                                                city="Indore",
                                                profession="Student",
                                                profile_pic="")
        self.manager  = Manager.objects.create(manager_id=self.manager_user,
                                                contact="8859634789",
                                                address="House no. 21 street no. x,annapurna",
                                                city="Indore",
                                                profile_pic="")

        self.client.login(email='customer@gmail.com',password='abcd@1234')

        self.room1 = Room.objects.create(room_manager=self.manager,
                                        room_number='A-301',
                                        room_pic="",
                                        room_type="Single Room",
                                        prior_booking_days=10,
                                        price=1999)
        self.room2 = Room.objects.create(room_manager=self.manager,
                                        room_number='A-302',
                                        room_pic="",
                                        room_type="Family Room",
                                        prior_booking_days=15,
                                        price=2999)
        self.room3 = Room.objects.create(room_manager=self.manager,
                                        room_number='A-303',
                                        room_pic="",
                                        room_type="Delux Suite",
                                        prior_booking_days=20,
                                        price=3999)
        self.timeslot11 = TimeSlot.objects.create(room_id=self.room1,
                                                start_time="14:00",
                                                end_time="20:00")
        self.timeslot12 = TimeSlot.objects.create(room_id=self.room1,
                                                start_time="02:00",
                                                end_time="10:00")
        self.timeslot13 = TimeSlot.objects.create(room_id=self.room1,
                                                start_time="10:00",
                                                end_time="12:00")
        self.timeslot21 = TimeSlot.objects.create(room_id=self.room2,
                                                start_time="04:00",
                                                end_time="07:00")
        self.timeslot22 = TimeSlot.objects.create(room_id=self.room2,
                                                start_time="08:00",
                                                end_time="12:00")
        self.timeslot23 = TimeSlot.objects.create(room_id=self.room2,
                                                start_time="14:00",
                                                end_time="16:00")
        self.timeslot31 = TimeSlot.objects.create(room_id=self.room3,
                                                start_time="6:00",
                                                end_time="10:00")
        self.timeslot32 = TimeSlot.objects.create(room_id=self.room3,
                                                start_time="14:00",
                                                end_time="20:00")
        self.timeslot33 = TimeSlot.objects.create(room_id=self.room3,
                                                start_time="20:00",
                                                end_time="23:00")

    def test_Room_Detail_get_request(self):
        response = self.client.get(reverse('Room_Detail',args=['a-301']))

        start_date = datetime.now().strftime ("%Y-%m-%d")
        date = datetime.strptime(start_date, "%Y-%m-%d")

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'room_detail.html')
        self.assertEquals(response.context['start_date'],start_date)
        self.assertEquals(response.context['room'].room_number,'A-301')

    def test_book_slot_post_request(self):
        response = self.client.post(reverse('Book_Room'),{'room_number':'A-301',
                                                            'start_time':'14:00',
                                                            'end_time':'20:00',
                                                            'booked_for':'2020-03-06'})
        self.assertEquals(response.status_code,302)
        self.assertEquals(RoomBooked.objects.all().first().room_timeslot_booked.start_time,'14:00')

    def test_customer_profile_post_request(self):
        response = self.client.post(reverse('ProfilePage'),{'full_name':'customer',
                                                            'email_id':'customer@gmail.com',
                                                            'contact':'8865454211',
                                                            'profession':'Student',
                                                            'address':'fgsb fhdsjhfdfv s',
                                                            'city':'Indore',
                                                            'profile_pic':''})

        self.assertEquals(response.context['logged_user'].contact,'8865454211')

    def test_customer_bookings_get_request(self):
        RoomBooked.objects.create(customer_booked=self.customer,room_timeslot_booked=self.timeslot11,booked_for='2020-03-09')
        response = self.client.get(reverse('PreviousBookings'))
        self.assertEquals(response.context['future_bookings'][0].room_timeslot_booked,self.timeslot11)

    def test_cancel_booking_post_request(self):
        RoomBooked.objects.create(customer_booked=self.customer,room_timeslot_booked=self.timeslot11,booked_for='2020-03-09')
        response = self.client.post(reverse('CancelBooking'),{'room_no':'A-301',
                                                            'start_time':'14:00',
                                                            'end_time':'20:00',
                                                            'booked_for':'2020-03-09'})

        self.assertEquals(RoomBooked.objects.all().count(),0)

    def test_contact_us_add_post_request(self):
        response = self.client.post(reverse('ContactUsPage'),{'full_name':'Abcd jsad',
                                                                'email':'abcd@gmail.com',
                                                                'phone':'8965512313',
                                                                'message':'fghdsf fgdshf fdhb'})













        #
