import random
import telegram
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask, ClockedSchedule, SolarSchedule

from dtb.settings import DEBUG

from tgbot.models import User, UserActionLog
from tgbot.forms import BroadcastForm
from tgbot.handlers import utils

#from tgbot.tasks import broadcast_message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'first_name', 'last_name',
        'language_code', 'deep_link',
        'created_at', 'updated_at', "is_blocked_bot",
    ]
    list_filter = ["is_blocked_bot", "is_moderator"]
    search_fields = ('username', 'user_id')

    actions = ['broadcast']

    def invited_users(self, obj):
        return obj.invited_users().count()


# @admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'created_at']


# @admin.register(Arcgis)
class ArcgisAdmin(admin.ModelAdmin):
    list_display = ['location', 'city', 'country_code']


# @admin.register(UserActionLog)
class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'created_at']


admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(SolarSchedule)
