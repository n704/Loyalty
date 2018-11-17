# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

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
            booking = Booking()
            booking.user = user
            booking.room = room
            booking.status = status
            room.reduce_available_amount()
            user.reduce_bonus_points()
            booking.save()
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

    def reduce_bonus_points(self):
        if self.bonus_point > 0:
            self.bonus_point -= 1
            self.save()



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
