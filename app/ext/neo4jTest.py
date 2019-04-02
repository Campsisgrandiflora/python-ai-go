from py2neo import Graph, Node, Relationship, walk, types
import sys

test_graph = Graph(
    'http://localhost:7474',
    username="neo4j",
    password="lkj123"
)

find_code_1 = test_graph.find_one(
    label="label",
    property_key="id",
    property_value="1"
)

find_code_3 = test_graph.find_one(
    label="label",
    property_key="id",
    property_value="2"
)

# print(find_code_1['name'])
find_all = test_graph.find(
    label="label"
)

find_relationship = test_graph.match()

print(find_relationship)
# for i in find_all:
#     print(i)
# for item in walk(test_graph):
#     print(item)
# while True:
#     try:
#         rel = find_all.__next__()
#         # rel = types.Relationship
#         print(rel['name'])
#     except StopIteration:
#         sys.exit()

for i in find_all:
    print(i)


while True:
    try:
        rel = find_relationship.__next__()
        # rel = types.Relationship
        print("开始节点:"+str(rel.start_node()['name']))
        print("结束节点:"+str(rel.end_node()['name']))
    except StopIteration:
        sys.exit()
