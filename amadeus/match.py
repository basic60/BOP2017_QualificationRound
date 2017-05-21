import jieba.posseg as posseg
from .query.definations import *
from .query.qtime import *
from .query.qthing import *

_last_query=''
_importance=[]
_word_list=[]
_clist=[]
def init_query(query):                                                          # 初始化查询语句
    global _last_query,_word_list,_clist,_importance
    if query!=_last_query:
        _last_query=query                                                       # 记录新的查询
        _query_posres = [(i.word, i.flag) for i in posseg.cut(query)]
        _word_list=_importance=_clist=[]                                    # 初始化并释放内存
        for i in _query_posres:
            _word_list.append(i[0])
            _clist.append(i[1])

        _importance=[0 for i in range(len(_word_list))]
        for i in range(len(_word_list)):
            if isqthing(_word_list[i],_clist[i]):
                j=i
                while j-1>=0:
                    if jieba_converter(_clist[j-1])==WordType.noun:
                        _importance[j - 1]=2
                        break
                    else:
                        j-=1
            elif jieba_converter(_clist[i])==WordType.noun and _importance[i]==0:
                _importance[i]=0.5
            elif jieba_converter(_clist[i])==WordType.verb:
                _importance[i]=2


def match(query,target):
    init_query(query)

    location_add=0
    ret=0

    article_list=posseg.cut(target)
    cnt=-1

    for i in range(len(_word_list)):
        cnt+=1
        wd=_word_list[i]
        fg=_clist[i]

        type_value=jieba_converter(fg)

        if type_value==WordType.location_name and wd in target and location_add==0:
            # print("location same: "+wd)
            ret+=1                                                              # 地点匹配加1,只加一次
            location_add=1
        elif type_value==WordType.noun and wd in target:
            # print("noun same>>> "+wd+"  val: "+str(_important_noun[cnt]))
            ret+= _importance[cnt]                                          # 关键名词匹配
        else:
            pass
            # print(wd)

        if isqtime(wd):
            for j in article_list:
                wd2=j.word
                fg2=j.flag
                type_value_2=jieba_converter(fg2)
                if type_value_2==WordType.number and hastime(wd2):
                    ret+=2                                                      # 查询时间意图匹配
                # print("time: "+wd2)
                    break
    # print(target)
    return ret
