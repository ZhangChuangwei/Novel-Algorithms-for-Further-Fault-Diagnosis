import random
from utils.MLEC import MLEC
from utils.PMC import PMC

# Returns the set of diagnosed faultless vertices
def paper1(network, algo_return_H_num, level=0): 
    cur_return_H_num = 0
    faultFreeSet = p1_decFaultFree(network)
    H_good_numNodeList = Algorithm2(network, faultFreeSet, algo_return_H_num)
    return H_good_numNodeList

def p1_decFaultFree(network):
    faultFreeSet = []
    bad_list=[]
    # print(f'len(network.G_AN_H) is {len(network.G_AN_H)}')
    for node in network.G_AN_H:
        for AN_node_id in node.neighbors[1]:
                if AN_node_id in bad_list:
                    continue
                if Algorithm1(network.all_node[AN_node_id], node):
                    for node_id in network.all_node[AN_node_id].neighbors[1]:
                        if not Algorithm1(network.all_node[AN_node_id], network.all_node[node_id]):
                            bad_list.append(AN_node_id)
                            break
                    if AN_node_id in bad_list: continue
                #if network.AN[AN_node_id].returnDF():
                    if network.all_node[AN_node_id] not in faultFreeSet:
                        faultFreeSet.append(network.all_node[AN_node_id])
                else:
                    bad_list.append(AN_node_id)
                    if network.all_node[AN_node_id] in faultFreeSet:
                        faultFreeSet.remove(network.all_node[AN_node_id])

    true_FaultFreenum = 0
    for node in faultFreeSet:
        if node.detection_function:
            true_FaultFreenum+=1
    # print(f'true_FaultFreenum is {true_FaultFreenum}')
    # print(f'FaultFree num ratio is {true_FaultFreenum/len(faultFreeSet)}')
    print(f'true_FaultFreenum is: {true_FaultFreenum} \
          FaultFree num ratio is: {true_FaultFreenum/len(faultFreeSet)}')

    print(f'H remain all degree is: {network.H_all_degree}\
            AN remain all degree is: {network.AN_all_degree}')

    return faultFreeSet

def Algorithm1(AN_node, node):
    if MLEC(AN_node, node)!=node.level:
        return False
    # 碰巧撞上或者这个节点真的好
    return True

def Algorithm2(network, faultFreeSet, algo_return_H_num):
    # find the fault free set of H
    H_good_numNodeList = []
    for node in faultFreeSet:
        for node_id in node.neighbors[0]:
            network.all_node[node_id].status = 1
            if PMC(node, network.all_node[node_id]) == 0 and network.all_node[node_id] not in H_good_numNodeList:
                network.all_node[node_id].dec_level = 0
                H_good_numNodeList.append(network.all_node[node_id])
                # if len(H_good_numNodeList) >= algo_return_H_num:
                #     return H_good_numNodeList

    if len(H_good_numNodeList) == 0:
        raise ValueError('H_good_numNodeList is empty')
    if len(H_good_numNodeList) < algo_return_H_num:
        print('algo_return_H_num is larger than the number of good nodes')
        algo_return_H_num = len(H_good_numNodeList)
    choose_H_good_numNodeList = random.sample(H_good_numNodeList, algo_return_H_num)
    true_goodnum = 0
    for node in H_good_numNodeList:
        if node.level == 0:
            true_goodnum+=1
    print(f'true_goodnum is: {true_goodnum}\
            good num ratio is: {true_goodnum/len(H_good_numNodeList)}')

    return choose_H_good_numNodeList