import random

import numpy as np
import pandas as pd
import math

# 列出所有的技术指标
EVALUATE = ['综合评分', '代码质量', '创新能力', '沟通能力', '文档完整程度', "粉丝数目", "技术广度"]


# 计算综合分
def calcul_comprehensive(*args, **kwargs):
    user = kwargs['user']
    if user:
        if user.fans:
            stu_me = [user.id, user.fans, len(user.demos)]  # 这是选出要展示的学生，三个数据分别是用户ID，用户粉丝数，用户发表demo数量
        else:
            stu_me = [user.id, 0, len(user.demos)]  # 这是选出要展示的学生，三个数据分别是用户ID，用户粉丝数，用户发表demo数量]
        stu = [stu_me, [5, 10, 9], [3, 9, 8], [13, 8, 8], [7, 7, 0], [2, 8, 1],
               [12, 17, 6], [9, 16, 5], [14, 5, 5], [6, 90, 3], [11, 8, 2],
               [8, 18, 2], [4, 15, 2], [15, 14, 1], [16, 1, 1], [17, 3, 1], [10, 2, 2]]  # 同理
        stu = pd.DataFrame(stu)  # 把它变成表
        stu.columns = ['id', 'fans', 'demos']  # 每个columns对应的keys
        stu.index = stu['id']  # 建立索引
        stu = stu[stu.columns[1:]]
        # 01标准化处理

        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()  # (0,1)标准化
        stu[['fans', 'demos']] = scaler.fit_transform(stu[['fans', 'demos']])
        # 计算熵和权
        yij = stu.apply(lambda x: x / x.sum(), axis=0)  # 第i个学生的第j个指标值的比重yij = xij/sum(xij) i=(1,m)
        K = 1 / np.log(len(stu))  # 一个常数
        tmp = yij * np.log(yij)
        tmp = np.nan_to_num(tmp)
        ej = -K * (tmp.sum(axis=0))  # 计算第j个指标的信息熵
        wj = (1 - ej) / np.sum(1 - ej)  # 计算第j个指标的权重
        # 在这里加自己定的权重随便调整wj啦，但没什么必要呢
        score = yij.apply(lambda x: np.sum(100 * x * wj * len(stu)), axis=1)  # 算分数，但这里是用标准化以后的数值算的，差距比较大
        return score[user.id]
    else:
        return 63 + random.randint(0, 15)


# 计算代码质量
def calcul_code_quality(*args, **kwargs):
    return 48 + random.randint(0, 12)


# 计算创新能力
def calcul_innovate(*args, **kwargs):
    return 54 + random.randint(2, 10)


# 计算沟通能力
def calcul_communication_skills(*args, **kwargs):
    return 51 + random.randint(0, 10)


# 计算文档完整程度
def calcul_document(*args, **kwargs):
    return 35 + random.randint(0, 15)


# 计算粉丝数目
def calcul_fans(*args, **kwargs):
    user = kwargs['user']
    if user:
        if user.fans:
            return 50+user.fans
        else:
            return 50

    return 50 + random.randint(0, 8)


# 计算技术广度
def calcul_technology_breadth(*args, **kwargs):
    return 63 + random.randint(0, 2)


CAL_EVALUATE = [calcul_comprehensive, calcul_code_quality, calcul_innovate,
                calcul_communication_skills, calcul_document, calcul_fans,
                calcul_technology_breadth]
