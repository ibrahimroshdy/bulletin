import os

import django
from celery import shared_task
from django.db.utils import IntegrityError
from loguru import logger

# Setup django to be able to access the settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.internet_speedtester.models import ServersModel, SpeedtesterModel, ClientModel
from apps.internet_speedtester.utils import AbstractSpeedtest


@shared_task
def process_speedtest():
    """
        A celery task that will be picked up.
        The task creates a speedtest instance and collects information of the conducted speedtest
        and adds them to the database using Django ORM.
    """
    # Create an instance of the AbstractSpeedtest class and results of the speedtest
    abstract_speedtest = AbstractSpeedtest()
    speedtest_res = abstract_speedtest.get_speedtest()
    best = abstract_speedtest.get_best_server()
    servers = abstract_speedtest.get_servers()
    client = abstract_speedtest.get_client()

    # Try to create a new entry in the ServersModel table for the best server, or retrieve it if it already exists
    try:
        s, b = ServersModel.objects.get_or_create(**best)
        s.save()
    except IntegrityError as _:
        # Log a message if the best server already exists in the database
        # logger.info(f"Best server {best['name']} exists. {IE}")
        pass

    # Try to create a new entry in the ClientModel table for the client, or retrieve it if it already exists
    try:
        c, b = ClientModel.objects.get_or_create(**client)
        c.save()

        # Create or update an entry in the SpeedtesterModel table for the speedtest result
        _ = SpeedtesterModel.objects.update_or_create(best_server_id=int(best['id']),
                                                      client=c,
                                                      **speedtest_res)

        # Log a success message if the speedtest has run successfully.
        logger.success(f"Speedtester ran successfully: {speedtest_res}")

    except IntegrityError as IE:
        # Log a message if the client already exists in the database
        logger.info(f"Client {client['cc']}-{client['isp']} exists. {IE}")

    # Loop through the list of servers and try to create a new entry in the ServersModel table for each server,
    # or retrieve it if it already exists
    for item in servers:
        try:
            s = ServersModel.objects.create(**item)
            s.save()
        except IntegrityError as _:
            # Log a message if the server already exists in the database
            # logger.info(f"Server {item['name']} exists. {IE}")
            pass


if __name__ == '__main__':
    process_speedtest()
