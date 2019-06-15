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


class BillRecord(models.Model):
    bill = models.ForeignKey(
        'core.Bill',
        on_delete=models.CASCADE,
        related_name='records'
    )
    destination = models.CharField(max_length=11)
    start_date = models.DateField()
    start_time = models.TimeField()
    duration = models.PositiveIntegerField()  # In seconds
    price = models.FloatField()

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
    telephone = models.CharField(max_length=11)
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
