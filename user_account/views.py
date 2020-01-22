# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, update_session_auth_hash

from booking.models import Booking
from booking.models import CancelledBooking
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import datetime
from .forms import UserSignUpForm
import re
from booking.models import WaitingList
from django.utils.translation import ugettext_lazy as _

def usersignup(request):
    """
    the function generating the usersignup website called directly by user_account.urls
    :param request: the request used to call the website either a POST or a GET request
    :return: a render either of the account creation successfull site or the same site again if input was not valid
    """
    # check if the request is a POST request
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            # saving all given values in db
            user = form.save()
            # user is an instance of the django account structure saves the first and second name
            #  also hashes the password and saves the username
            user.refresh_from_db()
            user.profile.title = form.cleaned_data.get('title')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.zip_code = form.cleaned_data.get('zip_code')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.street = form.cleaned_data.get('street')
            user.profile.house_number = form.cleaned_data.get('house_number')
            user.profile.data_privacy = form.cleaned_data.get('data_privacy')

            # set the user on in active until the email is getting confirmed
            user.is_active = False
            user.save()
            user.profile.save()
            current_site = get_current_site(request)
            subject = _('Bitte bestätigen Sie Ihren "FORUM international"-Account.')

            # create message containing an activation link
            message = render_to_string('user_account/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            # send message to email adress given by user
            to_email = form.cleaned_data.get('email')

            email = EmailMessage(subject, message, to=[to_email])
            email.send()

            return render(request, 'user_account/registration_confirm.html')
        else:
            return render(request, 'user_account/signup.html', {'form': form})
    else:
        form = UserSignUpForm()
        return render(request, 'user_account/signup.html', {'form': form})


def activate_account(request, uidb64, token):
    """
    confirmes that the email of an user is valid and activates an user account
    :param request: the request used to call the site
    :param uidb64: the ID of the user to authenticate in the db
    :param token: the token sent to the user by usersignup()
    :return: a website containing a link to the log in website
    """
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        # the user data from db
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.profile.signup_confirmation = True  # user has now activated their account
        # login(request, user)
        return render(request, 'user_account/account_activated.html')
    else:
        return HttpResponse(
            'Ungültiger Aktivierungslink! ' + '<a href="/accounts/register/"> Hier geht es zur Registrierung.</a>')


def edit_user(request, pk):
    """
    validates and update the data the user wants to change
    :param request: the request used to call the site
    :param pk: the ID of the User in the db
    :return: a HTTPS response when the new data was valid and got saved successfully
    """
    user = User.objects.get(pk=pk)  # load user from db
    profile = user.profile  # load user profile
    form = UserSignUpForm(instance=profile)  # load the existing user data in the form also used for sign up
    # check if user is the authenticated user
    if request.user.id == user.id:
        if request.POST.__getitem__("speichern") == "f1":  # check which part got the form got changed
            # foreach possible change check if the input matches the pattern
            if re.match("\\D+", request.POST.__getitem__("first_name")):
                user.first_name = request.POST.__getitem__("first_name")
                profile.save()
                user.save()
            if re.match("\\D+", request.POST.__getitem__("last_name")):
                user.last_name = request.POST.__getitem__("last_name")
                profile.save()
                user.save()
            title = request.POST.__getitem__("title")
            if title == "Herr" or title == "Frau":
                profile.title = title
                profile.save()
            # assemble the date from the POST request
            day = request.POST.__getitem__("date_of_birth_day")
            month = request.POST.__getitem__("date_of_birth_month")
            year = request.POST.__getitem__("date_of_birth_year")
            # check if the given data is valid
            if re.match("\\d\\d?", day):
                if re.match("\\d{4}", year):
                    if re.match("\\d\\d?", month):
                        # create datetime object to save in db
                        birthdate = datetime.date(int(year), int(month), int(day))
                        profile.date_of_birth = birthdate.isoformat()
                        profile.save()
            return render(request, 'user_account/account_change.html')
        elif request.POST.__getitem__("speichern") == "f2":
            if re.match("\\D+", request.POST.__getitem__("street")):
                profile.street = request.POST.__getitem__("street")
            if re.match(".{1,11}", request.POST.__getitem__("house_number")):
                profile.house_number = request.POST.__getitem__("house_number")
            if re.match("\\d{5}", request.POST.__getitem__("zip_code")):
                profile.zip_code = request.POST.__getitem__("zip_code")
            if re.match("\\D+", request.POST.__getitem__("city")):
                profile.city = request.POST.__getitem__("city")
            profile.save()
            return render(request, 'user_account/account_change.html')
        elif request.POST.__getitem__("speichern") == "f3":
            """
            if re.match("\\w*\\@\\w*\\.\\w*", request.POST.__getitem__("email")):
                profile.email = request.POST.__getitem__("email")
                """
            if re.match("\\d+", request.POST.__getitem__("phone")):
                profile.phone = request.POST.__getitem__("phone")
            profile.save()
            return render(request, 'user_account/account_change.html')
        elif request.POST.__getitem__("speichern") == "f4":
            password = request.POST.__getitem__("password")
            password_confirm = request.POST.__getitem__("passwordconfirm")
            if password == password_confirm:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
                return HttpResponseRedirect(reverse('info:home'))
            else:
                return HttpResponseRedirect(reverse('myaccount_edit'))
            return HttpResponseRedirect(reverse('home'))

    return render(request, 'user_account/myaccount.html', {'form': form})


def myaccount_storno(request):
    """
    function gets called by myaccount_edit if the user wants to cancel an event
    its then creates a new instance of CancelledBooking and deletes the Booking which was cancelled
    :param request: the request used to call the site
    :return: the new render for the site will be created back in myaccount_edit
    """
    user = request.user
    isotime = request.GET.get('stornieren', '')
    # load the Event, which will be cancelled from the db
    toCancel = Booking.objects.get(start_datetime=isotime, author=user)

    # get end time of booking
    end_time = toCancel.end_datetime.date
    # remind customers in waiting list for this day
    for wl in WaitingList.objects.all():
        if wl.date == toCancel.date or wl.date == end_time:
            wl.remind_customers()  # remind customers in this waiting list
            break

    # create a new instance on CancelledBooking
    # this will also sends mails to staff and customer
    cancelled_booking = CancelledBooking.create(event_to_cancel=toCancel)
    cancelled_booking.save()

    # delete the Event from db
    toCancel.delete()


def myaccount_edit(request):
    """
    function is directly called from the user_accounts.urls it represents the 'My Account' site
    on the website
    :param request: the request used to call the site
    :return: the render of a website concluding from the users actions on the website
    """
    user = request.user
    event = Booking.objects.filter(author=user)
    stornieren = request.GET.get('stornieren', '0')
    # if the request is a POST method check which submit happened
    if request.method == "POST":
        # case the the user wants to cancel an event
        if request.POST.get('entry_storn'):
            # update the database and send all necessary emails
            myaccount_storno(request)
            # return to the my account site
            return render(request, 'user_account/storno_final.html')
        else:
            # user submitted new user information
            req = edit_user(request, user.pk)
            user.refresh_from_db()
            # return HttpResponseRedirect(reverse('user_account/account_change'))
            return req
    edit = request.GET.get('edit', '0')

    refunded = 0
    active = 0
    for entry in event:
        if entry.deposit_refunded:
            refunded += 1
        else:
            active += 1

    return render(request, "user_account/myaccount_edit.html",
                  {'event': event, 'edit': edit, 'stornieren': stornieren, 'noactive': (active == 0),
                   'norefunded': (refunded == 0)})
