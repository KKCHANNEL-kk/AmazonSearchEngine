from operator import itemgetter
import pandas as pd
import redis
from nltk.stem import SnowballStemmer
import re
import calculate as cal
import json
import gzip

'''
需要用到的缓存：

    倒排索引：
        {doc_field}_{term}:倒排索引

    tf-idf:
        {doc_field}_{doc_asin}_len:文档长度
        {doc_field}_{doc_asin}_{term}_tf:词频
        {doc_field}_{term}_df:词文档频率

    余弦相似度:
        {doc_field}_{doc_asin}_tfidf:tf-idf向量缓存

'''


def parse(path):
    g = gzip.open(path, 'rb')
    for l in g:
        yield json.loads(l)


def getDF(path):
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
    return pd.DataFrame.from_dict(df, orient='index')


def info_dump(info, path):
    with open(path, 'w') as f:
        json.dump(info, f)


def get_redis_connect():
    pool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, password='123456')
    r = redis.Redis(connection_pool=pool)
    return r


def init_docs_info(doc_field, docs, cache_type='json'):
    '''
    初始化商品集数据
    doc:语料数据
    doc_asin:语料数据所属商品id
    doc_field:表示数据所在域，如title/description。
    '''

    N = len(docs)
    df = {}
    basic_info = {'index': {}, 'N': N, 'tf': {}, 'df': {}, 'doc_len': {}}
    for doc in docs:
        doc_asin = str(doc[0])
        doc_str = str(doc[1])

        index, doc_len, term_tf, term_set = parse_doc(
            doc_str, doc_asin, doc_field)
        for k, v in index.items():
            if k not in basic_info['index']:
                basic_info['index'][k] = []
            basic_info['index'][k] = basic_info['index'][k] + v
        for term in term_set:
            if term not in df:
                df[term] = 0
            df[term] += 1

        # 多条评论指向一件商品，长度取总和；其他情况下，一个doc_asin只与一条文本产生联系
        if doc_asin not in basic_info['doc_len']:
            basic_info['doc_len'][doc_asin] = 0
        basic_info['doc_len'][doc_asin] += doc_len

        # 大量无序索引列表，先合并，再排序。补充新索引，则先对补充部分排序，再合并。
        basic_info['tf'][doc_asin] = list(
            sorted(term_tf.items(), key=itemgetter(0), reverse=False))
    # DEBUG 前面没有把df打包进来
    basic_info['df'] = df
    for item, index_list in basic_info['index'].items():
        # DEBUG: list.sort默认改变原数组，返回值是None
        basic_info['index'][item] = sorted(index_list)

    # TODO redis部分 待优化
    # conn = get_redis_connect()

    # for asin_term_tf in basic_info['tf']:
    #     for asin,term_tf in asin_term_tf.items():
    #         conn.hmset(doc_field+'_'+asin+'_'+'tf', {term: tf})

    # for term, index in basic_info['index'].items():
    #     for i in index:
    #         conn.zadd('{}_{}_index'.format(doc_field, term), {i: 0})

    # basic_info['df'] = df
    # for term, df in basic_info['df'].items():
    #     conn.hmset('{}_df'.format(doc_field), {term: df})

    # conn.set('{}_N'.format(doc_field), basic_info['N'])
    # conn.close()

    return basic_info


def add_new_docs(doc_field, docs, cache_type='json'):
    pass
    # TODO 增加新语料。修改索引时，先对新增部分排序，再用union遍历合并。


def parse_doc(doc, doc_asin, doc_field):
    '''
    解析语料，语料数据入库。
    倒排索引、词频统计。

    return:
        {doc_field}_{doc_asin}_len:文档长度
        {doc_field}_{doc_asin}_{term}_tf:词频
        {doc_field}_{term}:倒排索引子集
        {doc_field}_{term}:去重词集合
    '''

    # 清洗，分词，提取词干
    # raw_str = re.sub('[^\w ]', '', doc)
    tokens = cal.tokenize(doc)
    doc_len = len(tokens)

    snowball_stemmer = SnowballStemmer("english")
    term_tf = {}
    index = {}
    term_set = set()
    for token in tokens:
        term = snowball_stemmer.stem(token)
        if term not in term_tf:
            term_tf[term] = 0
        term_tf[term] += 1
        if term not in index:
            index[term] = []
            index[term].append(doc_asin)
        term_set.add(term)

    return index, doc_len, term_tf, term_set


def load_field_cache(field: str, c_type='json'):
    if c_type == 'json':
        info_path = 'cache/{}_info.json'.format(field)
        with open(info_path, 'r') as f:
            info = json.load(f)
            return info

    elif c_type == 'redis':
        pass

def load_meta_json(path):
    with open(path, 'r') as f:
        meta = json.load(f)
    return meta
    