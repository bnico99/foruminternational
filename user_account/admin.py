from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'get_title', 'first_name', 'last_name', 'is_staff', 'get_date_of_birth',
                    'get_zip_code', 'get_city', 'get_street', 'get_house_number', 'get_phone',)

    list_select_related = ('profile',)

    def get_zip_code(self, instance):
        return instance.profile.zip_code

    get_zip_code.short_description = 'PLZ'

    def get_title(self, instance):
        return instance.profile.title

    get_title.short_description = 'Anrede'

    def get_city(self, instance):
        return instance.profile.city

    get_city.short_description = 'Ort'

    def get_house_number(self, instance):
        return instance.profile.house_number

    get_house_number.short_description = 'Hausnummer'

    def get_street(self, instance):
        return instance.profile.street

    get_street.short_description = 'Straße'

    def get_phone(self, instance):
        return instance.profile.phone

    get_phone.short_description = 'Telefonnummer'

    def get_date_of_birth(self, instance):
        return instance.profile.date_of_birth

    get_date_of_birth.short_description = 'Geburtsdatum'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
