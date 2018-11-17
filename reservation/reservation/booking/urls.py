from django.conf.urls import url
from booking.views import BookRoomView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'v1/booking/', csrf_exempt(BookRoomView.as_view()))
]
