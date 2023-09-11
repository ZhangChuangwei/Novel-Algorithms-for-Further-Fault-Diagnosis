import random


def distribute1(degree_sum, part_num, covariance):
    '''
        这个函数的作用是相当于 给总共要分配的度的数量以及要平摊到每个点都多少个度的情况
    '''
    result = []
    for i in range(part_num):
        result.append(max(6, int(random.normalvariate(degree_sum/part_num, covariance)))) #保证下限
    cur_sum = sum(result)
    # 这个就是超出result的长度
    if cur_sum > degree_sum:
        diff = cur_sum-degree_sum
        k = int(diff/part_num)
        remain = diff%part_num
        for i in range(part_num):
            if i < remain:
                result[i] -=(1+k)
            else:
                result[i] -= (k)
    elif cur_sum < degree_sum:
        diff = degree_sum-cur_sum
        k = int(diff/part_num)
        remain = diff%part_num
        for i in range(part_num):
            if i < remain:
                result[i] +=(1+k)
            else:
                result[i] += (k)
    return result


def distribute(degree_sum, part_num, covariance):
    '''
        这个函数的作用是相当于给总共要分配的度的数量以及要平摊到每个点都多少个度的情况
    '''
    result = [max(6, int(random.normalvariate(degree_sum / part_num, 
                                              covariance))) for _ in range(part_num)]
    diff = sum(result) - degree_sum
    k, remain = divmod(abs(diff), part_num)
    adjustment = [k + 1 if i < remain else k for i in range(part_num)]
    
    # 根据差异调整结果
    if diff > 0:
        result = [r - a for r, a in zip(result, adjustment)]
    else:
        result = [r + a for r, a in zip(result, adjustment)]
        
    return result