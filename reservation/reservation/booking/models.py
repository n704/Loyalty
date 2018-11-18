# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db import transaction

# Create your models here.
class Room(models.Model):
    """
    Room in the hotels
    """
    name = models.CharField(max_length=255, blank=False)
    available_amount = models.IntegerField(default=0)
    required_points = models.IntegerField(default=250)

    def reduce_available_amount(self):
        if self.available_amount > 0:
            self.available_amount -= 1
            self.save()

class BookingManager(models.Manager):
    """
    """

    def create_booking(self, user, room, status):
        """
        """
        try:
            with transaction.atomic():
                booking = Booking()
                booking.user = user
                booking.room = room
                booking.status = status
                room.reduce_available_amount()
                user.reduce_bonus_points(room.required_points)
                booking.save()
                return True, "Sucess"
        except Exception as e:
            return False, "Failed"



    def get_status(self, user, room):
        """
        """
        if user.bonus_point > room.required_points:
            status = Booking.RESERVED
        else:
            status = Booking.PENDING_APPROVAL
        return status


    def validate(self, data):
        """
        """
        room_id = data.get("room_id",'')
        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return False, "Room does not exist"
        user_id = data.get("user_id", '')
        try:
            user = BookingUser.objects.get(pk=user_id)
        except BookingUser.DoesNotExist:
            return False, "User does not exist"


class BookingUser(models.Model):
    """
    User
    """
    name = models.CharField(max_length=255, null=False)
    bonus_point = models.IntegerField(default=0)

    def reduce_bonus_points(self, value):
        import os, requests
        SCORE_HOST = os.environ.get('SCORE_HOST')
        SCORE_URI = os.environ.get('SCORE_URI')
        SCORE_PORT = os.environ.get('SCORE_PORT')
        url = 'http://{0}:{1}{2}'.format(SCORE_HOST,SCORE_PORT,SCORE_URI)
        SCORE_API_KEY = os.environ.get('SCORE_API_KEY')
        headers = {
            'SCORE_KEY': SCORE_API_KEY
        }
        try:
            res = requests.post(url, {"user_id": self.pk, "value": value}, headers=headers)
            status = res.status_code
        except Exception as e:
            status = 400
        if status != 200:
            raise Exception("Failed")



class Booking(models.Model):
    """
    Booking by user
    """
    RESERVED = 'RESERVED'
    PENDING_APPROVAL = 'PENDING_APPROVAL'
    STATUS_CHOICE = (
                        (RESERVED,'RESERVED'),
                        (PENDING_APPROVAL,'PENDING_APPROVAL'),
                    )
    user = models.ForeignKey(BookingUser,null=False)
    status = models.CharField(max_length=255, choices=STATUS_CHOICE)
    room = models.ForeignKey(Room, null=False)

    objects = BookingManager()
