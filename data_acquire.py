"""
Boston City hall and Library power consumption.
"""
import time
import sched
import pandas
import logging
import requests
from io import StringIO

import utils
from database import upsert_bpa


BPA_SOURCE = 'https://og-production-open-data-bostonma-892364687672.s3.amazonaws.com/resources/f123e65d-dc0e-4c83-9348-ed46fec498c0/tmpke4utrxy.csv?Signature=UAjyK0cDg%2BFiT22SGIeHlr12eQ8%3D&Expires=1575837619&AWSAccessKeyId=AKIAJJIENTAPKHZMIPXQ'
MAX_DOWNLOAD_ATTEMPT = 5
DOWNLOAD_PERIOD = 10         # second
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'data.log')


def download_bpa(url=BPA_SOURCE, retries=MAX_DOWNLOAD_ATTEMPT):
    """Returns BPA text from `BPA_SOURCE` that includes power loads and resources
    Returns None if network failed
    """
    print('hi')
    text = None
    for i in range(retries):
        try:
            req = requests.get(url, timeout=0.5)
            req.raise_for_status()
            text = req.text
        except requests.exceptions.HTTPError as e:
            logger.warning("Retry on HTTP Error: {}".format(e))
    if text is None:
        logger.error('download_bpa too many FAILED attempts')
    return text


def filter_bpa(text):
    """Converts `text` to `DataFrame`, removes empty lines and descriptions
    """
    print('hello')
    # use StringIO to convert string to a readable buffer
    df = pandas.read_csv(StringIO(text))
    
    return df


def update_once():
    print('boop')
    t = download_bpa()
    df = filter_bpa(t)
    upsert_bpa(df)


def main_loop(timeout=DOWNLOAD_PERIOD):
    scheduler = sched.scheduler(time.time, time.sleep)

    def _worker():
#         try:
          update_once()
#         except Exception as e:
#             logger.warning("main loop worker ignores exception and continues: {}".format(e))
#         scheduler.enter(timeout, 1, _worker)    # schedule the next event

    scheduler.enter(0, 1, _worker)              # start the first event
    scheduler.run(blocking=True)


if __name__ == '__main__':
    main_loop()


