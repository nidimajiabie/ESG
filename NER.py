from usualword import *

def NER(readpaths):
    '''
    remove spaces and line breaks from content in txt given readpath, select readpaths whose txt are null and
    part-of-speech tagging of content in txt
    :param readpaths:a list of str
    :return:three lists: contents in txt without spaces and line breaks, readpaths whose txt are null, tagging of contents in txt
    '''
    wenbens=[]#输出list
    nulls=[]#输出为空的文件路径
    NERs=[]#输出分词结果
    lac = LAC(mode='lac')
    for readpath in readpaths:
        f=open(readpath,'r',encoding='utf-8')
        wenben=f.read()
        f.close
        wenben=wenben.replace(' ','').replace('\n','').replace('\t','')
        #wenben=removePunct(wenben)
        if len(wenben)==0:
            nulls.append(readpath)
        wenbens.append(wenben)
        lac_result = lac.run(wenben)
        NER = lac_result
        NERs.append(NER)
    return wenbens,nulls,NERs
def NER_rate(NERs):
    '''
    calculate NERrate of each one of lac_result
    :param NERs: a list of str
    :return: three list: NERnums,NERrate and index which have no NER
    '''
    NERnums=[]
    NERrates=[]
    nulls=[]
    for i in range(0,len(NERs)):
        if len(NERs[i][1])==0:
            print('nothing in the %d text' % i)
            nulls.append(i)
            NERnum=0
            NERrate=-1
        else:
            NERnum=NERs[i][1].count('f')+NERs[i][1].count('s')+NERs[i][1].count('nw')+NERs[i][1].count('nz')+NERs[i][1].count('m')\
                   +NERs[i][1].count('q')+NERs[i][1].count('PER')+NERs[i][1].count('LOC')+NERs[i][1].count('ORG')+NERs[i][1].count('TIME')
            NERrate=NERnum/len(NERs[i][1])
        NERnums.append(NERnum)
        NERrates.append(NERrate)
    return NERnums,NERrates,nulls
