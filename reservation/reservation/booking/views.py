# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
# Create your views here.
class BookRoomView(View):


    def post(self, request, *args, **kwargs):
        """
        """
        from booking.form import *
        from booking.models import *
        import json
        booking_data = RoomForm(json.loads(request.body))
        if booking_data.is_valid():
            user = booking_data.cleaned_data.get('user')
            room = booking_data.cleaned_data.get('room')
            status = Booking.objects.get_status(user, room)
            commit_status, message = Booking.objects.create_booking(user, room, status)
            if commit_status:
                return JsonResponse({'data': {
                    'room_id': booking_data.cleaned_data.get('room_id'),
                    'user_id': booking_data.cleaned_data.get('user_id'),
                    'status': status
                }})
            else:
                return JsonResponse({'error': message}, status=400)
        else:
            return JsonResponse({'error': dict(booking_data.errors.items())}, status=400)
        return JsonResponse({'room': room.pk})
