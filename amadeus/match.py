import jieba.posseg as posseg
import jieba.analyse as analyse
from .query.definations import *
from .word.synonyms import *
from .query.qtime import *
from .query.qthing import *

_last_query=''              # 最新的查询，防止多次初始化一句询问
_importance=[]              # 单词权重
_word_list=[]               # 单词列表
_clist=[]                   # 词性列表，与单词列表一一对应
_keyword=[]                 # 关键词,降序排列

def _fill_list(sen,wordlist,clist):
    tmp=[(i.word, i.flag) for i in posseg.cut(sen)]
    wordlist=clist=[]           # 初始化列表释放内存
    for i in tmp:
        wordlist.append(i[0])   # 初始化word_list（单词列表）
        clist.append(i[1])      # 初始化clist（词性列表)


def init_query(query):                                              # 初始化查询语句
    global _last_query,_word_list,_clist,_importance,_keyword
    if query!=_last_query:
        _last_query=query                                           # 记录最新的查询，防止多次初始化一句询问
        _fill_list(query,_word_list,_clist)                         # 初始化单词列表和词性列表

        _keyword=analyse.extract_tags(query)
        _importance = [0 for i in range(len(_word_list))]           # 初始化权重列表

'''
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
'''


def match(query,target):
    init_query(query)

    location_add=False                           # 是否产生地点匹配
    time_add=False                               # 是否产生时间查询
    ret=0                                        # 函数返回值，匹配相似度，数值越大，相似度越高

    article_word=[]
    article_clist=[]

    _fill_list(target,article_word,article_clist)

    for i in range(len(_word_list)):
        wd=_word_list[i]
        fg=_clist[i]
        type_value = jieba_converter(fg)
        tval=0
        if type_value==WordType.noun:
            if wd in target:
                tval=1
            else:
                cnt=-1
                for j in article_word:
                    cnt+=1
                    if article_clist[cnt]==WordType.noun and is_synonyms(wd,j):
                        tval=1
            if tval!=0:
                rank=len(_keyword)




    return ret
'''
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
            ret+= _importance[cnt]                                              # 关键名词匹配
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
'''


