from .definations import *
from amadeus.word.synonyms import *
_query_number_word=['那几个','哪几个']
def isqnumber(word):
    return word in _query_number_word

def hasnumber(wlist,clist):
    try:
        cnt=-1
        for i in clist:
            cnt+=1
            if jieba_converter(clist[cnt])==WordType.number:
                if jieba_converter(clist[cnt+1])==WordType.number:
                    continue
                elif jieba_converter(clist[cnt + 1]) == WordType.noun:
                    return True
        return False
    except:
        return False
