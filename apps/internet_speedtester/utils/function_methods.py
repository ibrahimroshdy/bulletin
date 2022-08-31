import os

import django

# Setup django to be able to access the settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from .abstract_speeedtest import AbstractSpeedtest


def process_speedtest_test():
    """

    :return:
    """
    abstract_speedtest = AbstractSpeedtest()
    speedtest_res = abstract_speedtest.get_speedtest()
    best = abstract_speedtest.get_best_server()
    servers = abstract_speedtest.get_servers()
    client = abstract_speedtest.get_client()

    return speedtest_res, best, servers, client
