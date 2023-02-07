# Create your views here.
from django.forms.models import model_to_dict
from django.http import JsonResponse

from .models import TweetSystemModel
from .utils import AbstractTweepy


def twt_get_trends(request):
    """
    Returns dicts with trends per location
    :param request:
    :return:
    """
    at = AbstractTweepy()
    response = at.get_trends()
    return JsonResponse(response, safe=False, status=200)


def twt_get_tweeting_status(request):
    """
    Returns TweetSystemModel model
    :param request:
    :return:
    """
    twt_system_status = TweetSystemModel.load()
    response = model_to_dict(twt_system_status)
    response.update({
        'created': twt_system_status.created,
        'modified': twt_system_status.modified
    })
    return JsonResponse(response, safe=False, status=200)
