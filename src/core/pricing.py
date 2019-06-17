from datetime import datetime, timedelta, timezone
from constance import config
from math import floor


class Pricing:
    TARIFFS = {
        'standard': {
            'standing_charge': 'STANDARD_STANDING_CHARGE',
            'minute_charge': 'STANDARD_MINUTE_CHARGE',
            'upper_hour_limit': 22,
            'lower_hour_limit': 6
        },
        'reduced': {
            'standing_charge': 'REDUCED_STANDING_CHARGE',
            'minute_charge': 'REDUCED_MINUTE_CHARGE',
            'upper_hour_limit': 6,
            'lower_hour_limit': 22
        }
    }

    def __init__(self, start_timestamp, end_timestamp):
        if start_timestamp > end_timestamp:
            start_timestamp, end_timestamp = end_timestamp, start_timestamp

        self.start = start_timestamp
        self.end = end_timestamp

    def call_price(self):
        durations = self.duration_by_tariff()
        end_tariff = self.check_tariff(self.end)
        price = getattr(config, self.TARIFFS[end_tariff]['standing_charge'])

        price += floor(durations['reduced'] / 60) * getattr(
            config,
            self.TARIFFS['reduced']['minute_charge']
        )

        price += floor(durations['standard'] / 60) * getattr(
            config,
            self.TARIFFS['standard']['minute_charge']
        )

        return round(price, 2)

    def call_duration(self):
        duration = self.end - self.start
        return duration.seconds

    def duration_by_tariff(self):
        start_tariff = self.check_tariff(self.start)
        end_tariff = self.check_tariff(self.end)
        duration = self.call_duration()

        durations = {'standard': 0, 'reduced': 0}

        if start_tariff == end_tariff:
            durations[start_tariff] = duration
        else:
            durations[start_tariff] = self.start_tariff_duration(start_tariff)
            durations[end_tariff] = duration - durations[start_tariff]
        return durations

    def start_tariff_duration(self, tariff):
        upper_limit = datetime(
            self.start.year,
            self.start.month,
            self.start.day,
            self.TARIFFS[tariff]['upper_hour_limit'],
            0,
            tzinfo=timezone.utc
        )
        lower_limit = datetime(
            self.start.year,
            self.start.month,
            self.start.day,
            self.TARIFFS[tariff]['lower_hour_limit'],
            0,
            tzinfo=timezone.utc
        )
        if tariff == 'reduced':
            lower_limit = lower_limit - timedelta(days=1)

        if lower_limit <= self.start < upper_limit:
            diff = upper_limit - self.start
        else:
            diff = self.start - self.start

        return diff.total_seconds()

    @classmethod
    def check_tariff(cls, timestamp):
        standard_upper_limit = datetime(
            timestamp.year,
            timestamp.month,
            timestamp.day,
            cls.TARIFFS['standard']['upper_hour_limit'] - 1,
            59,
            tzinfo=timezone.utc
        )
        standard_lower_limit = datetime(
            timestamp.year,
            timestamp.month,
            timestamp.day,
            cls.TARIFFS['standard']['lower_hour_limit'],
            0,
            tzinfo=timezone.utc
        )
        upper_diff = standard_upper_limit - timestamp
        lower_diff = timestamp - standard_lower_limit

        if upper_diff.total_seconds() >= 0 and lower_diff.total_seconds() >= 0:
            return 'standard'
        else:
            return 'reduced'
