import jieba.posseg as posseg
from .query.definations import *

def query_intent(query):
    tmp=posseg.cut(query)
    for i in tmp:
        wd=i.word
        fg=i.flag
        if jieba_converter(fg)==WordType.location_name :
            pass


