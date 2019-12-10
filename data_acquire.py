"""
Boston City hall power consumption.
"""
import time
import sched
import pandas
import logging
import requests
from io import StringIO

import utils
from database import upsert_city


City_SOURCE = 'https://data.boston.gov/dataset/1b894599-21ff-478f-937d-653954977951/resource/f123e65d-dc0e-4c83-9348-ed46fec498c0/download/tmpm6_yf0qo.csv'
MAX_DOWNLOAD_ATTEMPT = 5
DOWNLOAD_PERIOD = 14400         # second
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'data.log')


def download_data(url=City_SOURCE, retries=MAX_DOWNLOAD_ATTEMPT):
    """Returns data text from `data_SOURCE` that includes datetime and total power usage
    Returns None if network failed
    """
    text = None
    for i in range(retries):
        try:
            req = requests.get(url, timeout=0.5)
            req.raise_for_status()
            text = req.text
        except requests.exceptions.HTTPError as e:
            logger.warning("Retry on HTTP Error: {}".format(e))
    if text is None:
        logger.error('download_data too many FAILED attempts')
    return text


def filter_data(text):
    """Converts `text` to `DataFrame`, removes empty lines and descriptions
    """
    # use StringIO to convert string to a readable buffer
    df = pandas.read_csv(StringIO(text))
    
    return df


def update_once():
    city = download_data()
    df = filter_data(city)
    upsert_city(df)
 

def main_loop(timeout=DOWNLOAD_PERIOD):
    scheduler = sched.scheduler(time.time, time.sleep)

    def _worker():
#         try:
          update_once()
        except Exception as e:
            logger.warning("main loop worker ignores exception and continues: {}".format(e))
        scheduler.enter(timeout, 1, _worker)    # schedule the next event

    scheduler.enter(0, 1, _worker)              # start the first event
    scheduler.run(blocking=True)


if __name__ == '__main__':
    main_loop()


