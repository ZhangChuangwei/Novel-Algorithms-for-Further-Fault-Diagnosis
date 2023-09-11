import random

# node1 给 node2 发诊断信息(相当于是给 node2 自己的数据, 让 node2 测出自己的结果), node2 给 node1 发自己的诊断结果


def MLEC(node1, node2, Node_level=7):
    if node1.returnDF():
        return node2.returnLevel()
    else:
        return random.randint(0, Node_level)

