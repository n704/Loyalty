from booking.models import *

def create_rooms():
    if Room.objects.count() == 0:
        room = Room.objects.create(name="Normal", available_amount=10, required_points=100)
        room = Room.objects.create(name="Economy Single Room", available_amount=10, required_points=150)
        room = Room.objects.create(name="Economy Double Room", available_amount=10, required_points=200)
        room = Room.objects.create(name="Luckory Single Room", available_amount=10, required_points=100)
        room = Room.objects.create(name="Luckory Double Room", available_amount=10, required_points=100)

def create_user():
    if BookingUser.objects.count() == 0:
        user = BookingUser.objects.create(
            name="John Doe",
            bonus_point=1000
        )
        user = BookingUser.objects.create(
            name="Jane Doe",
            bonus_point=1000
        )
        user = BookingUser.objects.create(
            name="Sam Doe",
            bonus_point=200
        )
        user = BookingUser.objects.create(
            name="Dena Doe",
            bonus_point=0
        )
