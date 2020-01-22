from booking.models import WeeklyBookingAdminForm
from .models import Booking, Blocker, CancelledBooking, WaitingList, WeeklyBooking
from django.contrib import admin
import string


# this clas represents an alphabetical filter for the last names of the website users
class AlphabetFilter(admin.SimpleListFilter):
    title = 'Nachname'
    parameter_name = 'alphabet'

    # this method creates the different categories for the filter, i.e. A,B,C,..
    def lookups(self, request, model_admin):
        abc = list(string.ascii_lowercase)
        return ((c.upper(), c.upper()) for c in abc)

    # this method queries for users whos last name start with the given letter
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(author__last_name__startswith=self.value())


# this class is used to display the cancelled bookings to the admin
class CancelledBookingAdmin(admin.ModelAdmin):
    # this is the information that the admin will see about cancelled bookings
    list_display = ('start_datetime', 'end_datetime', 'booking_time', 'cancellation_time', 'author',
                    'rent', 'rent_was_paid', 'rent_has_to_be_paid')

    # this is the information that the admin will not be allowed to change about the cancelled bookings
    readonly_fields = ('start_datetime', 'end_datetime', 'booking_time', 'cancellation_time', 'author',
                       'rent', 'rent_was_paid', 'rent_has_to_be_paid')

    # these are the filters that the admin can use in order to filter the cancelled bookings
    list_filter = ('start_datetime', 'end_datetime', 'booking_time', 'cancellation_time',
                   'rent', 'rent_was_paid', 'rent_has_to_be_paid', AlphabetFilter)


admin.site.register(Booking)
admin.site.register(Blocker)
admin.site.register(CancelledBooking, CancelledBookingAdmin)


# this class represents a filter that will be used to filter the bookings by number of people attending the event
class PersonsForEventFilter(admin.SimpleListFilter):
    title = 'Personenanzahl'
    parameter_name = 'number_people'

    # this method specifies the possible categories for the filter, i.e. less that 50 people and more that or equal to 50 people
    def lookups(self, request, model_admin):
        return (("<50", "bis 50"),
                (">=50", "ab 50"))

    # this method queries for bookings to see if they fit the above described categories
    def queryset(self, request, queryset):
        if self.value() == '<50':
            return queryset.filter(number_people__lt=50)
        if self.value() == '>=50':
            return queryset.filter(number_people__gte=50)


# this class is used to display the bookings to the admin
class BookingAdmin(admin.ModelAdmin):
    # this is the information that the admin will see about bookings
    list_display = (
    'id', 'date', 'get_author', 'start_time', 'duration', 'student', 'number_people', 'refrigerator', 'confirmed',
    'occasion',
    'rent_paid', 'contract_signed', 'deposit_paid', 'deposit_refunded', 'requested_inspection',)

    # these are the filters that the admin can use in order to filter the bookings
    list_filter = (
    'confirmed', 'rent_paid', 'contract_signed', 'deposit_paid', 'deposit_refunded', 'requested_inspection',
    'duration', 'start_time', PersonsForEventFilter, 'student', 'date', 'refrigerator', AlphabetFilter,)

    # this method is used to get the last name of the author of a booking, in order to display it to the admin
    def get_author(self, instance):
        return instance.author.profile.last_name

    get_author.short_description = 'Kunde'


admin.site.unregister(Booking)
admin.site.register(Booking, BookingAdmin)


# this class is used to display the blockers to the admin
class BlockerAdmin(admin.ModelAdmin):
    # this is the information that the admin will see about blockers
    list_display = ('date', 'start_time', 'duration',)

    # these are the filters that the admin can use in order to filter the blockers, e.g. by duration
    list_filter = ('date', 'duration', 'start_time')


admin.site.unregister(Blocker)
admin.site.register(Blocker, BlockerAdmin)


# this class is used to display the waiting lists to the admin
class WaitingListAdmin(admin.ModelAdmin):
    # this is the information that the admin will see about waiting lists
    list_display = ('date', 'get_waiting')

    # this is the information that the admin will not be allowed to change about the waiting lists
    list_filter = ('date',)

    # these are the filters that the admin can use in order to filter the existing waiting lists, e.g. by date
    readonly_fields = ('date', 'waiting',)

    # this method is used to get the first and last names of the people waiting for a certain date
    def get_waiting(self, instance):
        wait = ""
        for customer in instance.waiting.all():
            wait += customer.first_name + " " + customer.last_name + ", "
        return wait

    get_waiting.short_description = "Warteliste"


admin.site.register(WaitingList, WaitingListAdmin)


# this class represents a filter that will be used to filter the weekly bookings by weekday
class WeekDayFilter(admin.SimpleListFilter):
    title = 'Wochentag'
    parameter_name = 'start_datetime'

    # this method creates the different categories for the filter, i.e. Monday, Tuesday, ...
    def lookups(self, request, model_admin):
        return (("2", "Montag"),
                ("3", "Dienstag"),
                ("4", "Mittwoch"),
                ("5", "Donnerstag"),
                ("6", "Freitag"),
                ("7", "Samstag"),
                ("1", "Sonntag"),
                )

    # this method queries for weekly bookings to see if they fit the above described categories
    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(start_datetime__week_day=1)
        if self.value() == '2':
            return queryset.filter(start_datetime__week_day=2)
        if self.value() == '3':
            return queryset.filter(start_datetime__week_day=3)
        if self.value() == '4':
            return queryset.filter(start_datetime__week_day=4)
        if self.value() == '5':
            return queryset.filter(start_datetime__week_day=5)
        if self.value() == '6':
            return queryset.filter(start_datetime__week_day=6)
        if self.value() == '7':
            return queryset.filter(start_datetime__week_day=7)

# this class is used to display the weekly bookings to the admin
class WeeklyBookingAdmin(admin.ModelAdmin):

    # this is the information that the admin will see about weekly bookings
    list_display = ('get_weekday', 'get_start_time', 'get_end_time', 'get_start_date', 'get_end_date', 'exception_first',
    'exception_second', 'exception_third', 'exception_forth', 'exception_fifth')

    # these are the filters that the admin can use in order to filter the existing weekly bookings, e.g. by start time
    list_filter = (WeekDayFilter, 'start_datetime', 'end_datetime')

    #this is the form that the admin will use to create new weekly bookings
    form = WeeklyBookingAdminForm


    # the following methods are used to get and format information about the weekly meetings in order to disaply as much information
    # about them as possible to the admin
    def get_start_time(self, instance):
        return instance.start_datetime.strftime("%H:%M")

    get_start_time.short_description = "Startzeit"

    def get_start_date(self, instance):
        return instance.start_datetime.strftime("%d.%m.%Y")

    get_start_date.short_description = "erster Termin"

    def get_end_time(self, instance):
        return instance.end_datetime.strftime("%H:%M"),

    get_end_time.short_description = "Endzeit"

    def get_end_date(self, instance):
        return instance.end_datetime.strftime("%d.%m.%Y")

    get_end_date.short_description = "letzter Termin"

    get_end_date.short_description = "letzter Termin"


    #this method is used to get the day of the weekly booking
    def get_weekday(self, instance):
        day = instance.start_datetime.weekday()

        if day == 0:
            day_name = "Montag"

        if day == 1:
            day_name = "Dienstag"

        if day == 2:
            day_name = "Mittwoch"

        if day == 3:
            day_name = "Donnerstag"

        if day == 4:
            day_name = "Freitag"

        if day == 5:
            day_name = "Samstag"

        if day == 6:
            day_name = "Sonntag"

        return day_name

    get_weekday.short_description = "Wochentag"


admin.site.register(WeeklyBooking, WeeklyBookingAdmin)
