from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from preferences.admin import PreferencesAdmin
from people.models import Teammate, PropsMessage, PeoplePreferences


class TeammateAdmin(MPTTModelAdmin):
    pass


class PropsMessageAdmin(admin.ModelAdmin):
    filter_horizontal = ("teammates_to",)


admin.site.register(Teammate, TeammateAdmin)
admin.site.register(PropsMessage, PropsMessageAdmin)
admin.site.register(PeoplePreferences, PreferencesAdmin)
