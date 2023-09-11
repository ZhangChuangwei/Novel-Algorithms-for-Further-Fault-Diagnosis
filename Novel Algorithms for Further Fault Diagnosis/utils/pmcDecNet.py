

from utils.PMC import PMC

def PMC_decNet(network, good_H_list):
    # 用 pmc 算法传播检测 H 中的节点
    cur_good_list = good_H_list
    while(len(cur_good_list)):
        new_add_list = []
        for node in cur_good_list:
            #一个点要是没有被检测, 而且通过 PMC 检测是个好点, 就加入 new_add_list
            for node_id in node.neighbors[0]:
                if network.all_node[node_id].status == -1:
                    # 注意! 被坏点检测的时候也会被认为这个点已经检测过了,虽然得到不是正确结果
                    network.all_node[node_id].status = 1
                    if PMC(node, network.all_node[node_id]) == 0: #如果是未检测而且还是好点, 就加入
                        network.all_node[node_id].dec_level = 0
                        new_add_list.append(network.all_node[node_id])
                    else:
                        network.all_node[node_id].dec_level = -1 # PMC 不会出啥问题
        cur_good_list = new_add_list

    return network