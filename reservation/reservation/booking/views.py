# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
# Create your views here.
class BookRoomView(View):

    def get(self, request, *args, **kwargs):
        """
        """
        from booking.models import *
        rooms = Room.objects.count()
        return JsonResponse({'room': rooms})

    def post(self, request, *args, **kwargs):
        """
        """
        from booking.form import *
        from booking.models import *
        import json
        import sys
        print >>sys.stderr, json.loads(request.body)
        booking_data = RoomForm(json.loads(request.body))
        if booking_data.is_valid():
            user = booking_data.cleaned_data.get('user')
            room = booking_data.cleaned_data.get('room')
            status = Booking.objects.get_status(user, room)
            oBooking = Booking.objects.create_booking(user, room, status)
            return JsonResponse({'data': {
                'room_id': booking_data.cleaned_data.get('room_id'),
                'user_id': booking_data.cleaned_data.get('user_id'),
                'status': status
            }})
        else:
            print >>sys.stderr, booking_data.errors
            return JsonResponse({'error': dict(booking_data.errors.items())})
        return JsonResponse({'room': '1'})
