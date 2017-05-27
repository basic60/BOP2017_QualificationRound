import jieba.posseg as posseg
import jieba.analyse as analyse
from .query.definations import *
from .word.synonyms import *
from .query.qtime import *
from .query.qreason import *
from .query.qlocation import *

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

def match(query,target,debug=False):
    init_query(query)
    location_add=False                           # 是否产生地点匹配
    time_add=False                               # 是否产生时间查询
    reason_add=False                             # 是否产生原因匹配
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
                    if debug: print('time correct')
                    break
        elif not reason_add and isqreason(wd) and hasanswer(query):         # 处理原因查询
            ret+=5
            reason_add=True
        elif not location_add and isqlocation(wd):
            for j in article_clist:
                if jieba_converter(j)==WordType.location_name:
                    ret+=5
                    location_add=True
                    break
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
                        if debug: print(wd,'>>>>>noun correct')
                        break
                    rank-=0.2
                    if rank<=0: rank=0.2
        elif type_value==WordType.verb and wd!='是' and wd!='有' and wd!='会':    # 处理动词匹配
            samev=False
            for k in range(i):
                if jieba_converter(_clist[k])==WordType.verb and is_synonyms(wd,_word_list[k])>=0.5:
                    samev=True
                    break
            if samev: continue

            if wd in target:                            # 直接相等
                if debug: print(wd+" ===> verb same")
                ret+=5
            else:
                cnt=-1
                for j in article_word:
                    cnt+=1
                    if jieba_converter(article_clist[cnt])==WordType.verb:
                        tmp=is_synonyms(wd,j)
                        if tmp>0.8:
                            ret+=5*tmp
                        if debug: print(wd + " ===> s_verb correct")
                        break
    if debug: print(target)
    return ret


