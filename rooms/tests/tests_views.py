from django.test import TestCase, Client
from django.urls import reverse
from rooms.models import Customer,Manager,Room,RoomBooked,TimeSlot,ContactUs
from accounts.models import User
import json

class TestViews(TestCase):

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

        print(self.manager_user)
        self.client.login(email='manager@gmail.com',password='abcd@1234')

        # self.room1 = Room.objects.create(room_manager=self.manager,
        #                                 room_number='A-301',
        #                                 room_pic="",
        #                                 room_type="Single Room",
        #                                 prior_booking_days=10,
        #                                 price=1999)
        # self.room2 = Room.objects.create(room_manager=self.manager,
        #                                 room_number='A-302',
        #                                 room_pic="",
        #                                 room_type="Family Room",
        #                                 prior_booking_days=15,
        #                                 price=2999)
        # self.room3 = Room.objects.create(room_manager=self.manager,
        #                                 room_number='A-303',
        #                                 room_pic="",
        #                                 room_type="Delux Suite",
        #                                 prior_booking_days=20,
        #                                 price=3999)
        # self.timeslot11 = TimeSlot.objects.create(room_id=self.room1,
        #                                         start_time="14:00",
        #                                         end_time="20:00")
        # self.timeslot12 = TimeSlot.objects.create(room_id=self.room1,
        #                                         start_time="02:00",
        #                                         end_time="10:00")
        # self.timeslot13 = TimeSlot.objects.create(room_id=self.room1,
        #                                         start_time="10:00",
        #                                         end_time="12:00")
        # self.timeslot21 = TimeSlot.objects.create(room_id=self.room1,
        #                                         start_time="04:00",
        #                                         end_time="07:00")
        # self.timeslot22 = TimeSlot.objects.create(room_id=self.room1,
        #                                         start_time="08:00",
        #                                         end_time="12:00")
        # self.timeslot23 = TimeSlot.objects.create(room_id=self.room1,
        #                                         start_time="14:00",
        #                                         end_time="16:00")
        # self.timeslot31 = TimeSlot.objects.create(room_id=self.room1,
        #                                         start_time="6:00",
        #                                         end_time="10:00")
        # self.timeslot32 = TimeSlot.objects.create(room_id=self.room1,
        #                                         start_time="14:00",
        #                                         end_time="20:00")
        # self.timeslot33 = TimeSlot.objects.create(room_id=self.room1,
        #                                         start_time="20:00",
        #                                         end_time="23:00")


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

        print(response)
        self.assertEquals(response.status_code,302)
        self.assertEquals(Room.objects.all().first().room_number,'A-3011')















        #
