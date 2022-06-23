import time
import store
import pandas as pd
import gzip
import json
import re


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

# 初始化数据，将新语料读入语料库
df1 = getDF('data/meta_Gift_Cards.json.gz')
fields = ['title', 'feature', 'description']
print('df1 shape: {}'.format(df1.shape))


def init_data(df, field):
    data = list(zip(df['asin'], df[field]))
    info = store.init_docs_info(field, data)
    # store.info_dump(info, 'cache/{}_info.json'.format(field))

for field in fields:
    start = time.time()
    init_data(df1, field)
    end = time.time()
    print('{} init finished in {}'.format(field, end-start))

df2 = getDF('data/Gift_Cards.json.gz')
print('df2 shape: {}'.format(df2.shape))
fields = ['reviewText', 'summary']

for field in fields:
    start = time.time()
    init_data(df2, field)
    end = time.time()
    print('{} init finished in {}'.format(field, end-start))


# 评论数据重构，以商品为主键
# df = getDF('data/Gift_Cards.json.gz')
# goods_reviews = {}
# for row in df.itertuples():
#     asin = row.asin
#     row_dict = row._asdict()
#     del row_dict['Index']

#     if asin not in goods_reviews:
#         goods_reviews[asin] = {}
#         goods_reviews[asin]['reviews'] = []
#         goods_reviews[asin]['score'] = 0
#     goods_reviews[asin]['reviews'].append(row_dict)
#     goods_reviews[asin]['score'] += row.overall

# for asin, info in goods_reviews.items():
#     info['score'] /= len(info['reviews'])
#     # TODO Vote有NaN，需要处理
#     for review in info['reviews']:
#         temp = float(re.sub(',', '', re.sub(
#             'nan', '0', str(review['vote']))))
#         if str(temp) != str(review['vote'])[:-2]:
#             print('{} {} {}'.format(asin, review['vote'], temp))
#         # review['vote'].astype(float)
#         review['vote'] = temp

#     info['reviews'].sort(key=lambda x: (
#         x['vote'], int(x['unixReviewTime'])), reverse=True)

# store.info_dump(goods_reviews, 'cache/goods_reviews.json')

# g_r = store.load_meta_json('cache/goods_reviews.json')
# print(g_r['B001GXRQW0'])
