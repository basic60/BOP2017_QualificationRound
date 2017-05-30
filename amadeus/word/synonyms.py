import os

_ifs=open(os.path.join(os.getcwd(),'data\synonyms.txt'),encoding='UTF-8')
_dicsize=43000

# 使用并查集建立同义词查询数据结构
_fa=[i for i in range(_dicsize<<1)]
_id={}
_cnt=0
def _findfa(x):
    if x==_fa[x]:
        return x
    else:
        _fa[x]=_findfa(_fa[x])
        return _fa[x]

def _union(a,b):
    _fa[_findfa(a)]=_findfa(b)

for i in _ifs.readlines():
    tmp=i.strip('\n').split('→')
    if not tmp[0] in _id:
        x=_id[tmp[0]]=_cnt
        _cnt+=1
    else:
        x=_id[tmp[0]]
    if not tmp[1] in _id:
        y=_id[tmp[1]]=_cnt
        _cnt+=1
    else:
        y=_id[tmp[1]]
    _union(x,y)

def is_synonyms(s1,s2):
    if s1==s2:
        return True
    suc=True
    if s1 in _id:
        x=_id[s1]
    else:
        return False

    if s2 in _id:
        y=_id[s2]
    else:
        return False

    return _findfa(x)==_findfa(y)

