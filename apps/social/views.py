# Create your views here.
from django.http import JsonResponse

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
