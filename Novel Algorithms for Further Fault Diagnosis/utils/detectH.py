
# 这个函数的作用是, 我找到 H 中一个好的点 u, 利用这个好的点进行 PMC 算法的检测和传播

from utils.PMC import PMC

def detectH(self, u):

    self.H_good_numNodeList = [u]
    # self.H_good_numNodeList.append(u)
    u.status = 1

    #现在实验还有一个问题, 如果 u 是个错误的节点, 那么反馈出来的结果也是错的, 我们也可以做一个研究错误的指标, 就是在检测出来的这些点哪些是真实没问题的

    #可以显示两个指标, precision, accuracy

    while(len(self.H_good_numNodeList)):#当没有新的好点加入到集合中, 表示检测完毕了; 广度优先算法
        self.H_new_goodNodeList = [] #本轮检测出的好点的集合
        for node in self.H_good_numNodeList:
            for node_id in node.neighbors[0]:
                if self.H[node_id].status == -1:
                    if PMC(node, self.H[node_id]) == 0: #如果是未检测而且还是好点, 就加入; PMC这里是如果 node 有问题就会返回的是错误的结果;
                        self.H_new_goodNodeList.append(self.H[node_id])
        self.H_good_numNodeList = self.H_new_goodNodeList

