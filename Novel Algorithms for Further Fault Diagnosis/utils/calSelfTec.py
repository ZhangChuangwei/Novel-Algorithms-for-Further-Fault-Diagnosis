# 2023年07月09日01:20:05 专门用于自检测类型的算法, 通过 TP TN FP 和 FN 来计算相应的仿真指标


def selfTec(network, algorithm, l=7):
    '''
        network 是指当前的网络
        algorithm 是指要进行自检测的算法
    '''
    for node in network.H:
        algorithm(network, node, network.Node_level)

    return network