import jieba
import amadeus.intent as intent
from .query.definations import *

_possible_intent={}
_wclass={}
_last_query=''

def match(query,target):
    global _possible_intent, _wclass,_last_query
    if query!=_last_query:
        _last_query=query
        _possible_intent, _wclass = intent.query_intent(query)      # 对pattern的初始化只进行一次
    for i in _possible_intent:
        cnt = _possible_intent[i]
    return 0