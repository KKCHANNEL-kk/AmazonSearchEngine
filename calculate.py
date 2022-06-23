from nltk.tokenize import word_tokenize
import math
from operator import itemgetter
import re
from nltk.stem import SnowballStemmer
from nltk.util import ngrams

def tokenize(doc, ngram=1):
    raw_str = re.sub('[^\w ]', '', doc)
    result = word_tokenize(raw_str)
    if ngram > 1:
        result = list(ngrams(result, 2))
    return result


# TODO tf-idf缓存层
tfidf_cache = {}


def tfidf_matrix(doc_type: str, docs: list[str], tf: dict, df: dict, N: int):
    matrix = {}
    global tfidf_cache
    if doc_type == 'short':
        for doc_asin in docs:
            try:
                matrix[doc_asin] = tfidf_cache[doc_asin]
            except KeyError:
                tf_mini = tf[doc_asin]
                vec = {}
                for term, tf_val in tf_mini.items():
                    df_val = df[term]
                    idf_val = math.log(N/df_val, 10)
                    vec[term] = round((1+math.log(tf_val, 10))*idf_val, 6)
                matrix[doc_asin] = vec
                tfidf_cache[doc_asin] = vec

    elif doc_type == 'long':
        for doc_asin in docs:
            try:
                matrix[doc_asin] = tfidf_cache[doc_asin]
            except KeyError:
                tf_mini = tf[doc_asin]
                # 为了获得长文本/评论文本的总词频，需要多遍历一次
                tf_sum = 0
                for term, tf_val in tf_mini.items():
                    tf_sum += tf_val

                vec = {}
                for term, tf_val in tf_mini.items():
                    df_val = df[term]
                    idf_val = math.log(N/df_val, 10)
                    vec[term] = round((tf_val/tf_sum)*idf_val, 6)
                matrix[doc_asin] = vec
                tfidf_cache[doc_asin] = vec

    return matrix


def vecDot(vec1, vec2):
    '''
    计算两个向量的点积
    '''
    i = 0
    j = 0
    len_i = len(vec1)
    len_j = len(vec2)
    dot_value = 0
    while i < len_i and j < len_j:
        if(vec1[i][0] == vec2[j][0]):
            dot_value += vec1[i][1]*vec2[j][1]
            i += 1
            j += 1
        elif vec1[i][0] < vec2[j][0]:
            i += 1
        elif vec1[i][0] > vec2[j][0]:
            j += 1
    return dot_value


def vecLen(vec):
    '''
    计算向量的空间长度
    '''
    len_value = 0
    for item in vec:
        len_value += item[1]**2

    return math.sqrt(len_value)


def cosine_similarity(v1: list, v2: list):
    # v1 = list(sorted(vec1.items(), key=itemgetter(0), reverse=False))
    # v2 = list(sorted(vec2.items(), key=itemgetter(0), reverse=False))
    dot = vecDot(v1, v2)
    len_doc1 = vecLen(v1)
    len_doc2 = vecLen(v2)
    if len_doc1 == 0 or len_doc2 == 0:
        return 0

    return round(dot/(len_doc1*len_doc2), 6)


def intersect(list1: list, list2: list) -> list:
    """
    取两个列表的交集
    """
    answer = []
    i = 1
    j = 1
    len_i = len(list1)
    len_j = len(list2)

    while i < len_i and j < len_j:
        if list1[i] == list2[j]:
            answer.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return answer


def multiIntersect(lists: list) -> list:
    """
    取多个列表的交集
    """
    lists.sort(key=lambda x: x[0])
    cmp_count = len(lists)
    if cmp_count == 1:
        return lists[0]
    else:
        answer = intersect(lists[0], lists[1])
    index = 2
    while index != cmp_count:
        answer = intersect(answer, lists[index])
        index += 1
    return answer


def get_query_tfidf(tokens: list, df, N):
    term_tf = {}
    snowball_stemmer = SnowballStemmer("english")
    terms = []
    for token in tokens:
        term = snowball_stemmer.stem(token)
        if term not in term_tf:
            term_tf[term] = 0
            terms.append(term)
        term_tf[term] += 1
    q_vec = {}
    for term in terms:
        df_val = df[term]
        idf_val = math.log(N/df_val, 10)
        tf_val = term_tf[term]
        q_vec[term] = round((1+math.log(tf_val, 10))*idf_val, 6)
    return q_vec
