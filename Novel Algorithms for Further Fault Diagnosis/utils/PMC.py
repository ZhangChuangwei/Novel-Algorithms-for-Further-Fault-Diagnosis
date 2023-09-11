import random


def PMC(node1, node2):
    # 这个算法的主要作用是
    # 用 node1 检测 node2, 反馈出 node2 的检测能力是否有问题;
    # PMC 算法有一定可能性出现不好的结果, 因为设定的时候会认为 如果一个节点是个坏节点, 那么就会随机返回结果,这里采用 0 和 1

    if node1.returnDF():
        return 0 if node2.returnLevel() == 0 else 1
    else:
        return random.randint(0,1)
    