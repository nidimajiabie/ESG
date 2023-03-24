from LAC import LAC
import numpy as np

def removeStop(content):
    '''
    delete stopwords of content
    :param content: a str
    :param stopwords: a list
    :return: content with out stopwords
    '''
    stopwords=[]
    with open(r"D:\资料\鸣石\union_Stop_words.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            stopwords.append(line)
    for i in stopwords:
        if i in content:
            content = content.replace(i, '')
    return content
def segment(readpaths):
    '''
    remove spaces and line breaks from content in txt given readpath, select readpaths whose txt are null and segment content in txt
    :param readpaths:a list of str
    :param punct:whether to remove punctuation of content in txt, the defalut is False
    :return:three lists: contents in txt without spaces and line breaks, readpaths whose txt are null, segmentations of contents in txt
    '''
    wenbens=[]
    nulls=[]
    seglists=[]
    lac = LAC(mode='lac')#Load the lac package
    for readpath in readpaths:
        f=open(readpath,'r',encoding='utf-8')
        wenben=f.read()
        f.close
        wenben=wenben.replace(' ','').replace('\n','').replace('\t','')
        wenben=removeStop(wenben)
        if len(wenben) == 0:
            nulls.append(readpath)
        wenbens.append(wenben)
        lac_result = lac.run(wenben)
        seglist = lac_result[0]
        seglists.append(seglist)
    return wenbens,nulls,seglists
def moving(unroll,roll,thres):
    '''
    moving words of unroll from roll
    :param unroll: a list of words
    :param roll: a list of lists of words
    :param thres: a float between 0 and 1
    :return: words that are not only in unroll but in most lists of roll
    '''
    regular_words=[]
    thres=thres*len(roll)
    for i in range(0,len(unroll)):
        b=0
        regular_word=unroll[i]
        for j in range(0,len(roll)):
            if regular_word in roll[j]:
                b=b+1
        if b>=thres and regular_word not in regular_words:
            regular_words.append(regular_word)
    return regular_words
def unique(textlist):
    '''
    make textlist to be a list of unique elements
    :param textlist: a list of lists
    :return: textlist with unique elements
    '''
    newlist=['+'.join(textlist[i]) for i in range(0,len(textlist))]
    newlist=list(set(newlist))
    newlist=[newlist[i].split('+') for i in range(0,len(newlist))]
    return newlist
def sumlist(lislist):
    '''
    merge lists to be a big list
    :param lislist: a list of lists
    :return: a merged list
    '''
    bindlis=[]
    for lis in lislist:
        bindlis=bindlis+lis
    return bindlis
def thres_select(seglists):
    '''
    select a threshold such that we can regard a word as a usualword
    :param seglists: a list
    :return: a list of number of usualwords
    '''
    usualword_nums=[]
    division=np.linspace(0,1,11)
    for thres in division:
        movingwords=[moving(seglists[i],seglists,thres) for i in range(0,len(seglists))]
        usualword=list(set(sumlist(movingwords)))
        usualword_num=len(usualword)
        usualword_nums.append(usualword_num)
    print("阈值为 %s 的废话模板中词的数量依次为 %s" %(" ".join(str(i) for i in division)," ".join(str(i) for i in usualword_nums)))
    return usualword_nums
def nonsense_rate(seglists,usualwords):
    '''calculate nonsense rate for every element of seglists
    seglists ia a list of lists
    usualwords is a list
    return a list a nonsense_rate'''
    usualrate=[]
    for i in range(0,len(seglists)):
        usualnum=0
        if len(seglists[i])==0:
            print('nothing in the %d text!!!' %i )
            rate=-1
        else:
            for word in seglists[i]:
                if word in usualwords:
                    usualnum=usualnum+1
            rate=usualnum/len(seglists[i])
        usualrate.append(rate)
    return usualrate
def remove0(content):
    '''
    remove all '' in content
    :param content: a list
    :return: content without ''
    '''
    if '' in content:
        content=content[0:content.index('')]
    else:
        content=content
    return content