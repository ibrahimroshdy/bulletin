import os

import django

# Setup django to be able to access the settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from .abstract_speeedtest import AbstractSpeedtest


def process_speedtest_test():
    """
    Process the speedtest by creating a speedtest object, making a speedtest and returns the following data
    :return:
        speedtest_res: dictionary object with download, upload, lat and lon of the speedtest
        best: dict with best server conducting the speedtest
        servers: dict of lists of the matched servers
        client: single dictionary with information about the client making the test
    """
    abstract_speedtest = AbstractSpeedtest()
    speedtest_res = abstract_speedtest.get_speedtest()
    best = abstract_speedtest.get_best_server()
    servers = abstract_speedtest.get_servers()
    client = abstract_speedtest.get_client()

    return speedtest_res, best, servers, client
