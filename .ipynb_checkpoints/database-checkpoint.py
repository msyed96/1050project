# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import logging
import pymongo
import pandas as pd
import expiringdict

import utils

client = pymongo.MongoClient()
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'db.log')
RESULT_CACHE_EXPIRATION = 3000           # seconds


def upsert_city(df):
    """
    Update MongoDB database `cityhallpower` and collection `cityhallpower` with the given `DataFrame`.
    """
    db = client.get_database("cityhallpower")
    collection = db.get_collection("cityhallpower")
    update_count = 0
    for record in df.to_dict('records'):
        result = collection.replace_one(
            filter={'DateTime_Measured': record['DateTime_Measured']},    # locate the document if exists
            replacement=record,                         # latest document
            upsert=True)                                # update if exists, insert if not
        if result.matched_count > 0:
            update_count += 1
    logger.info("rows={}, update={}, ".format(df.shape[0], update_count) +
                "insert={}".format(df.shape[0]-update_count))



def fetch_all_city():
    db = client.get_database("cityhallpower")
    collection = db.get_collection("cityhallpower")
    ret = list(collection.find())
    logger.info(str(len(ret)) + ' documents read from the db')
    return ret


_fetch_all_city_as_df_cache = expiringdict.ExpiringDict(max_len=1,
                                                       max_age_seconds=RESULT_CACHE_EXPIRATION)


def fetch_all_city_as_df(allow_cached=False):
    """Converts list of dicts returned by `fetch_all_bpa` to DataFrame with ID removed
    Actual job is done in `_worker`. When `allow_cached`, attempt to retrieve timed cached from
    `_fetch_all_bpa_as_df_cache`; ignore cache and call `_work` if cache expires or `allow_cached`
    is False.
    """
    def _work():
        data = fetch_all_city()
        if len(data) == 0:
            return None
        df = pd.DataFrame.from_records(data)
        df.drop('_id', axis=1, inplace=True)
        return df

    if allow_cached:
        try:
            return _fetch_all_city_as_df_cache['cache']
        except KeyError:
            pass
    ret = _work()
    _fetch_all_city_as_df_cache['cache'] = ret
    return ret

if __name__ == '__main__':
    print(fetch_all_city_as_df())
   

