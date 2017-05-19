import jieba.posseg as posseg
from .query.definations import *
from .query.qtime import *
from .query.qthing import *

_last_query=''
_query_posres=''
_important_noun=[]
_word_list=[]
_clist=[]
def init_query(query):
    global _last_query,_query_posres,_word_list,_clist,_important_noun
    _query_posres = posseg.cut(query)
    if query!=_last_query:
        print('ent!!!')
        _last_query=query
        for i in _query_posres:
            wd=i.word
            fg=i.flag
            _word_list.append(wd)
            _clist.append(fg)
        for i in range(len(_word_list)):
            if isqthing(_word_list[i],_clist[i]):
                j=i
                find=False
                while j-1>=0:
                   if jieba_converter(_clist[j-1])==WordType.noun:
                        _important_noun.append(2)
                        find=True
                        break
                   else:
                       j-=1
                if not find:
                    _important_noun.append(0.5)
            elif jieba_converter(_clist[i])==WordType.noun:
                _important_noun.append(0.5)
            else:
                _important_noun.append(0)
   #     print(_important_noun)

def match(query,target):
    init_query(query)

    location_add=0
    ret=0

    article_list=posseg.cut(target)

    cnt=0
    for i in _query_posres:
        cnt+=1
        wd=i.word
        fg=i.flag

        type_value=jieba_converter(fg)

        if type_value==WordType.location_name and wd in target and location_add==0:
            ret+=1                                                              # 地点匹配加1,只加一次
            location_add=1
        elif type_value==WordType.noun and wd in target:
            ret+= 1 * _important_noun[cnt]                                          # 名词匹配加1
            #print(">>"+wd)

        if isqtime(wd):
            for j in article_list:
                wd2=j.word
                fg2=j.flag
                type_value_2=jieba_converter(fg2)
                if type_value_2==WordType.time:
                    ret+=1
                    break
    #print(target)
    return ret