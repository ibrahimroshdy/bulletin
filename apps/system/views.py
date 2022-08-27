"""
System application request management functions at views.py
"""

import datetime
import json
import platform

from django.http import HttpResponse
from uptime import uptime


def platform_specs(request):
    """
    Platform specs function that retreives platform information and returns information in a dict.
    :param request: WSGI GET request at '/platform_specs/
    :return: a multi-object dict containing platform specs as str
    """
    response = {
        'machine': platform.machine(),
        'platform': platform.platform(),
        'system': platform.system(),
        # 'architecture': platform.architecture(),
        # 'processor': platform.processor(),
        # 'release': platform.release(),
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


def machine_uptime(request):
    """
    Machine uptime function that converts the difference between time now and time the machine has been up.
    :param request: WSGI GET request at '/machine_uptime/
    :return: a single object dict with 'uptime' as a string converted from datetime object
    """
    response = {
        'uptime': str(datetime.timedelta(seconds=uptime()))

    }

    return HttpResponse(json.dumps(response), content_type="application/json")
