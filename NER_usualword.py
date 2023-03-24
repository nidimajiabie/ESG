def NERusual_rate(NERrate,usualrate):
    '''
    calculate (rate of NER)/(rate of usualword)
    :param NERrate: a list
    :param usualrate: a list
    :return: a list
    '''
    NER_usual=[]
    for i in range(len(NERrate)):
        if NERrate[i]==-1 or usualrate[i]==0:
            NER_usual.append(-1)#分母为0，无法计算比值，记为-1
        else:
            NER_usual.append(NERrate[i]/usualrate[i])
    return NER_usual