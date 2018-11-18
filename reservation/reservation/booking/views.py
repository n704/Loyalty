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
        import os, sys, requests
        print >>sys.stderr, os.environ
        SCORE_HOST = os.environ.get('SCORE_HOST')
        SCORE_URI = os.environ.get('SCORE_URI')
        SCORE_PORT = os.environ.get('SCORE_PORT')
        url = 'http://{0}:{1}{2}'.format(SCORE_HOST,SCORE_PORT,SCORE_URI)
        SCORE_API_KEY = os.environ.get('SCORE_API_KEY')
        headers = {
            'SCORE_KEY': SCORE_API_KEY
        }
        print >>sys.stderr, url
        try:
            res = requests.post(url, {"user_id": 1, "value": 1}, headers=headers)
            status = res.status_code
        except Exception as e:
            status = 400
        user = BookingUser.objects.get(pk=1)
        print >>sys.stderr, user.bonus_point
        return JsonResponse({'room': rooms}, status=status)

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
                return JsonResponse({'error': 'Failed'}, status=400)
        else:
            print >>sys.stderr, booking_data.errors
            return JsonResponse({'error': dict(booking_data.errors.items())})
        return JsonResponse({'room': '1'})
