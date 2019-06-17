from rest_framework.exceptions import APIException


class InvalidPeriodFormat(APIException):
    status_code = 400
    default_detail = 'Invalid period format'
    default_code = 'bad request'
