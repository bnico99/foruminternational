from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from booking.forms import BookingForm
from . import views

app_name = 'booking'
urlpatterns = [
    url(r'^calendar$', views.CalendarView.as_view(), name='calendar'),
    url(r'^event/edit/(?P<event_datum>[\d-]+)/(?P<event_time>[\d:]+)/(?P<event_dur>\d+)$', views.event,
        name='event_edit'),
    url(r'^ajax/validate_price/$', views.calculate_price_ajax, name='validate_price'),
    url(r'^confirmation/', views.book_confirm, name='confirm'),
    url(r'^waitinglist/(?P<date>[\d-]+)$', views.request_waiting_list_addition, name='request_waitinglist'),
]
urlpatterns += staticfiles_urlpatterns()
