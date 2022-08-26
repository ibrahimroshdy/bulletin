import json
import platform

from django.http import HttpResponse


# Create your views here.
from django.shortcuts import render


def platform_specs(request):
    response = {}
    machine = {'machine': platform.machine()}

    return HttpResponse(json.dumps(machine), content_type="application/json")
    # return render(request, 'includes/system/platform-specs_card.html', machine)
