from scipy.stats import norm
from scipy.stats import chi2

def quantile(data, value):
    '''
    search quantile of every value among data
    :param data: a list
    :param value: a float
    :return: quantile of every value among the data
    '''
    sort_data = sorted(data)
    if value not in data:
        print("%d is not in %s" %(value, data))
    else:
        value_order = sort_data.index(value) + 1
        quantile = value_order / len(sort_data)
    return quantile
def z_score(data, value):
    q = quantile(data, value) / 1.01
    z_score = norm.ppf(q, 0, 1)
    return z_score
def percentile_rank(data, value):
    '''transform value between 0 to 100 based on data using percentile rank method
    data is a list
    value is a float'''
    sort_data = sorted(data)  # 从小到大进行排序
    rank = sort_data.index(value) + 1
    percentile_rank = 100 - (100 * rank - 50) / len(data)
    return percentile_rank
def chi2_score(data, value):
    # rescale by z-score
    q = quantile(data, value) / 1.01
    chi2_score = 50 - chi2.ppf(q, 55)
    return chi2_score
def rescale(data):
    # rescale by z-score
    z = [z_score(data, i) for i in data]
    # rescale by percentile_rank
    pr = [percentile_rank(data, i) for i in data]
    # rescale by chi2
    chi2 = [chi2_score(data, i) for i in data]
    return z, pr, chi2