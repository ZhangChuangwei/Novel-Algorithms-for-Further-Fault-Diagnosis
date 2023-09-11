
import random
from Node.Node import Node
from utils.reload import *


def randomGenerateNetForDecGood(self): #generate network for dec_good node only, satisfy good neiborhor
    self.faultFreeSetH = []
    self.faultFreeSetHids = []

    # print("正在形成H_Good节点")
    # 这一步用 random.sample(range(0, 20), 20) 来做会更简洁
    H_ids = []
    for i in range(self.H_nodes_num):
        H_ids.append(i)
    while(len(self.faultFreeSetHids) != self.H_good_num):
        i = random.randint(0, len(H_ids)-1)
        node_id = H_ids[i]
        node = Node(node_id=node_id, level=0, detection_function=True, goodN=self.g_goodN, degree=-1, graph_id=0)
        self.H.append(node)
        self.faultFreeSetH.append(node)
        self.faultFreeSetHids.append(node_id)
        H_ids.remove(node_id)
    # 这个循环是: 在图G_AN_H中, 全部作为好点 , 进行建模

    # print("正在形成G_AN_H中节点")
    start_node_id = self.H_nodes_num + self.AN_nodes_num
    end_node_id = start_node_id + self.G_AN_H_nodes_num

    for index in range(start_node_id, end_node_id):
        node = Node(node_id=index, level=0, detection_function=True, goodN=self.g_goodN, degree=-1, graph_id=2)
        self.G_AN_H.append(node)
    # 在这些点中, 满足邻接好点 = g_goodNeighbor的条件
    # 改版的网络结构要求是: 网络H 和 网络G_AN_H中所有有完整功能的点都需要有至少g个邻接节点
    # AN中所有的点都是有不同程度的损坏, 唯一的区别就是有的点 检测能力没有坏, 对检测能力没有坏的节点, 并没有g_goodN(g个好邻节点)的要求

    #这里是对H中好的点进行条件满足: 要有g_goodN
    # print("正在让H中的好点满足g_goodN")
    # 注意, H中好点的goodN是在内部的寻找好的节点, 因为AN所有节点都是坏的, 只不过有些检测能力没有坏而已.
    #我们做不到每个节点恰好googN, 生成的结果是>=, 含等于
    for node in self.faultFreeSetH:
        remain_listH = reloadListrandomGenerateNetForDecGood(self)[0]
        remain_listH.remove(node)
        while(node.g_goodN>0):
            list1size = len(remain_listH)
            nodeN = remain_listH[random.randint(0, list1size - 1)]
            while(nodeN.node_id in node.neighbors[nodeN.graph_id]):
                remain_listH.remove(nodeN)
                list1size = len(remain_listH)
                nodeN = remain_listH[random.randint(0, list1size - 1)]

            node.addNeighbor(nodeN.graph_id, nodeN.node_id)
            node.g_goodN -=1
            nodeN.addNeighbor(0, node.node_id)
            nodeN.g_goodN-=1
            self.H_all_degree -=2

    # 对G_AN_H中所有的点, 满足g_goodN
    # print("正在让G_AN_H满足g_goodN")
    for node in self.G_AN_H:
        remain_listG_ = reloadListrandomGenerateNetForDecGood(self)[1]
        remain_listG_.remove(node)
        while(node.g_goodN>0):
            list2size = len(remain_listG_)
            nodeN = remain_listG_[random.randint(0, list2size - 1)]
            while(nodeN.node_id in node.neighbors[nodeN.graph_id]):
                remain_listG_.remove(nodeN)
                list2size = len(remain_listG_)
                nodeN = remain_listG_[random.randint(0, list2size - 1)]

            node.addNeighbor(nodeN.graph_id, nodeN.node_id)
            node.g_goodN -=1
            nodeN.addNeighbor(2, node.node_id)
            nodeN.g_goodN-=1
    # 至此, 所有的检测好的点都完成了 g_neighbor的要求
