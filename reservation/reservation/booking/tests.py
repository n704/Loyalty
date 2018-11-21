# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from mock import patch, Mock, MagicMock
# Create your tests here.
from booking.form import RoomForm
from booking.models import *
from booking.views import BookRoomView

class RoomFormTest(TestCase):

    def test_form_logic(self):

        data = { "room_id": 34, "user_id": 34}
        form = RoomForm(data)
        self.assertEquals(form.is_valid(), False)
        self.assertEquals(dict(form.errors.items()), {"room_id": ["Invalid Room"], "user_id": ["Invalid User"]})
        room = Room()
        room.name ='1'
        room.save()
        user = BookingUser()
        user.name = 'John'
        user.save()
        data = { "room_id": room.pk, "user_id": user.pk}
        form = RoomForm(data)
        self.assertEquals(form.is_valid(), True)

class BookingTest(TestCase):

    def test_get_status(self):
        """
        testing get_status of hotel rooms.
        """
        room = Room()
        room.name ='1'
        room.save()
        user = BookingUser()
        user.name = 'John'
        user.save()
        status = Booking.objects.get_status(user, room)
        self.assertEquals(status, Booking.PENDING_APPROVAL)
        room.required_points = 150
        room.save()
        user.bonus_point = 150
        user.save()
        status = Booking.objects.get_status(user, room)
        self.assertEquals(status, Booking.PENDING_APPROVAL)
        room.available_amount = 1
        room.save()
        status = Booking.objects.get_status(user, room)
        self.assertEquals(status, Booking.RESERVED)

    def test_create_booking(self):
        """
        Creating new booking.
        """
        room = Room()
        room.name ='1'
        room.save()
        user = BookingUser()
        user.name = 'John'
        user.save()
        status = Booking.RESERVED
        # error on no room available
        status, message = Booking.objects.create_booking(user, room, status)
        self.assertEquals(status, False)
        self.assertEquals(message, "No Room available.")
        room.available_amount = 1
        room.save()
        def foo(x):
            raise Exception("Failed")
        user.reduce_bonus_points = foo
        # error on user point updation
        status, message = Booking.objects.create_booking(user, room, status)
        self.assertEquals(status, False)
        self.assertEquals(message, "Failed")
        def foo(x):
            pass
        user.reduce_bonus_points = foo
        count = Booking.objects.count()
        room.available_amount = 1
        # success updating count of booking increament by 1
        status, message = Booking.objects.create_booking(user, room, status)
        self.assertEquals(status, True)
        self.assertEquals(message, "Success")
        new_count = Booking.objects.count()
        self.assertEquals(count + 1, new_count)


class RoomTest(TestCase):
    def test_reduce_room_avialablity(self):
        """
        Reduce no of room function to be tested.
        """
        room = Room()
        room.name = "212"
        room.save()
        # no room available throw error
        self.assertRaises(Exception, lambda: room.reduce_available_amount())
        room.available_amount = 1
        room.save()
        # 1 room available
        room.reduce_available_amount()
        self.assertEquals(room.available_amount, 0)
        # no room available
        self.assertRaises(Exception, lambda: room.reduce_available_amount())


def return_mock_400():
    mock = Mock()
    mock.status_code = 400
    return mock

def return_mock_200():
    mock = Mock()
    mock.status_code = 200
    return mock

class TestBookingUser(TestCase):
    @patch('requests.post', side_effect=Exception)
    def test_reduce_bonus_points(self, mock_fn):
        """
        test reduce bonus point for a user.
        """
        user = BookingUser()
        user.name = '123'
        user.save()
        self.assertRaises(Exception, lambda:user.reduce_bonus_points())

    @patch('requests.post', return_value=return_mock_400())
    def test_reduce_bonus_points_success(self, mock_fn):
        user = BookingUser()
        user.name = '123'
        user.save()
        self.assertRaises(Exception, lambda:user.reduce_bonus_points(12))

    @patch('requests.post', return_value=return_mock_200())
    def test_reduce_bonus_points_success(self, mock_fn):
        user = BookingUser()
        user.name = '123'
        user.save()
        self.assertEquals(user.reduce_bonus_points(12), None)


class TestBookRoomView(TestCase):

    def test_post(self):
        """
        post api call test.
        """
        request = Mock()
        request.body = '{"user_id": 99, "room_id": 99}'
        book_room_view = BookRoomView()
        res = book_room_view.post(request)
        self.assertEquals(res.status_code, 400)
        user = BookingUser()
        user.name = '123'
        user.save()
        room = Room()
        room.name = "212"
        room.save()
        request.body = '{"user_id": '+str(user.pk)+', "room_id": '+str(room.pk)+'}'
        res = book_room_view.post(request)
        self.assertEquals(res.status_code, 400)
        with patch.object(BookingManager, "create_booking", return_value=(True,'')) as mock_method:
            res = book_room_view.post(request)
            self.assertEquals(res.status_code, 200)
