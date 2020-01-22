from django.contrib import admin
from .models import FAQEntry, InfoText, FAQEntryEN, FAQEntryFR, PriceEntry, MailEntry


class InfoTextAdmin(admin.ModelAdmin):
    # Do not allow to edit title since it's an identifier
    readonly_fields = ('title',)

    # Do not allow to add new InfoTexts since they would (intentionally) not be displayed on the website
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PriceEntryAdmin(admin.ModelAdmin):
    # Do not allow to edit title since it's an identifier
    readonly_fields = ('title',)

    # Do not allow to add new PriceEntry since they would (intentionally) not have any effect
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MailEntryAdmin(admin.ModelAdmin):
    # Do not allow to edit title since it's an identifier
    readonly_fields = ('title',)

    # Do not allow to add new MailEntry since they would (intentionally) not have any effect
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(FAQEntry)
admin.site.register(FAQEntryEN)
admin.site.register(FAQEntryFR)
admin.site.register(InfoText, InfoTextAdmin)
admin.site.register(PriceEntry, PriceEntryAdmin)
admin.site.register(MailEntry, MailEntryAdmin)
