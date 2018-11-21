from django import forms

class RoomForm(forms.Form):
    room_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def clean_room_id(self):
        from booking.models import *
        room_id = self.cleaned_data['room_id']
        try:
            room = Room.objects.get(pk=room_id)
            self.cleaned_data['room'] = room
        except Room.DoesNotExist:
            raise forms.ValidationError("Invalid Room")
        return room_id

    def clean_user_id(self):
        from booking.models import *
        user_id = self.cleaned_data['user_id']
        try:
            user = BookingUser.objects.get(pk=user_id)
            self.cleaned_data['user'] = user
        except BookingUser.DoesNotExist:
            raise forms.ValidationError("Invalid User")
        return user_id
