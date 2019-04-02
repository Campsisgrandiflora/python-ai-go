# 构建兴趣推荐的代码 ######################################################
from app.models import Demand, Demo, Tag, User, Enterprise


def interest_recommmand_demo(user):
    # 查出user的标签
    tags = user.tags.all()
    d = dict()
    dre = dict()
    # 对于每一个user的标签
    for user_tag in tags:
        for demo in user_tag.demos.all():
            if demo.id not in d.keys():
                dre[demo.id] = demo
                d[demo.id] = 1
            else:
                d[demo.id] += 1

    lis = sorted(d.items(), key=lambda x: x[1], reverse=True)[0:3]
    relis = []
    for i in lis[0:3]:
        relis.append(dre[i[0]])
    return relis


def interest_recommmand_demand(user):
    # 查出user的标签
    tags = user.tags.all()
    d = dict()
    dre = dict()
    # 对于每一个user的标签
    for user_tag in tags:
        for demand in user_tag.demands.all():
            if demand.id not in d.keys():
                dre[demand.id] = demand
                d[demand.id] = 1
            else:
                d[demand.id] += 1

    lis = sorted(d.items(), key=lambda x: x[1], reverse=True)[0:3]
    relis = []
    for i in lis[0:3]:
        relis.append(dre[i[0]])
    return relis


# for user in users:
# print(interest_recommmand(user))
# interest_recommmand(user)
if __name__ == '__main__':
    user = User.query.first()
    print(interest_recommmand_demo(user))
    enterprise = Enterprise.query.first()
    print(interest_recommmand_demand(enterprise))