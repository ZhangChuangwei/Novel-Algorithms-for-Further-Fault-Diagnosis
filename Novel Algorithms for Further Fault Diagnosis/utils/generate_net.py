# from utils.decorator import silent_print
import random

def add_neibor_2lst(network, lista, listb, x:int, anet:int, bnet:int, name):
    '''
        输入第一个是 network, 需要把修改的数据传递出去;
        输入是两个网络, 两个网络互相添加邻居, 这个是随机带来的;
        anet 表示 lista 是哪个网络
        x 的意思就是, 两个网络之间的连接数目, 如果是相同网络, 需要除以 2, 如果是不同网络就不需要
    '''
    assert x>0, "两个网络之间的连接数目 必须大于 0"

    if anet == bnet:
        x = x//2

    # print(network.H_all_degree, network.AN_all_degree, network.G_AN_H_all_degree)

    la = lista.copy()
    lb = listb.copy() # copy list, avoid change the original list
    xm = min(int(2 * x), len(la) * len(lb)) # 因为还有一些容错, 不采用全集采用 min是为了节省时间
    pairs = select_pairs(la, lb, xm)
    # random.shuffle(pairs)
    success = 0

    for pa, pb in pairs:
        status = add_neibor(network, pa, pb, anet, bnet)
        if status:
            success += 1
            if success >= x:
                break

    if success < x:
        # AN 加不满没事儿, H 中的点必须加满
        # print(f"{name} 只能添加 {success} 个邻居, 还有 {x-success}的邻居没有添加上")
        # 这个没加满的原因常见的是度和节点数量分配的不合理, 以后再优化吧,问题不大
        pass
    # print(network.H_all_degree, network.AN_all_degree, network.G_AN_H_all_degree)
    # print('------------------------------')
    return None
    


def select_pairs(la, lb, x):
    # 检查是否有足够的配对来选择 x 个
    # 耗时太长了
    if x > len(la) * len(lb):
        return "无法选择这么多配对"

    available_pairs = [(a, b) for a in la for b in lb]
    selected_pairs = random.sample(available_pairs, x)

    return selected_pairs


def add_neibor(network, nodea, nodeb, anet:int, bnet:int):
    '''
        这个函数里实现了:
        1. 两个节点之间的判断
        2. 两个节点之间的连接
        3. 网络和节点的度进行了删减
    '''

    # 双向邻居, 不存在单边邻居的情况
    assert anet in [0,1] and bnet in [0,1,2], \
    f"anet的值必须在 [0,1] 范围内, bnet 值必须在 [0,1,2]，但现在的值是 anet={anet}, bnet={bnet}"

    if nodea.node_id == nodeb.node_id:
        # print("不能添加自己为邻居")
        return False

    # 节点的度必须大于0
    if nodea.degree <= 0 or nodeb.degree <= 0:
        if nodea.degree >0 and bnet ==2:
            pass
        else:
            return False
        # print('节点度必须大于 0')
        # print(f'nodea.degree = {nodea.degree}, nodeb.degree = {nodeb.degree}')

    # 两个节点之前就是邻居 就 return False
    if nodeb.node_id in nodea.neighbors[bnet]:
        # print('两个节点之前就是邻居')
        return False

    nodea.addNeighbor(nodeb.graph_id, nodeb.node_id)
    nodeb.addNeighbor(nodea.graph_id, nodea.node_id)

    nodea.degree -= 1
    nodeb.degree -= 1

    # 只计算 AN 和 H 中的度, G-AN-H 就 pass 掉
    # 这里不能用赋值来做, 因为这里的 a_degree 和 b_degree 是数字, 只能通过 network的引用来实现数字的修改

    if anet == 0:
        network.H_all_degree -=1
    else:
        network.AN_all_degree -=1

    if bnet == 0:
        network.H_all_degree -=1
    elif bnet == 1:
        network.AN_all_degree -=1
    else:
        network.G_AN_H_all_degree -=1
    return True 