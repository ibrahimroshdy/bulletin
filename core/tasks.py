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

speedtester_interval_time = timedelta(hours=settings.SPEEDTESTER_INTERVAL_TIME_HRS)
text_tweet_interval_time = timedelta(minutes=settings.TEXT_TWEET_INTERVAL_TIME_MINS)
image_tweet_interval_time = timedelta(days=settings.IMAGE_TWEET_INTERVAL_TIME_DAYS)


@tl.job(interval=speedtester_interval_time)
def internet_speedtests():
    """
    Timeloop job defention that runs every specified speedtester_interval_time
    :return:None
    """
    logger.info(f'Running internet_speedtest @ interval of: {speedtester_interval_time}')
    internet_speedtester_tasks.process_speedtest()


@tl.job(interval=text_tweet_interval_time)
def random_auto_tweeter_poster():
    """
    Timeloop text based tweet job defention that runs every specified social_interval_time
    :return:None
    """
    logger.info(f'Running autotweeter_poster @ interval of: {text_tweet_interval_time}')
    social_tasks.random_auto_tweeter_process()


@tl.job(interval=image_tweet_interval_time)
def random_auto_image_tweeter_poster():
    """
    Timeloop image based tweet job defention that runs every specified social_interval_time
    :return: None
    """
    logger.info(f'Running auto_image_tweeter_poster @ interval of: {image_tweet_interval_time}')
    social_tasks.random_auto_image_tweeter_process()


if __name__ == "__main__":
    tl.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            tl.stop()
            break
