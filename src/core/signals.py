from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from core import models, pricing


@receiver(post_save, sender=models.CallRecord, dispatch_uid='process_records')
def process_call_records(sender, instance, created, **kwargs):
    pair = models.CallRecord.objects.filter(
        call_id=instance.call_id,
    ).exclude(record_type=instance.record_type)

    if created and pair.count() > 0:
        if instance.record_type == models.CallRecord.START:
            start_record = instance
            end_record = pair[0]
        else:
            start_record = pair[0]
            end_record = instance

        price = pricing.Pricing(
            start_record.timestamp,
            end_record.timestamp
        )
        bill = models.Bill.objects.get_or_create(
            telephone=start_record.source,
            period=datetime(
                end_record.timestamp.year,
                end_record.timestamp.month,
                1,
            ).date()
        )[0]
        models.BillRecord.objects.create(
            bill=bill,
            destination=start_record.destination,
            start_date=start_record.timestamp.date(),
            start_time=start_record.timestamp.time(),
            duration=price.call_duration(),
            price=price.call_price()
        )
