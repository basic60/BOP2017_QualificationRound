import jieba
from .query.qthing import *
from .query.definations import *

_noise=['吗', '啊', '请问', '哦']
def query_intent(query):
    def _add(s):
        nonlocal possible_intent
        if s in possible_intent:
            possible_intent[s] += 1
        else:
            possible_intent[s] = 1
    word_list=jieba.cut(query)              # 句子分词后的各个部分
    wclass_list=[]                          # 各个词的词性
    possible_intent={}
    for i in word_list:
        if isqthing(i):
            _add(QueryType.thing)
            wclass_list.append(WordType.thing)
        elif i in _noise:
            wclass_list.append(WordType.noise)
    return possible_intent,dict(zip(word_list,wclass_list))
