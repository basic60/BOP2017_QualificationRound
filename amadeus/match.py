import jieba.posseg as posseg
import jieba.analyse as analyse
from .query.definations import *
from .word.synonyms import *
from .query.qtime import *
from .query.qreason import *
from .query.qlocation import *
from .query.qperson import *
from .query.qnumber import *
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

    has_qlocation=False

    location_add=False                           # 是否产生地点匹配

    has_qtime=False
    time_add=False                               # 是否产生时间查询

    has_qreason=False
    reason_add=False                             # 是否产生原因匹配

    has_qpearson=False
    person_add=False

    has_verb=False
    verb_add=False

    has_noun=False
    noun_count=0

    has_number=False
    number_add=False
    ret=0                                        # 函数返回值，匹配相似度，数值越大，相似度越高

    article_word=[]
    article_clist=[]
    _fill_list(target,article_word,article_clist)

    for i in range(len(_word_list)):
        wd=_word_list[i]
        fg=_clist[i]
        type_value = jieba_converter(fg)
        if not time_add and isqtime(wd):                                    # 处理查询时间意图
            k=-1
            has_qtime=True
            for j in article_word:
                k+=1
                type_value_2=jieba_converter(article_clist[k])
                if type_value_2==WordType.number and hastime(j):
                    ret+=2                                                  # 查询时间意图匹配
                    time_add=True                                           # 只匹配一次
                    if debug: print('time correct')
                    break
        elif not reason_add and isqreason(wd) and hasanswer(query):         # 处理原因查询
           has_qreason=True
           ret+=5
           if debug:print('reasona add')
           reason_add=True
        elif not person_add and isqperson(wd):                              # 处理人名匹配
            cnt=-1
            has_qpearson=True
            for j in article_clist:
               cnt+=1
               if jieba_converter(j)==WordType.personname:
                   person_add=True
                   if debug:print('person same',article_word[cnt])
                   ret+=5
                   break
        elif not location_add and isqlocation(wd):
            cnt=-1
            has_qlocation=True
            for j in article_clist:
                cnt+=1
                if jieba_converter(j)==WordType.location_name:
                    ret+=5
                    if debug: print('location same'+article_word[cnt])
                    location_add=True
                    break
        elif not number_add and isqnumber(wd):
            has_number=True
            if not number_add and hasnumber(article_word,article_clist):
                ret+=5
                if debug: print('number add')
                number_add=True
        elif type_value==WordType.noun or type_value==WordType.location_name:                       # 处理名词匹配
            tval=0
            has_noun=True
            if wd in target:
                tval=1
            else:
                cnt=-1
                for j in article_word:
                    cnt+=1
                    if jieba_converter(article_clist[cnt])==WordType.noun and is_synonyms(wd,j):
                        if debug:print(wd+"noum sif >>>>>>>>>>>>"+j)
                        noun_count+=1
                        tval=1
                        break
            if tval!=0:
                rank = 3
                for j in _keyword:
                    if j == wd:
                        ret += rank * tval                      # 名词匹配
                        noun_count+=1
                        if debug:
                            print(wd, '>>>>>noun correct',rank)
                        break
                    rank -= 0.3
                    if rank <= 0: rank = 0.3
        elif type_value==WordType.verb and not is_unusefulverb(wd):    # 处理动词匹配
            samev=False
            has_verb=True
            for k in range(i):
                if jieba_converter(_clist[k])==WordType.verb and is_synonyms(wd,_word_list[k]):
                    samev=True
                    break
            if samev: continue

            if wd in target:                            # 直接相等
                if debug: print(wd+" ===> verb same")
                verb_add=True
                ret+=5
            else:
                cnt=-1
                for j in article_word:
                    cnt+=1
                    if not is_unusefulverb(j) and jieba_converter(article_clist[cnt])==WordType.verb:
                        if is_synonyms(wd,j):
                            ret+=5
                            verb_add=True
                            if debug: print(wd + " ===> s_verb correct"+j)
                            break

    if has_qlocation and location_add==False:
        if debug: print('minus location')
        ret-=5
    if has_qpearson and person_add==False:
        if debug: print('minus person')
        ret-=5
    if has_qreason and person_add==False:
        if debug: print('minus reason')
        ret-=5
    if has_qtime and time_add==False:
        if debug: print('minus time')
        ret-=5
    if has_verb and verb_add==False:
        if debug:print('minus verb')
        ret-=5
    if has_noun and noun_count==0:
        if debug: print('minus noun')
        ret-=5
    if has_number and number_add==False:
        ret-=5
        if debug: print('minus number')
    if debug: print(target)
    return ret


_useful_verb=['是','会','有']
def is_unusefulverb(s):
    return s in _useful_verb