import jieba  # 用于中文分词
import jieba.analyse
import jieba.posseg
import amadeus.match as match
import os
from multiprocessing import Pool
import time
import amadeus.word.synonyms as syn

# 计算两个句子的相关度
def calculate_relevancy(pattern, target,dbg=False):
    return match.match(pattern, target,debug=dbg)

# 寻找答案序列中最大值的位置。
def find_max(tmp):
    pos = -1
    maxx = -1
    index = -1
    for i in tmp:
        index += 1
        if i > maxx:
            maxx = i
            pos = index
    return pos, maxx

# 测试
def test_process(ifile, debug=True):
    last = ""  # 上一个问题。
    ans_list = []  # 正确答案序列
    my_list = []  # 计算答案序列
    ac_num = 0  # 正确答案个数
    tot_num = 0  # 测试数据总组数
    article_list = []  # 文章内容
    ofs = open('output.txt', 'w', encoding='UTF-8')
    limit = 0

    def check():
        nonlocal ac_num, tot_num, last, ans_list, my_list, article_list
        posans, relans = find_max(ans_list)
        posmy, relmy = find_max(my_list)

        if posans == posmy:
            if debug:
                print("\033[34;0mNo." + str(tot_num + 1) + " is correct.The sequence:")
                print(my_list)
                print('\033[0m',end='')
            ac_num += 1
        else:
            if debug:
                print("\033[1;31;0mIncorrect answer:\033[36;0m\nThe question is: " + last +
                      "\n\033[33;0mThe wrong pos is:<<< " + str(posmy) +
                      " >>> Wrong Sentence:" + article_list[posmy] + "Calculated Relativity:" + str(relmy) + "\n" +
                      "\033[32;0mThe correct pos is:<<< " + str(posans) +
                      " >>> Correct Sentence: " + article_list[posans], end='\033[34;0m')

                print(my_list)
                print('\033[1;31;0m======================================='
                      '============================================\033[0m')
        last = que
        tot_num += 1
        ans_list = []
        my_list = []
        article_list = []

    for i in ifile.readlines():
        limit += 1
        ans, que, sen = i.split('\t')  # ans,que,sen分别代表匹配程度，问题和句子内容。
        ans = int(ans)
        if limit == 1: last = que  # 初始化last
        if que != last:
            check()
        article_list.append(sen)
        ans_list.append(ans)
        val = calculate_relevancy(que, sen,debug)
        my_list.append(val)
        ofs.write(str(val) + '\n')

        # if limit>500:
        #    break

    check()
    print("\033[1;31;0mTotal " + str(ac_num) + " correct answers.\n" + "The accuracy rate is " + str(ac_num / tot_num))

# 输出答案
def oj(ifile, opath='d:\zzh\output.txt'):
    print('output:  ' + opath)
    ofs = open(opath, 'w', encoding='UTF-8')
    limit = 0  # 读取行数的数目，以方便测试。
    for i in ifile.readlines():
        limit += 1
        ans, que, sen = i.split('\t')  # ans,que,sen分别代表匹配程度，问题和句子内容。
        val = calculate_relevancy(que, sen)
        ofs.write(str(val) + '\n')
    ofs.close()

# 分割输入文件
def separate(ifile):
    num = 0
    tot = 0
    filenane = str(num) + ".txt"
    fpath = os.path.join(os.getcwd(), 'data')
    fpath = os.path.join(fpath, filenane)
    ofs = open(fpath, 'w', encoding='utf-8')
    last = ""  # 上一个问题。

    def check():
        nonlocal last, tot, num, ofs, fpath, filenane
        last = que
        tot += 1
        if tot == 500:
            tot = 0
            num += 1
            ofs.close()
            filenane = str(num) + ".txt"
            fpath = os.path.join(os.getcwd(), 'data')
            fpath = os.path.join(fpath, filenane)
            print('Creating ' + fpath)
            ofs = open(fpath, 'w', encoding='utf-8')

    limit = 0
    for i in ifile.readlines():
        limit += 1
        ans, que, sen = i.split('\t')  # ans,que,sen分别代表匹配程度，问题和句子内容。
        if limit == 1: last = que  # 初始化last
        if que != last:
            check()
        ofs.write(i)

    ofs.close()

# 加载数据
def load_input(fname, refresh=False):
    ifs = open(fname, 'r', encoding='UTF-8')
    if not os.path.exists('data') or refresh:
        separate(ifs)
    ifs.close()

# 开始运行，共开启process_number个子进程
def execute(process_number):
    fpath = os.path.join(os.getcwd(), 'data')
    files = os.listdir(fpath)
    num = len(files)-1
    pol = Pool(process_number)
    for i in range(num):
        pol.apply_async(test2, args=(i, os.path.join(fpath, str(i) + '.txt')), )
    pol.close()
    pol.join()
    merge(num)

def test2(id, fname):
    jieba.load_userdict('dic.txt')
    outpath = os.path.join(os.getcwd(), 'ans')
    outpath = os.path.join(outpath, str(id) + ".txt")

    inpath = os.path.join(os.getcwd(), 'data')
    inpath = os.path.join(inpath, fname)
    print('Processing ' + fname)

    ifs = open(inpath, 'r', encoding='UTF-8')
    oj(ifs, outpath)
    ifs.close()

# 将不同文件的答案合并
def merge(num):
    sepath = os.path.join(os.getcwd(), 'ans')
    outpath = os.path.join(sepath, '0_output.txt')
    ofs = open(outpath, 'w', encoding='UTF-8')
    for i in range(num):
        pnow = os.path.join(sepath, str(i) + '.txt')
        print("Merging answers: " + pnow)
        ifs = open(pnow, 'r', encoding='UTF-8')
        for i in ifs.readlines():
            ofs.write(i)
        ifs.close()
    ofs.close()

if __name__ == '__main__':
    start = time.time()  # 开始计算运行时间

    # =======================多进程测试，输出文件为ans/0_output.txt=============
    # load_input('dev.txt')     # 读取数据
    # execute(4)                # 多进程版本
    # =============================================================================

    # =======================单进程测试，输出文件为output.txt========================
    ifs = open('dev.txt', 'r', encoding='UTF-8')
    jieba.load_userdict('dic.txt')
    test_process(ifs,debug=True)
    ifs.close()
    # ==============================================================================

    end=time.time()
    print("Executing time: %f secs" % (end - start))  # 输出运行时间
