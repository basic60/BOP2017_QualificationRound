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
    for i in tmp:
        wordlist.append(i[0])   # 初始化word_list（单词列表）
        clist.append(i[1])      # 初始化clist（词性列表)


def init_query(query):                                              # 初始化查询语句
    global _last_query,_word_list,_clist,_importance,_keyword
    if query!=_last_query:
        _last_query=query                                           # 记录最新的查询，防止多次初始化一句询问
        _word_list=[]
        _clist=[]
        _fill_list(query,_word_list,_clist)                         # 初始化单词列表和词性列表

        _keyword=analyse.extract_tags(query)                        # 使用TF-IDF算法获取关键词
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
        tword=''
        if not time_add and isqtime(wd):                                # 处理查询时间意图
            k=-1
            for j in article_word:
                k+=1
                type_value_2=jieba_converter(article_clist[k])
                if type_value_2==WordType.number and hastime(j):
                    ret+=2                              # 查询时间意图匹配
                    time_add=True                       # 只匹配一次
                    # print('time correct')
                    break
        elif not location_add and type_value==WordType.location_name and wd in target:
            ret+=1                                                              # 地点匹配加1,只加一次
            location_add=True
        elif type_value==WordType.noun:                 # 处理名词匹配
            if wd in target:                            # 直接向等
                tval=1
                tword=wd
            else:                                       # 同义词匹配
                cnt=-1
                for j in article_word:
                    cnt+=1
                    if article_clist[cnt]==WordType.noun and is_synonyms(wd,j):
                        tval=0.9
                        tword=j
                        break
            if tval!=0:
                rank=2
                for j in _keyword:
                    if j==tword:
                        ret+=rank*tval                  # 名词匹配
                        # print(wd,'>>>>>noun correct')
                        break
                    rank-=0.2
                    if rank<=0: rank=0.2
        elif type_value==WordType.verb and wd!='是':    # 处理动词匹配
            if wd in target:                            # 直接相等
                # print(wd+" ===> verb correct")
                ret+=5
            else:
                cnt=-1
                for j in article_word:
                    cnt+=1
                    if jieba_converter(article_clist[cnt])==WordType.verb and is_synonyms(wd,j):
                        tval=0.9
                        # print(wd + " ===> verb correct")
                        break
                if tval!=0:
                    ret+=5*tval                         # 动词匹配
    # print(target)
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


