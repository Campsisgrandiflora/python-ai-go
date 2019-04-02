import math
import pickle
from app import app
from app.models import Demo, Demand


def calculate(a, b, ab):
    if ab == 0: return 0
    return ab / math.sqrt(a) / math.sqrt(b)


def matchDemo(demandid):
    dic = dict()
    with open(app.static_folder + '/keyword/' + 'demandkey.dat', 'rb') as file:
        d = pickle.load(file)
    demandic = d
    d = {}
    with open(app.static_folder + '/keyword/' + 'demokey.dat', 'rb') as file:
        d = pickle.load(file)
    demodic = d
    d = {}

    for i in demodic.keys():
        # print(demandic[i])
        set1 = set(demodic[i].keys())
        set2 = set(demandic[demandid].keys())
        set3 = set1.union(set2)

        ab = 0
        a = 0
        b = 0
        for word in set3:
            if word in set1 and word in set2:
                ab = ab + demodic[i][word] * demandic[demandid][word]
            elif demodic[i].get(word):
                a = a + demodic[i].get(word) ** 2
            elif demandic[demandid].get(word):
                b = b + demandic[demandid].get(word) ** 2

        dic[i] = calculate(a, b, ab)
    """
    对字典的值进行排序，并返回元组列表
    返回形式如[(3, 0.04214559058181912), (1, 0.0878747280663184), (2, 1.1113993263441402)]
    """
    lis = sorted(dic.items(), key=lambda x: x[1], reverse=True)[0:3]
    # print(lis[0:3])
    return lis
    # print(d)


d = {}
# 将demand匹配到的demo写入文件
for demand in Demand.query.all():
    d[demand.id] = matchDemo(demand.id)
with open(app.static_folder + '/keyword/' + 'redemandlist.dat', 'wb') as file:
    pickle.dump(d, file)


def matchDemand(demoid):
    dic = dict()
    with open(app.static_folder + '/keyword/' + 'demandkey.dat', 'rb') as file:
        d = pickle.load(file)
    demandic = d
    d = {}
    with open(app.static_folder + '/keyword/' + 'demokey.dat', 'rb') as file:
        d = pickle.load(file)
    demodic = d
    d = {}

    for i in demandic.keys():
        # print(demandic[i])
        set1 = set(demodic[demoid].keys())
        set2 = set(demandic[i].keys())
        set3 = set1.union(set2)

        ab = 0
        a = 0
        b = 0
        for word in set3:
            if word in set1 and word in set2:
                ab = ab + demodic[demoid][word] * demandic[i][word]
            elif demodic[demoid].get(word):
                a = a + demodic[demoid].get(word) ** 2
            elif demandic[i].get(word):
                b = b + demandic[i].get(word) ** 2

        dic[i] = calculate(a, b, ab)
    """
    对字典的值进行排序，并返回元组列表
    返回形式如[(3, 0.04214559058181912), (1, 0.0878747280663184), (2, 1.1113993263441402)]
    """
    lis = sorted(dic.items(), key=lambda x: x[1], reverse=True)[0:3]
    # print(lis[0:3])
    return lis


d = {}
# 将demo匹配到的demand写入文件
for demo in Demo.query.all():
    d[demo.id] = matchDemand(demo.id)
with open(app.static_folder + '/keyword/' + 'redemolist.dat', 'wb') as file:
    pickle.dump(d, file)

with open(app.static_folder + '/keyword/' + 'redemolist.dat', 'rb') as file:
    d = pickle.load(file)
    print(d)

with open(app.static_folder + '/keyword/' + 'redemandlist.dat', 'rb') as file:
    d = pickle.load(file)
    print(d)
