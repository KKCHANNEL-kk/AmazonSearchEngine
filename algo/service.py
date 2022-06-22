import calculate as cal
import store
import logging
import time
import logging.handlers
import os

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logger = logging.getLogger(__file__)

# Console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logger.addHandler(console)

# File
file_handler = logging.FileHandler(
    '{}/log/service_{}.log'.format(os.getcwd(), time.strftime('%Y%m%d', time.localtime())))
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

logger.info('start')

# TODO tf-idf缓存层

doc_fields = ['title', 'feature', 'description', 'summary', 'reviewText']
info = {}
meta = None
reviews = None


def start_service():
    global info
    for doc_field in doc_fields:
        info[doc_field] = store.load_field_cache(doc_field)
        logger.info('{} init finished'.format(doc_field))
    global meta
    global reviews
    # meta = store.load_meta_json('data/meta_Gift_Cards.json')
    # logger.info('meta init finished')
    # reviews = store.load_reviews_json('cache/goods_reviews.json')
    # logger.info('reviews init finished')
    meta = store.getDF('data/meta_Gift_Cards.json.gz')
    logger.info('meta init finished')
    reviews = store.load_meta_json('cache/goods_reviews.json')
    logger.info('reviews init finished')


def handle_query(query):
    '''
    处理查询语句
    '''
