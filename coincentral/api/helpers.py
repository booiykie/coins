"""Helper functions."""
import time
from datetime import datetime, timedelta
from rest_framework.request import Request
from rest_framework.throttling import UserRateThrottle


DATE_FORMART = "%Y/%m/%d"

_TIME_OFFSET = (
    ('m', 'minutes'),
    ('h', 'hours'),
    ('M', 'months'),
    ('Y', 'years')
)

def string_date_to_datetime_format(date_str: str) -> datetime:
    """Conevert date string to datetime object."""
    _date = datetime.strptime(date_str, DATE_FORMART)
    return _date

def offset_resolver(_time_delta_offset: str, offset: int):
    """Resolving the required offset"""
    _offest_type = dict(_TIME_OFFSET).get(_time_delta_offset)
    if _time_delta_offset == 'h':
        _time_delta_offset = timedelta(hours=offset)
    elif _time_delta_offset == 'm':
        _time_delta_offset = timedelta(minutes=offset)
    elif _time_delta_offset == 'M':
        _time_delta_offset = timedelta(days=offset*30)
    elif _time_delta_offset == 'Y':
        _time_delta_offset = timedelta(days=offset*365)
    else:
        raise Exception(f"invalid time offset. Use h, m, M or Y.")
    return _time_delta_offset

def datetime_conversion(
    date_to_convert: str, time_offset: str, offset: int) -> str:
    """Convert given to epoch time with parsed offset."""
    _offset = offset_resolver(time_offset, offset)
    _time = time.mktime(
        (date_to_convert + _offset).timetuple()
    )
    return _time

def extract_coin_request_params(req: Request) -> list:
    """Extract params required for the 3rd party request/query."""
    _params = req.query_params.dict()
    _coin_id = _date = _currency = None
    _expected = ['coin_id', 'date', 'currency']
    _params_keys_set = set(_params.keys())
    _expected_params_set = set(_expected)
    key_validation = _expected_params_set & _params_keys_set
    if len(key_validation) < 3:
        raise Exception(
            f'Missing param: {set(_expected).difference(_params.keys())}')
    else:
        _coin_id = _params.get('coin_id')
        _currency = _params.get('currency')
        _date = string_date_to_datetime_format(_params.get('date'))
    return _coin_id, _date, _currency


class OncePerDayUserThrottle(UserRateThrottle):
    """Throttling class definition."""
    rate = '5/min'