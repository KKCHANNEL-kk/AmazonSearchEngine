from sympy import marcumq
import store
import calculate as cal
import math
from nltk.stem import SnowballStemmer
from operator import itemgetter
import os
import service
os.chdir(r'd:\Vscodeworkplace\amzSearch')

service.start_service()
# print(1)
meta = store.getDF('data/meta_Gift_Cards.json.gz')
# review = store.getDF('data/Gift_Cards.json.gz')
# info = store.load_field_cache('reviewText')

# tf = info['tf']
# df = info['df']
# N = info['N']

# snowball_stemmer = SnowballStemmer("english")
# q = 'baby'
# query_tokens = cal.tokenize(q)

# index_lists = [info['index']
#                [snowball_stemmer.stem(token)] for token in query_tokens]
# # print(index_lists[:5])
# mul_ints_ans = cal.multiIntersect(index_lists)
# # print(mul_ints_ans[:10])

# matrix = cal.tfidf_matrix('long', mul_ints_ans, tf, df, N)
# # print(matrix)

# q_vec = cal.get_query_tfidf(query_tokens, df, N)
# # print(q_vec)

# results = []
# v1 = list(sorted(q_vec.items(), key=itemgetter(0), reverse=False))
# for doc_asin, vec_candidate in matrix.items():
#     v2 = list(sorted(vec_candidate.items(), key=itemgetter(0), reverse=False))
#     results.append((doc_asin, cal.cosine_similarity(v1, v2)))

# s_results = sorted(results, key=lambda x: x[1], reverse=True)

# review['reviewText'] = review['reviewText'].fillna('').astype(str)
# print(review['reviewText'])
# for result in s_results[:10]:
#     doc_asin = result[0]
#     # print("doc_asin:", doc_asin)
#     # doc = meta[meta['asin'] == doc_asin]
#     # print("doc:", doc['title'])
#     rt = review[review['asin'] == doc_asin]['reviewText']
#     # print('review:', review[review['asin'] == doc_asin][:1]['reviewText'])
#     # print("score:", result[1])
#     for r in rt:
#         try:
#             if q in r:
#                 print("doc_asin:", doc_asin)
#                 print('review:', r)
#                 print("score:", result[1])
#                 break
#         except Exception as e:
#             exit(e)

r = service.handle_query('shoe','title')