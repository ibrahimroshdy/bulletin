"""
Timeloop based scheduled tasks
"""
from datetime import timedelta
import time
import timeloop
from loguru import logger

from apps.internet_speedtester import tasks

tl = timeloop.Timeloop()
interval_time = timedelta(minutes=15)


@tl.job(interval=interval_time)
def internet_speedtests():
    """
    Timeloop job defention that runs every specified time above
    :return:
    """
    logger.info(f'Running internet_speedtest @ interval of: {interval_time}')
    tasks.process_speedtest()


if __name__ == "__main__":
    while True:
        try:
            tl.start()
        except RuntimeError:
            time.sleep(2000)
