import os

import django
import speedtest
from django.db.utils import IntegrityError
from loguru import logger

# Setup django to be able to access the settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.internet_speedtester.models import ServersModel, SpeedtesterModel, ClientModel


class AbstractSpeedtest:
    def __init__(self):
        """
        A speedtest abstract class that iniates a speedtest method with catch clause for internet connection.
        """
        try:
            self.speedtester = speedtest.Speedtest(secure=True)
        except speedtest.ConfigRetrievalError as CRE:
            logger.error(f'No internet connection: {CRE}')
            raise SystemExit

    def get_speedtest(self):
        """
        Speed test getter that translates bits to megabits
        Concanate all items into a struct or 'dict' for return
        :return:
        A dict containting download, upload, lat, lat of conducted speed test
        """
        lat, lon = self.speedtester.lat_lon
        return {
            'download': round(self.speedtester.download() * 10 ** -6, 3),
            'upload': round(self.speedtester.upload() * 10 ** -6, 3),
            'lat': lat,
            'lon': lon
        }

    def get_client(self):
        """
        Speed test getter that returns the configuration of the client doing the speedtest itself
         only using speedtester.config['client']
        :return:
        A dict with client information
        """
        client = self.speedtester.config['client']
        entries_to_remove = ('isprating', 'rating', 'ispdlavg', 'ispulavg', 'loggedin')
        for k in entries_to_remove:
            client.pop(k, None)
        client['cc'] = client['country']
        client.pop('country')
        return client

    def get_best_server(self):
        """
        Get the best server that the speeed test is locked onto
        Added a new field called "Latency"
        :return:
        A dict with server information
        """
        best_server = self.speedtester.best
        return best_server

    def get_servers(self):
        """
        Converting a dict of list to a list of one item that is a list of dicts

        :return:
        List of server dicts that are within reach to the speedtest
        """
        servers = [i for i in [t for t in zip(*self.speedtester.servers.values())][0]]
        return servers


if __name__ == '__main__':
    abstract_speedtest = AbstractSpeedtest()
    speedtest_res = abstract_speedtest.get_speedtest()
    best = abstract_speedtest.get_best_server()
    servers = abstract_speedtest.get_servers()
    client = abstract_speedtest.get_client()

    try:
        s, b = ServersModel.objects.get_or_create(**best)
        s.save()
    except IntegrityError as IE:
        logger.info(f"Best server {best['name']} exists. {IE}")

    try:
        c, b = ClientModel.objects.get_or_create(**client)
        c.save()
        speedtest_object = SpeedtesterModel.objects.update_or_create(best_server_id=int(best['id']),
                                                                     client=c,
                                                                     **speedtest_res)
    except IntegrityError as IE:
        logger.info(f"Client {client['cc']}-{client['isp']} exists. {IE}")

    for item in servers:
        try:
            s = ServersModel.objects.create(**item)
            s.save()
        except IntegrityError as IE:
            logger.info(f"Server {item['name']} exists. {IE}")
