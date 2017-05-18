import jieba.posseg as posseg
from .query.qthing import *
from .query.definations import *
from .query.qnoise import *

def query_intent(query):
    def _add(s):
        nonlocal possible_intent
        if s in possible_intent:
            possible_intent[s] += 1
        else:
            possible_intent[s] = 1

    word_list=posseg.cut(query)              # 句子分词后的各个部分
    wclass_list=[]                          # 各个词的词性
    possible_intent={}
    ret={}
    for ii in word_list:
        wd=ii.word
        i=ii.flag

        print(wd+"===")
        if isqthing(wd):
            _add(QueryType.thing)
            wclass_list.append(WordType.thing)
            ret[wd] = WordType.thing
        elif isnoise(i):
            wclass_list.append(WordType.noise)
            ret[wd] = WordType.noise
        else:
            wclass_list.append(WordType.noun)
            ret[wd] = WordType.noun
    return possible_intent,ret
