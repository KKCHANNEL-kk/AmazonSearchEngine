from math import prod
import calculate as cal
import store
import logging
import time
import logging.handlers
import os
from nltk.stem import SnowballStemmer
from operator import itemgetter
import pandas as pd


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

snowball_stemmer = SnowballStemmer("english")


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


def handle_query(query, field):
    '''
    处理查询语句
    '''
    tf = info[field]['tf']
    df = info[field]['df']
    N = info[field]['N']

    query_tokens = cal.tokenize(query)
    index_lists = [info[field]['index']
                   [snowball_stemmer.stem(token)] for token in query_tokens]
    mul_ints_ans = cal.multiIntersect(index_lists)
    matrix = cal.tfidf_matrix('long', mul_ints_ans, tf, df, N)
    q_vec = cal.get_query_tfidf(query_tokens, df, N)

    results = []
    v1 = list(sorted(q_vec.items(), key=itemgetter(0), reverse=False))
    for doc_asin, vec_candidate in matrix.items():
        v2 = list(sorted(vec_candidate.items(),
                  key=itemgetter(0), reverse=False))
        results.append((doc_asin, cal.cosine_similarity(v1, v2)))

    # TODO get Top 5
    asin_results = sorted(results, key=lambda x: x[1], reverse=True)
    prod_result = []
    for result in asin_results[:5]:
        asin = result[0]
        prod = meta[meta['asin'] == asin].to_dict('records')[0]

        prod_info = {}
        prod_info['asin'] = asin
        prod_info['corr'] = result[1]
        prod_info['title'] = prod['title']
        print('prod:{}'.format(prod))
        prod_info['feature'] = prod['feature']
        prod_info['description'] = prod['description']
        prod_info['price'] = prod['price']
        if len(prod['imageURL'])!=0:
            prod_info['img'] = prod['imageURL'][0]
        prod_info['review'] = {}
        prod_info['review']['text'] = reviews[asin]['reviews'][0]['reviewText']
        prod_info['review']['vote'] = reviews[asin]['reviews'][0]['vote']
        prod_info['review']['score'] = reviews[asin]['score']

        prod_result.append(prod_info)

    return prod_result
