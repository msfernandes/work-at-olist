from datetime import datetime
from constance import config
from math import floor


def call_duration(start_timestamp, end_timestamp):
    duration = end_timestamp - start_timestamp
    return duration.seconds


def check_tariff(timestamp):
    standard_upper_limit = datetime(
        timestamp.year,
        timestamp.month,
        timestamp.day,
        22,
        0
    )
    standard_lower_limit = datetime(
        timestamp.year,
        timestamp.month,
        timestamp.day,
        6,
        0
    )
    upper_diff = standard_upper_limit - timestamp
    lower_diff = timestamp - standard_lower_limit

    if upper_diff.total_seconds() >= 0 and lower_diff.total_seconds() >= 0:
        return 'standard'
    else:
        return 'reduced'


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


def calculate_tariff_time(tariff, timestamp, initial_record):
    if initial_record:
        limit = datetime(
            timestamp.year,
            timestamp.month,
            timestamp.day,
            TARIFFS[tariff]['upper_hour_limit'],
            0
        )
        diff = limit - timestamp
    else:
        limit = datetime(
            timestamp.year,
            timestamp.month,
            timestamp.day,
            TARIFFS[tariff]['lower_hour_limit'],
            0
        )
        diff = timestamp - limit

    return diff.total_seconds()


def calculate_time_by_tariff(start_timestamp, end_timestamp):
    start_tariff = check_tariff(start_timestamp)
    end_tariff = check_tariff(end_timestamp)
    duration = call_duration(start_timestamp, end_timestamp)

    time_by_tariff = {'standard': 0, 'reduced': 0}

    if start_tariff == end_tariff:
        time_by_tariff[start_tariff] = duration
    else:
        time_by_tariff[start_tariff] = calculate_tariff_time(
            start_tariff,
            start_timestamp,
            True
        )
        time_by_tariff[end_tariff] = duration - time_by_tariff[start_tariff]
    return time_by_tariff


def get_call_price(start_timestamp, end_timestamp):
    time_by_tariff = calculate_time_by_tariff(start_timestamp, end_timestamp)
    end_tariff = check_tariff(end_timestamp)
    price = getattr(config, TARIFFS[end_tariff]['standing_charge'])

    price += floor(time_by_tariff['reduced'] / 60) * getattr(
        config,
        TARIFFS['reduced']['minute_charge']
    )

    price += floor(time_by_tariff['standard'] / 60) * getattr(
        config,
        TARIFFS['standard']['minute_charge']
    )

    return price
