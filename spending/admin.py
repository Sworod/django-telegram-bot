from django.contrib import admin

# Register your models here.
from spending.models import Spending, SpendingType


@admin.register(Spending)
class SpendingAdmin(admin.ModelAdmin):
    list_display = [ 'type', 'amount','created_at',]


@admin.register(SpendingType)
class SpendingTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'subtype']
