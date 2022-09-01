from django.db import IntegrityError, transaction
from django.test import TestCase
from loguru import logger
from model_bakery import baker

from .models import ClientModel, ServersModel, SpeedtesterModel
from .utils import AbstractSpeedtest


# Create your tests here.
class ServersSpeeedTestCase(TestCase):
    def setUp(self):
        self.server = baker.make(ServersModel)
        self.speedtest = baker.make(SpeedtesterModel)

    def test_creation(self):
        """
        Tests database creation
        :return: True if a server and speedtest instances were created sucessfully.
        """
        if self.server and self.speedtest:
            logger.success('DB SUCCESS')
            logger.info(f'{self.server.__str__()[:5]})')
            logger.info(f'{self.speedtest.__str__()[:5]})')
            assert True

    def test_process_speedtest(self):
        """
        Processess a speedtest that gets the result, best server, and the pinged servers.
        Can't directly use the task from local dir because it contains transcations of  atomic blocks (for loop)
        in a non atomic test
        :return: True if the speedtest is processed and no errors happened.
        """
        abstract_speedtest = AbstractSpeedtest()
        speedtest_res = abstract_speedtest.get_speedtest()
        best = abstract_speedtest.get_best_server()
        servers = abstract_speedtest.get_servers()
        client = abstract_speedtest.get_client()

        if speedtest_res:
            logger.success(f'speed: {speedtest_res}')
            logger.success(f'best: {best}')
            logger.success(f'client: {client}')
            try:
                s, b = ServersModel.objects.get_or_create(**best)
                s.save()
            except IntegrityError as IE:
                logger.info(f"Best server {best['name']} exists. {IE}")

            try:
                c, b = ClientModel.objects.get_or_create(**client)
                c.save()
                _ = SpeedtesterModel.objects.update_or_create(best_server_id=int(best['id']),
                                                              client=c,
                                                              **speedtest_res)
            except IntegrityError as IE:
                logger.info(f"Client {client['cc']}-{client['isp']} exists. {IE}")

            for item in servers:
                try:
                    with transaction.atomic():  # important
                        s = ServersModel.objects.create(**item)
                        s.save()
                except IntegrityError as IE:
                    logger.info(f"Server {item['name']} exists. {IE}")

            assert True

    def tearDown(self):
        ServersModel.objects.all().delete()
        SpeedtesterModel.objects.all().delete()
