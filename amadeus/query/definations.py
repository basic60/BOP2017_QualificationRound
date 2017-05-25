class QueryType:
    thing=1
    time=2
    location=3
    reason=4

class WordType:
    noun=1           # 名词
    verb=2           # 动词
    noise=3          # 非语素词，比如“？”，“，”
    adj=4            # 形容词
    pronoun=5        # 代词，比如“我”，“这里”
    number=6         # 数词，比如“一个”
    preposition=7    # 介词，比如“在”
    time=8           # 时间词，比如“早上”
    location_name=9  # 地名
    conjunction=10   # 连词，比如“和”


    qthing=4
    qlocation=5
    qtime=6
    qreason=8


_jieba_to_buildin_dic={'a':WordType.adj,'r':WordType.pronoun,'m':WordType.number,'x':WordType.noise,
                       'p':WordType.pronoun,'v':WordType.verb,'n':WordType.noun,'ns':WordType.location_name,
                      'c':WordType.conjunction,'t':WordType.time}

def jieba_converter(clistvalue):
    if clistvalue in _jieba_to_buildin_dic:
        return _jieba_to_buildin_dic[clistvalue]
    else:
        return 0