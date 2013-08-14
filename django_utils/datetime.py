from django.template import defaultfilters
from django.utils.timezone import get_current_timezone, make_naive

def format_like_template(datetime_value):
    return defaultfilters.date(make_naive(datetime_value, get_current_timezone()), 'F j, Y, P')
