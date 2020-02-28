from django.test import SimpleTestCase
from django.urls import reverse,resolve
from rooms.views import (homepage,create_rooms,rooms_created_by_manager,
                    cancel_booking,room_detail,book_slot,
                    contact_us_add,customer_profile,customer_bookings,
                    show_all_rooms,manager_rooms_detail,delete_timeslot,
                    edit_room_details,manager_booking_details)

class TestUrls(SimpleTestCase):

    def test_homepage_url(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, homepage)

    def test_create_rooms_url(self):
        url = reverse('Add_Room')
        self.assertEquals(resolve(url).func, create_rooms)

    def test_rooms_created_by_manager_url(self):
        url = reverse('ManagerRooms')
        self.assertEquals(resolve(url).func, rooms_created_by_manager)

    def test_cancel_booking_url(self):
        url = reverse('CancelBooking')
        self.assertEquals(resolve(url).func, cancel_booking)

    def test_room_detail_url(self):
        url = reverse('Room_Detail',args=['slug'])
        self.assertEquals(resolve(url).func, room_detail)

    def test_book_slot_url(self):
        url = reverse('Book_Room')
        self.assertEquals(resolve(url).func, book_slot)

    def test_contact_us_add_url(self):
        url = reverse('ContactUsPage')
        self.assertEquals(resolve(url).func, contact_us_add)

    def test_customer_profile_url(self):
        url = reverse('ProfilePage')
        self.assertEquals(resolve(url).func, customer_profile)

    def test_customer_bookings_url(self):
        url = reverse('PreviousBookings')
        self.assertEquals(resolve(url).func, customer_bookings)

    def test_show_all_rooms_url(self):
        url = reverse('Rooms')
        self.assertEquals(resolve(url).func, show_all_rooms)

    def test_manager_rooms_detail_url(self):
        url = reverse('ManagerRoomsDetail',args=['slug'])
        self.assertEquals(resolve(url).func, manager_rooms_detail)

    def test_delete_timeslot_url(self):
        url = reverse('DeleteTimeslot')
        self.assertEquals(resolve(url).func, delete_timeslot)

    def test_edit_room_details_url(self):
        url = reverse('EditRoomDetails')
        self.assertEquals(resolve(url).func, edit_room_details)

    def test_manager_booking_details_url(self):
        url = reverse('BookingDetails',args=['slug'])
        self.assertEquals(resolve(url).func, manager_booking_details)
