import calendar
from datetime import datetime
from datetime import time, date
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views import generic
from booking.forms import BookingForm
from .models import Booking, timeslot_available, calculate_price, get_day_type, str_to_bool, Event
from user_account.models import Profile
from .utils import Calendar, get_monthname
from booking.models import WaitingList



class CalendarView(generic.ListView):
    model = Booking
    template_name = 'booking/book.html'

    def get_context_data(self, **kwargs):
        """
        Return the context that will be displayed in the template
        """
        context = super().get_context_data(**kwargs)

        # use today's month for the calendar
        d = get_date(self.request.GET.get('month', None))

        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['prev_month_name'] = prev_month_name(d)
        context['next_month'] = next_month(d)
        context['next_month_name'] = next_month_name(d)
        context['date_in_past_month'] = is_past(d)
        context['six_month_ahead'] = six_month_ahead(d)
        context['dur_chosen'] = False

        #  called when user chose datum in calendar
        if self.request.GET.get('datum'):
            date = self.request.GET.get('datum')
            datum = datetime.strptime(date, '%Y-%m-%d')
            context['datum'] = datum
            context['durationlist'] = get_durationlist(datum)

        # called when user chose duration
        if self.request.GET.get('dur'):
            date = self.request.GET.get('datum')
            datum = datetime.strptime(date, '%Y-%m-%d')
            dur = self.request.GET.get('dur')
            context['dur'] = dur
            context['free_timeslots'] = get_free_timeslots(datum, dur)
            context['blocked_timeslots'] = get_blocked_timeslots(datum)
            context['dur_chosen'] = True

        return context


def prev_month(d):
    """
    Return the previous month as string for url
    """
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def prev_month_name(d):
    """
    Return the name of the previous month
    """
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = prev_month.month
    return get_monthname(month)


def next_month(d):
    """
    Return the next month as string for url
    """
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def next_month_name(d):
    """
    Return the name of the next month
    """
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = next_month.month
    return get_monthname(month)


def get_date(req_day):
    """
    Return datetime format of either req_day or today
    """
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today().date()


def event(request, event_datum, event_time, event_dur):
    """
    Render event.html with BookingForm.
    If form is submitted redirect to a confirmation page
    """
    form = BookingForm(request.POST or None)
    yearstr = datetime.strptime(event_datum, '%Y-%m-%d')
    form.fields['date'].initial = yearstr.strftime('%Y-%m-%d')
    form.fields['start_time'].initial = event_time
    form.fields['duration'].initial = event_dur

    if request.POST and form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()

        return HttpResponseRedirect(reverse('booking:confirm'))

    return render(request, 'booking/event.html', {'form': form})


def book_confirm(request):
    """
    Render the confirmation page
    """
    return render(request, 'booking/book_confirm.html')


def get_free_timeslots(datum, dur):
    """
    Calculate free timeslots between 8 and 23 o'clock.
    :param datum: the given date
    :param dur: the given duration
    :return: a dictionary with start and endtime
    """
    timelist = dict()
    for x in range(8, 24):
        start = time(x, 00)
        starttime = datetime.combine(datum, start)
        endtime = starttime + timedelta(hours=int(dur))
        if timeslot_available(starttime, endtime):
            timelist[starttime.strftime('%H:%M')] = endtime.strftime('%H:%M')
    return timelist


def get_blocked_timeslots(datum):
    """
    Get blocked timeslots.
    :param datum: the given date
    :return: a dictionary with start and endtime
    """
    eventlist = Event.objects.filter(date__year=datum.year, date__month=datum.month,
                                     start_datetime__day=datum.day).order_by('start_time')
    eventlist_overnight = Event.objects.filter(date__year=datum.year, date__month=datum.month,
                                               end_datetime__day=datum.day)
    blocked_timeslots = dict()
    for event in eventlist_overnight:
        if (event.end_datetime.strftime('%H:%M') > time(8, 0, 0).strftime('%H:%M')) & (
                event.start_datetime.day != event.end_datetime.day):
            blocked_timeslots[time(8, 0, 0).strftime('%H:%M')] = event.end_datetime.strftime('%H:%M')

    for event in eventlist:
        if (event.end_datetime.day != event.start_datetime.day):
            blocked_timeslots[event.start_datetime.strftime('%H:%M')] = time(0, 0, 0).strftime('%H:%M')
        else:
            blocked_timeslots[event.start_datetime.strftime('%H:%M')] = event.end_datetime.strftime('%H:%M')
    return blocked_timeslots


def calculate_price_ajax(request):
    """
    Calculates the price of the booking from ajax call
    :return: JSONResponse with the calculated price
    """
    number_people = request.GET.get('number_people', None)
    student = request.GET.get('student', None)
    duration = request.GET.get('duration', None)
    start_time = datetime.strptime(request.GET.get('start_time', None), '%H:%M')
    start_date = datetime.strptime(request.GET.get('date', None), '%Y-%m-%d')
    start_datetime = datetime.combine(start_date, start_time.time())
    end_datetime = start_datetime + timedelta(hours=int(duration))
    refrigerator = request.GET.get('refrigerator', None)
    validate_input(start_date, int(duration), int(number_people))
    price = calculate_price(start_date, str_to_bool(student), int(duration), int(number_people), end_datetime,
                            refrigerator)
    data = {
        'price': price
    }
    return JsonResponse(data)


def validate_input(start_date, duration, number_people):
    if get_day_type(start_date) == 'WEEKDAY' and duration not in [3, 6, 12]:
        raise ValidationError(_('An Wochentagen ist nur eine 3-,6- oder 12-stündige Buchung möglich.'),
                              'invalid_duration')
    elif get_day_type(start_date) == 'WEEKEND' and duration not in [12, 24]:
        raise ValidationError(_('An Wochenenden ist nur eine 12- oder 24-stündige Buchung möglich.'),
                              'invalid_duration')

    if number_people <= 0:
        raise ValidationError(_('Die Anzahl erscheinender Personen muss größer als 0 sein.'), 'invalid_people_num')


def get_durationlist(datum):
    """
    Calculates possible durations (3,6,12 on weekdays and 12,24 on weekends)
    :param datum: the given date
    :return: a list with possible durations as integer
    """
    if get_day_type(datum) == "WEEKDAY":
        durationlist = list()
        for dur in [3, 6, 12]:
            if not len(get_free_timeslots(datum, dur)) == 0:
                durationlist.append(dur)
        return durationlist
    else:
        durationlist = list()
        for dur in [12, 24]:
            if not len(get_free_timeslots(datum, dur)) == 0:
                durationlist.append(dur)
        return durationlist


def is_past(datum):
    """
    Checks whether or not the given date is in the past (including today)
    :param datum: the given date
    :return: bool
    """
    if datum == date.today():
        return True
    elif datum > date.today():
        return False
    else:
        return True


def six_month_ahead(datum):
    """
    Check whether the date given is (more than) six month ahead from today
    :param datum: the date to check
    :return: bool
    """
    return datum >= date.today() + relativedelta(months=+6)


def request_waiting_list_addition(request, date):
    """
    function used to request to be added to the waiting list for the chosen date date
    :param request: request used to call the function
    :return: adds the customer to the waiting list for the chosen date
    """
    user = request.user
    flag = (user.is_staff or user.is_superuser) #check if this is a staff member or a superuser
    event_date = datetime.strptime(date, '%Y-%m-%d')
    picked_date = event_date.date()
    pk = user.pk
    user = Profile.objects.get(pk=pk)

    if not flag: # if the user is not a staff member or a super user, add him to a waiting list and create one first if needed
        for wl in WaitingList.objects.all():
            if wl.date == picked_date: #if waiting list for this date already exists, then add this customer to it
                wl.waiting.add(user)
                return render(request, 'booking/waiting_list_addition.html')
        #there is no waiting list for this date yet, so create a new one first and then add customer to it
        new_wlist = WaitingList(date=picked_date)
        new_wlist.save()
        new_wlist.waiting.add(user)
    return render(request, 'booking/waiting_list_addition.html')



