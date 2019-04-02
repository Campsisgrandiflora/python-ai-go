import pickle
from app.models import Demand, Demo
import jieba.analyse
from app import app
from app.ext.ext import remove_tag,change_list_to_dic

jieba.analyse.set_stop_words(app.static_folder+'/keyword/'+'stopword.txt')
jieba.load_userdict(app.static_folder+'/keyword/'+'ai.txt')

demands = Demand.query.all()
demos = Demo.query.all()

# with open(app.static_folder + '/keyword/' + 'demandkey.dat', 'rb') as file:
#     d = pickle.load(file)
# 将demand文本+标题提取关键词 转换成字典存储
d = {}
with open(app.static_folder + '/keyword/' + 'demandkey.dat', 'wb') as file:

    for demand in demands:
        txt = remove_tag(demand.description+demand.name)
        keywordlist = jieba.analyse.extract_tags(txt, topK=10, withWeight=True, allowPOS=('nz', 'n'))
        dic = change_list_to_dic(keywordlist)

        d[demand.id] = dic
    pickle.dump(d, file)


d = {}
# with open(app.static_folder + '/keyword/' + 'demokey.dat', 'rb') as file:
#     d = pickle.load(file)
# 将demo文本+标题提取关键词 转换成字典存储
with open(app.static_folder + '/keyword/' + 'demokey.dat', 'wb') as file:

    for demo in demos:
        txt = remove_tag(demo.description+demo.name)
        keywordlist = jieba.analyse.extract_tags(txt, topK=10, withWeight=True, allowPOS=('nz', 'n'))
        dic = change_list_to_dic(keywordlist)

        d[demo.id] = dic
    pickle.dump(d, file)

f = open(app.static_folder + '/keyword/' + 'demokey.dat', 'rb')
d = pickle.load(f)
f.close()
print(d)