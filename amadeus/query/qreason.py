_query_reason_word=['为什么','为何']
_answer_word=['因为']
def isqreason(word):
    return word in _query_reason_word

def hasanswer(s):
    for j in _answer_word:
        if j in s:
            return True
    return False
