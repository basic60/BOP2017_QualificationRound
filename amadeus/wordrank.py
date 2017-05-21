import jieba.analyse
def brute_force(s1,s2):
    t1=jieba.analyse.extract_tags(s1)
    t2=jieba.analyse.extract_tags(s2)
    ret=0
    for i in t1:
        cnt=len(t2)
        for j in t2:
            if i==j:
                ret+=cnt
                break
            else:
                cnt-=1
    return ret
