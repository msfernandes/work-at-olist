from django.db.models.signals import post_save
from django.dispatch import receiver
from core import models


@receiver(post_save, sender=models.CallRecord)
def check_call_ended(sender, instance, created, **kwargs):
    if created:
        pair = models.CallRecord.objects.filter(
            call_id=instance.call_id,
        ).exclude(record_type=instance.record_type)

        if pair.count() > 0:
            pair = pair[0]
