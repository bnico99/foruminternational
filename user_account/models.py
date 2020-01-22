from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string

from info.models import MailEntry
from website import settings


class Profile(models.Model):
    """Representation of a user profile linked 1-to-1 to a Django user account"""
    title = models.CharField(max_length=30, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=40, blank=True)
    date_of_birth = models.DateField(null=True)
    signup_confirmation = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=5, null=True)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    house_number = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=15, null=True)
    data_privacy = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def send_visit_email_tutor(self):
        """Send mail requesting a inspection to the tutor mail address saved in database including all user info."""
        # construct and send email message to admin
        context = {
            'customer': self,
        }
        mail_text = render_to_string('mails/tutor_visit.txt', context=context)
        send_mail(
            'Besichtigungsanfrage FORUM international',
            mail_text,
            settings.EMAIL_HOST_USER,
            [MailEntry.objects.get(title='Tutor').mail],
            fail_silently=False,
        )
        return


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance).save()
        instance.profile.save()  # new
