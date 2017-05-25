_query_time=['时候']
_time_str=['年','月','日']
# 判断是否是在查询时间
def isqtime(word):
    return word in _query_time

# 判断一个字符串中是否可能包含时间
def hastime(s):
    for i in _time_str:
        if i in s:
            return True
    return False
