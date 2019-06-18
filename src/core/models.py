from django.db import models


class CallRecord(models.Model):
    START = 'start'
    END = 'end'
    RECORD_TYPE_CHOICES = (
        (START, 'Start'),
        (END, 'End')
    )

    call_id = models.PositiveIntegerField(
        help_text='Unique identifier for each call record pair'
    )
    record_type = models.CharField(
        max_length=5,
        choices=RECORD_TYPE_CHOICES,
        verbose_name='Record Type',
        help_text='Indicate if it\'s a call start or end record'
    )
    timestamp = models.DateTimeField(
        help_text='The timestamp of when the event occured'
    )
    source = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        help_text='The subscriber phone number that originated the call'
    )
    destination = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        help_text='The phone number receiving the call'
    )

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


class BillRecord(models.Model):
    bill = models.ForeignKey(
        'core.Bill',
        on_delete=models.CASCADE,
        related_name='records'
    )
    destination = models.CharField(
        max_length=11,
        help_text='The phone number receiving the call'
    )
    start_date = models.DateField(help_text='The date when the call started')
    start_time = models.TimeField(help_text='The time when the call started')
    duration = models.PositiveIntegerField(
        help_text='The call duration, in seconds'
    )  # In seconds
    price = models.FloatField(
        help_text='The call total price'
    )

    class Meta:
        verbose_name = "Bill Record"
        verbose_name_plural = "Bill Records"

    def __str__(self):
        return 'Record from bill {} - {}s - price: {}'.format(
            self.bill.id,
            self.duration,
            self.price
        )


class Bill(models.Model):
    telephone = models.CharField(
        max_length=11,
        help_text='The subscriber phone number'
    )
    period = models.DateField()

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Bills"
        unique_together = ['telephone', 'period']

    def __str__(self):
        return 'Bill {} from {} - {}'.format(
            self.id,
            self.telephone,
            self.period.strftime('%m-%Y')
        )
