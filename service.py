import math
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

    meta = store.getDF('data/meta_Gift_Cards.json.gz')
    logger.info('meta init finished')
    reviews = store.load_meta_json('cache/goods_reviews.json')
    logger.info('reviews init finished')


def handle_query(query, field):
    '''
    处理查询语句
    '''
    global meta
    global reviews
    global info

    tf = info[field]['tf']
    df = info[field]['df']
    N = info[field]['N']

    query_tokens = cal.tokenize(query)
    terms = [str(snowball_stemmer.stem(token)) for token in query_tokens]
    check_keys = info[field]['index'].keys()
    # 防止检索词不存在
    index_lists = []
    for term in terms:
        if term in check_keys:
            index_lists.append(info[field]['index'][term])
    if len(index_lists) == 0:
        return []

    mul_ints_ans = cal.multiIntersect(index_lists)
    if len(mul_ints_ans) == 0:
        return []

    doc_type = {'title': 'short', 'feature': 'short',
                'description': 'short', 'summary': 'long', 'reviewText': 'long'}
    matrix = cal.tfidf_matrix(doc_type[field], mul_ints_ans, tf, df, N)
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
    for result in asin_results[:10]:
        asin = result[0]
        prod = meta[meta['asin'] == asin].to_dict('records')[0]

        prod_info = {}
        prod_info['asin'] = asin
        prod_info['corr'] = result[1]
        prod_info['title'] = prod['title']
        # print('prod:{}'.format(prod))
        prod_info['feature'] = prod['feature']
        prod_info['description'] = prod['description']
        prod_info['price'] = prod['price']
        if len(prod['imageURLHighRes']) != 0:
            prod_info['img'] = prod['imageURLHighRes']

        # if field == 'reviewText':
        #     t = query_tokens[0]
        #     reviews_q = list(
        #         filter(lambda x: t in str(x['reviewText']), reviews[asin]['reviews']))
        # elif field == 'summary':
        #     t = query_tokens[0]
        #     reviews_q = list(
        #         filter(lambda x: t in str(x['summary']), reviews[asin]['reviews']))
        # else:
        #     reviews_q = reviews[asin]['reviews']

        reviews_q = reviews[asin]['reviews']
        review = reviews_q[0]
        prod_info['review'] = {}
        prod_info['review']['cnt'] = len(reviews[asin]['reviews'])
        prod_info['review']['text'] = review['reviewText']
        prod_info['review']['summary'] = review['summary']
        prod_info['review']['vote'] = review['vote']
        prod_info['review']['score'] = reviews[asin]['score']

        prod_result.append(prod_info)

    return prod_result


def get_advice(asins: list):
    candidate_goods = {}
    for asin in asins:
        prod = meta[meta['asin'] == asin].to_dict('records')[0]
        view = prod['also_view']
        buy = prod['also_buy']
        for i in view + buy:
            if i not in candidate_goods:
                candidate_goods[i] = 0
            candidate_goods[i] += 1

    if len(candidate_goods) == 0:
        return [], []

    # 统计 猜你喜欢 商品，这里存的是asin
    advice_goods = list(sorted(candidate_goods.items(),
                        key=itemgetter(1), reverse=True))

    # 根据建议商品，获取这些商品的高频关键词.推荐商品，返回的是title（商品名）
    advice_title = []
    grams_cnt = {}
    for good in advice_goods:
        try:
            prod = meta[meta['asin'] == good[0]].to_dict('records')[0]
        except IndexError:
            # 商品不在meta中
            continue
        advice_title.append(prod['title'])
        grams = cal.tokenize(str(prod['feature']), 2)
        # TODO 只取与query相关的n-gram
        for gram in grams:
            if gram not in grams_cnt:
                grams_cnt[gram] = 0
            grams_cnt[gram] += 1*math.log(good[1])  # 商品提及次数

    grams_cnt = list(
        sorted(grams_cnt.items(), key=itemgetter(1), reverse=True))
    return advice_title[:3], grams_cnt[:3]
