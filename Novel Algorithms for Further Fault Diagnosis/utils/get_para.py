# 第二版重构代码后的参数获取模块

# 返回网络的参数指标
# 返回网络中的相关数据, 例如检测率, 精准率, 准确率

def return_para(self):
    accuracy, precision, recall = cal_apr(self)
    parameters = [  cal_score(self),
                    decConnectedSpace(self),
                    accuracy,
                    precision,
                    recall,
                    self.H_nodes_num,
                    self.H_good_num,
                    self.H_degree,
                    self.AN_nodes_num,
                    self.AN_decGood_num,
                    self.AN_degree,
                    self.G_AN_H_nodes_num,
                    self.g_goodN,
                    self.Node_level
                ]
    return parameters



def cal_score(self): # 检测率
    num_node_dec = 0
    for node in self.H:
        if node.status == 1:
            num_node_dec+=1

    return (num_node_dec) / (len(self.H))

def cal_apr(self):
    # 2023年07月09日01:07:36 get_para 的意义只用于一个网络对所有的点的仿真
    # 好像不存在把好点当成是坏点的情况, 所以 FN 为 0, 所以 recall = 1 始终
    #TP:被模型预测为正类的正样本
    # TN:被模型预测为负类的负样本
    # FP:被模型预测为正类的负样本
    # FN:被模型预测为负类的正样本, 这里 FN >0 是因为 H 中坏点被认为是好点, 所以在判定好点的时候, 会认为好点是坏点导致出现的 FN
    TP = TN = FP = FN = 0

    num = 0
    for node in self.H:
        if node.status == -1:
            continue # 未被检测, 不列入指标计算情况
        # num+=1
        if node.level ==0:
            if node.dec_level == 0:
                TP+=1
            else:
                # UndecGood+=1
                FN+=1
        else:
            if node.dec_level == 0:
                FP+=1
            else:
                TN+=1
    # print(num)
    print("TP, TN, FP, FN: ", TP, TN, FP, FN) # FN 是0
    accuracy = (TP + TN) / (TP + TN + FP + FN) #精准率 
    precision = TP / (TP + FP) #准确率
    recall = TP / (TP + FN) #召回率

    return accuracy, precision, recall


def decConnectedSpace(self): #for H network, H 的连通度
    connected_space_num = 0
    dectected_good_nodeid_list = []
    cur_list = []
    for node in self.faultFreeSetH:
        if node.node_id in dectected_good_nodeid_list:
            continue
        cur_list.append(node)
        while(len(cur_list)):
            cur_node = cur_list[0]
            cur_list.remove(cur_node)
            for nei_node_id in cur_node.neighbors[0]:
                if nei_node_id not in self.faultFreeSetHids:
                    continue
                if self.H[nei_node_id] in cur_list:
                    continue
                if nei_node_id not in dectected_good_nodeid_list:
                    cur_list.append(self.H[nei_node_id])
                    dectected_good_nodeid_list.append(nei_node_id)
        connected_space_num+=1
    return connected_space_num


def get_degree(l:list):
    sum_degree = 0
    for node in l:
        sum_degree+=node.degree
    return sum_degree

