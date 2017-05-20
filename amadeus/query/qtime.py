_query_time=['时候']
_time_str=['年','月','日']
def isqtime(v):
    return v in _query_time

def hastime(s):
    for i in _time_str:
        if i in s:
            return True
    return False
