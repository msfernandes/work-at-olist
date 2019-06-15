from django.contrib import admin
from core import models


@admin.register(models.CallRecord)
class CallRecordAdmin(admin.ModelAdmin):
    list_display = (
        'source',
        'destination',
        'call_id',
        'record_type',
        'timestamp',
    )
    list_filter = (
        'record_type',
        'timestamp'
    )


@admin.register(models.BillRecord)
class BillRecordAdmin(admin.ModelAdmin):
    list_display = (
        'bill',
        'destination',
        'start_date',
        'start_time',
        'duration',
        'price',
    )


@admin.register(models.Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = (
        'telephone',
        'period',
    )
    list_filter = (
        'period'
    )
