import jieba
import jieba.posseg as posseg
import amadeus.match as match

def calculate_relevancy(pattern,target):
    return match.match(pattern,target)

def find_max(tmp):
    pos=-1
    maxx=-1
    index=0
    for i in tmp:
        index+=1
        if i>maxx:
            maxx=i
            pos=index
    return pos,maxx

def test_process(ifile):
    data=ifile.readlines()              # 文件以List形式逐行读取到data。
    limit=0                             # 读取行数的数目，以方便测试。
    last=""                             # 上一个问题。

    ans_list=[]                         # 正确答案序列
    my_list=[]                          # 计算答案序列
    ac_num=0                            # 正确答案个数
    tot_num=0                           # 测试数据总组数
    article_list=[]                     # 文章内容

    def check():
        nonlocal ac_num,tot_num,last,ans_list,my_list,article_list
        posans, relans = find_max(ans_list)
        posmy, relmy = find_max(my_list)
        if posans == posmy:
            ac_num += 1
        else:
            print("\033[1;31;0mIncorrect answer:\033[36;0m\nThe question is: " + last +
                  "\n\033[33;0mThe wrong pos is:<<< " + str(posmy) +
                  " >>> Wrong Sentence:" + article_list[posmy] + "Calculated Relativity:" + str(relmy) + "\n"+
                  "\033[32;0mThe correct pos is:<<< " +str(posans) +
                  " >>> Correct Sentence: "+article_list[posans],end='\033[34;0m')
            print(my_list)
            print("\033[1;31;0m======================================="
                  "============================================\033[0m")

        last = que
        tot_num += 1
        ans_list.clear()
        my_list.clear()
        article_list.clear()

    for i in data:
        limit+=1
        ans,que,sen=i.split('\t')       # ans,que,sen分别代表匹配程度，问题和句子内容。
        ans=int(ans)
        if limit==1: last=que           # 初始化last
        if que!=last:
            check()
        article_list.append(sen)
        ans_list.append(ans)
        my_list.append(calculate_relevancy(que,sen))

        if limit>19:
            break
    check()
    print("Total "+str(ac_num)+" correct answers.\n"+"The correct rate is "+str(ac_num/tot_num))

if __name__ == '__main__':
  #  asd=posseg.cut("这由什么组成？这是哪里")
   # for j in asd:
    #    print(j.word,j.flag,type(j.flag))
    ifs = open('dev.txt', encoding='UTF-8')
    test_process(ifs)