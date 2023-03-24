import re
from fuzzywuzzy import process

def char_only(readpaths):
    '''
    remove spaces and line breaks from content in txt given readpath and select readpaths whose txt are null
    :param readpaths: a list of str
    :return: two lists: contents in txt without spaces and line breaks, readpaths whose txt are null
    '''
    wenbens=[]
    nulls=[]
    for readpath in readpaths:
        f=open(readpath,'r',encoding='utf-8')
        wenben=f.read()
        wenben=wenben.replace(' ','').replace('\n','').replace('\t','')
        if len(wenben)==0:
            nulls.append(readpath)
        wenbens.append(wenben)
        f.close
    return wenbens,nulls
def readrefer(reference):
    '''
    According to the book name search str
    :param reference:a str
    :return:unique str with book name
    '''
    refer=re.findall(r"《.*?》",reference)#筛选带书名号的字符串,输出为一个字符串list
    for x in refer:
        if x=='《》':
            refer.remove(x)
    refer_norepeat=list(set(refer))#去除列表中相同的元素
    return refer_norepeat
def dropsign(reference,signrefer):
    '''
    delete signrefer from reference
    :param reference: a str
    :param signrefer: a str
    :return: reference without signrefer
    '''
    for sign in signrefer:
        reference=reference.replace(sign,'')
    return reference
def scoring(reference,echo11,echo21,echo12,echo22,sr):
    '''
    score reference based on echo11,echo21 using precious match and on echo12,echo22 using fuzzy match
    :param reference: a str
    :param echo11: a list
    :param echo21: a list
    :param echo12: a list
    :param echo22: a list
    :param sr: similarity rate
    :return: score of reference
    '''
    sorce=0
    sorce1=3
    sorce2=1
    sorce3=0
    if reference==[]:
        sorce3=0
    else:
        #先精确匹配
        reference=''.join(reference).replace('\n','')
        refer=reference
        prerefer=[]#存放精确匹配的编制规则
        for echo in echo11:
            if echo in refer:
                sorce1=sorce1+1
                prerefer.append(echo)
                refer=refer.replace(echo, '')
                if sorce1>=5:
                    sorce1=5
        for echo in echo21:
            if echo in refer:
                sorce2=2
                prerefer.append(echo)
                refer=refer.replace(echo, '')
        refer=dropsign(reference, prerefer) #把精确匹配了的编制规则删除
        newrefer=readrefer(refer)#提出带书名号的编制规则
        if newrefer==[]:
            print("find no reference with 《》")
        if newrefer != []:
            simi1=[]
            for ref in newrefer:
                mostsimi1=process.extractOne(ref, echo12)
                simiratio1=mostsimi1[1]
                if simiratio1>sr:
                    simi1.append(simiratio1)
                    sorce1=sorce1+1
                    if sorce1>=5:
                        sorce1=5
            simi2=[]
            for ref in newrefer:
                mostsimi2=process.extractOne(ref, echo22)
                simiratio2=mostsimi2[1]
                if simiratio2>sr:
                    simi2.append(simiratio2)
                    sorce2=2
            if len(simi1)+len(simi2)<len(newrefer):
                sorce3=1
    if sorce1>3:
        sorce=sorce1
    if sorce1==3 and sorce2>1:
        sorce=sorce2+sorce3
    if sorce1==3 and sorce2==1:
        sorce=sorce3
    return sorce