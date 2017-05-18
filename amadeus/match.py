import jieba
import amadeus.intent as intent
from .query.definations import *

_possible_intent={}
_wclass={}
_last_query=''

_thing_answer=['是','以','由']

def match(query,target):
    global _possible_intent, _wclass,_last_query
    if query!=_last_query:
        _last_query=query
        _possible_intent, _wclass = intent.query_intent(query)      # 对pattern的初始化只进行一次

    _word_list=jieba.cut(target)
    ret=0
    for i in _wclass:
        if _wclass[i]==WordType.noun and i in target:   # 名词匹配加0.5
            print('noun')
            ret+=0.5

    for i in _possible_intent:
        tmp=0
        totintent = _possible_intent[i]
        if i==QueryType.thing:
            for j in _word_list:
                if j in _thing_answer and tmp+1<=totintent:
                        tmp+=1
            tmp/=totintent
        ret+=tmp                                        # 意图匹配加1
    return ret