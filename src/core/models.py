from django.db import models


class CallRecord(models.Model):
    START = 'start'
    END = 'end'
    RECORD_TYPE_CHOICES = (
        (START, 'Start'),
        (END, 'End')
    )

    call_id = models.PositiveIntegerField()
    record_type = models.CharField(
        max_length=5,
        choices=RECORD_TYPE_CHOICES,
        verbose_name='Record Type'
    )
    timestamp = models.DateTimeField()
    source = models.CharField(max_length=11, null=True, blank=True)
    destination = models.CharField(max_length=11, null=True, blank=True)

    class Meta:
        verbose_name = "Call Record"
        verbose_name_plural = "Call Records"
        unique_together = ['record_type', 'call_id']

    def __str__(self):
        return 'Call {} - {} <{}>'.format(
            self.call_id,
            self.record_type,
            self.timestamp
        )
