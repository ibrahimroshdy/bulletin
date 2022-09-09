# Create your views here.

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Avg, Max, Min, StdDev
from django.http import JsonResponse

from . import models


def get_latest_speedtest(request):
    """
    Returns a single last speed test object
    :param request:
    :return:
    """
    try:
        speedtest_obj = models.SpeedtesterModel.objects.latest('created')
    except models.SpeedtesterModel.DoesNotExist as _:
        return JsonResponse({"message": "NOT FOUND"}, safe=False, status=404)

    response = {
        'created': speedtest_obj.created,
        'ip': speedtest_obj.client.ip,
        'isp': speedtest_obj.client.isp,
        'download': speedtest_obj.download,
        'upload': speedtest_obj.upload,
    }
    # response = serializers.serialize('json', [speedtest_obj])
    return JsonResponse(response, safe=False, status=200)


def get_lastest_week_internet_speedtests(request):
    """
    Calcultates latest week worth of data points (speed tests)
    :param request: HTTP request
    :return: json object as a list of dictionaries with the values ('created', 'download', 'upload')
    """
    speedtest_object = models.SpeedtesterModel.get_days_worth_speedtest_datapoints()

    response = json.dumps(list(speedtest_object), cls=DjangoJSONEncoder)
    return JsonResponse(json.loads(response), safe=False, status=200)


def get_week_internet_speedtest_agg(request):
    """
    Calcultates latest week worth of data points (speed tests) to minn, max, avg
    :param request:  HTTP request
    :return: json object with min, max , avg
    """
    speedtest_object = models.SpeedtesterModel.get_days_worth_speedtest_datapoints()

    agg_dict = speedtest_object.aggregate(Min('download'), Min('upload'),
                                          Max('download'), Max('upload'),
                                          Avg('download'), Avg('upload'),
                                          StdDev('download'), StdDev('upload'))

    response = {
        'order': ['download', 'upload'],
        'min': [agg_dict['download__min'], agg_dict['upload__min']],
        'max': [agg_dict['download__max'], agg_dict['upload__max']],
        'avg': [agg_dict['download__avg'], agg_dict['upload__avg']],
        'stddev': [agg_dict['download__stddev'], agg_dict['upload__stddev']],
    }
    return JsonResponse(response, safe=False, status=200)
