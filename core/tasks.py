"""
Timeloop based scheduled tasks
"""
import time
from datetime import timedelta

import timeloop
from django.conf import settings
from loguru import logger

from apps.internet_speedtester import tasks as internet_speedtester_tasks
from apps.social import tasks as social_tasks

tl = timeloop.Timeloop()
speedtester_interval_time = timedelta(minutes=settings.SPEEDTESTER_INTERVAL_TIME_MINS)
social_interval_time = timedelta(hours=settings.SOCIAL_INTERVAL_TIME_HRS)


@tl.job(interval=speedtester_interval_time)
def internet_speedtests():
    """
    Timeloop job defention that runs every specified speedtester_interval_time
    :return:
    """
    logger.info(f'Running internet_speedtest @ interval of: {speedtester_interval_time}')
    internet_speedtester_tasks.process_speedtest()


@tl.job(interval=social_interval_time)
def random_auto_tweeter_poster():
    """
    Timeloop job defention that runs every specified social_interval_time
    :return:
    """
    logger.info(f'Running autotweeter_poster @ interval of: {social_interval_time}')
    social_tasks.random_auto_tweeter_process()


if __name__ == "__main__":
    while True:
        try:
            tl.start()
        except RuntimeError:
            time.sleep(2000)
