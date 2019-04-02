from app import app
# 生成一个知识图谱 输入为图谱名称id
def generate_graph(id):
    import csv
    # 读取csv文件
    with open(app.static_folder + '/keyword/' + str(id)+'.csv') as f:
        reader = csv.reader(f)
        lis = list(reader)[1:]
        nodes = [{"name": l[1]} for l in lis]
    with open(app.static_folder + '/keyword/' + str(id) +'r.csv') as f:
        reader = csv.reader(f)
        lisref = list(reader)[1:]
        edges = [{"source": int(e[0]) - 1, "target": int(e[1]) - 1} for e in lisref]
    return nodes, edges