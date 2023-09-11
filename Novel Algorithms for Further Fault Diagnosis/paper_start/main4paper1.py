# The main file pertains to the paper.
# Novel Algorithms for Further Fault Diagnosis

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import pandas as pd
from Algorithm.paper1 import paper1

from network.Network1 import Network1
from utils.get_para import return_para
from utils.pmcDecNet import PMC_decNet
from utils.calSelfTec import selfTec


if __name__ == '__main__':
    
    # Just adjust the parameter settings here
    para_list = []
    # Parameter settings
    cur_net = Network1 # The RGN(Randomly Generated Network) network is currently selected
    times = 5 # The number of times the experiment is repeated for each network
    cur_algorithm = paper1   # Which detection algorithm is currently selected
    algo_return_H_num = 20 # The current algorithm needs to return several good H points, because one faultless vertex may not be enough

    # Set the parameters for generating the network
    test_or_not = False # Set to False when running officially, and set to True to simply test whether the code runs smoothly. When set to True, the number of vertices in the network will be reduced to facilitate quick testing.


    if test_or_not:
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
        = 1000,         400,        25,         2000,           30,              25,        5000,          7,        6
        parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num],
                          [G_AN_H_nodes], [Node_level, g_goodN]]
        para_list.append(parameters_tmp)
        # Node level is the Diagnosis level for the MLPMC model.

    else:
        # In the 1st subgroup, the number of vertices with intact diagnosis capability in AN is manipulated.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     250,        25,         2000,           3,              25,        5000,           7,        6
        # Try adding variables yourself in each for loop
        for i in range(10):
            parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num + i*5, AN_degree_num],
                        [G_AN_H_nodes], [Node_level, g_goodN]]
            para_list.append(parameters_tmp)

        # In the 2nd subgroup, the number of faultless vertices in H is manipulated.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     100,        25,         2000,           30,              25,        5000,          7,        6
        for i in range(10):
            parameters_tmp = [[H_nodes_num, H_good_num + i*30, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num],
                            [G_AN_H_nodes], [Node_level, g_goodN]]
            para_list.append(parameters_tmp)

        # In the 3rd subgroup, the degree of vertices in AN is manipulated.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     250,        25,         2000,           30,              15,        5000,           7,       6
        for i in range(10):
            parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num+i*3],
                            [G_AN_H_nodes], [Node_level, g_goodN]]
            para_list.append(parameters_tmp)

        # In the 4th subgroup, the degree of vertices in H is manipulated.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     250,        12,         2000,           30,            25,        5000,           7,        6
        for i in range(10):
            parameters_tmp = [[H_nodes_num, H_good_num, H_degree+i*3], [AN_nodes_num, AN_decGood_num, AN_degree_num],
                            [G_AN_H_nodes], [Node_level, g_goodN]]
            para_list.append(parameters_tmp)

        # In the 5th subgroup, the value of g for g-good-neighbor property is manipulated.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     250,        25,         2000,           30,              25,        5000,           7,        3
        for i in range(10):
            parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num],
                            [G_AN_H_nodes], [Node_level, g_goodN+i*5]]
            para_list.append(parameters_tmp)

    # Follow the entire process.
    for parameters in para_list:
        # Each set of parameters retains a csv file
        paraList = []
        time_string = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        for i in range(times):
            print("***********************************************************************************")
            print("第"+str(i)+"次 Net")
            # start core running module!
            network = cur_net(parameters) # Generate the network. Here we only generate the network and do not detect it
            # network = selfTec(network, p2_algo3, network.Node_level)
            good_H_list = cur_algorithm(network, algo_return_H_num, network.Node_level) # A list, the standard configuration of the RGN is to use the new algorithm to diagnose faultless H vertices, and then use PMC to internally propagate in H
            network = PMC_decNet(network, good_H_list) # Use the PMC algorithm to pass through the diagnosed vertices and then diagnos the subnetwork H
            net_para = return_para(network)# Return some diagnosed parameters
            paraList.append(net_para)
            # end core running module!

        names = ["H_score", "H_connected_space", "accuracy", "precision", "recall", "H_nodes", "H_goodnodes", "H_averageNodeDegree",
                "AN_nodes", "AN_goodDecGene", "AN_nodeEdge", "AN_averageDegree",
                "G_AN_H_nodes", "node_level"]
        result = pd.DataFrame(columns=names, data=paraList)
        scores = result['H_score'] #H_score here means $\phi(G)=\frac{|R|}{|V(H)|-|R|}$;
        net_ave = scores.mean()
        net_max = scores.max()
        net_min = scores.min()
        net_med = scores.median()
        net_std = scores.std()

        accuracy_score = result['accuracy']
        acc_ave = accuracy_score.mean()
        acc_max = accuracy_score.max()
        acc_min = accuracy_score.min()
        acc_med = accuracy_score.median()


        H_c_s = result['H_connected_space'].mean()
        result.loc[times+1] = {'H_score': ""} #Here times+1 is the statistical data added at the end. Each parameter has one statistical data.
        result.loc[times+2] = {'H_score': "exp_times is: "+str(times)}
        result.loc[times+3] = {'H_score': "ave_score is: "+str(net_ave)}
        result.loc[times+4] = {'H_score': "max_score is: "+str(net_max)}
        result.loc[times+5] = {'H_score': "min_score is: "+str(net_min)}
        result.loc[times+6] = {'H_score': "median_score is: "+str(net_med)}
        result.loc[times+7] = {'H_score': "std_score is: "+str(net_std)} #Std
        result.loc[times+8] = {'H_score': "ave_connected_space is: "+str(H_c_s)} #mean value of connectivity
        result.loc[times+9] = {'H_score': "ave_accuracy is: "+str(acc_ave)}
        result.loc[times+10] = {'H_score': "max_accuracy is: "+str(acc_max)}
        result.loc[times+11] = {'H_score': "min_accuracy is: "+str(acc_min)}
        result.loc[times+12] = {'H_score': "median_accuracy is: "+str(acc_med)}

        time_string1 = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        excel_name = time_string1+" Net Repeat "+str(times)+" times.xlsx"
        script_path = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(script_path, '..', 'experiment_result', excel_name)
        result.to_excel(save_path)
        print("***********************************************************************************")
        print('----------------------- The final result of the statistics. -----------------------')
        print("***********************************************************************************")
        print("%d times' average dec score: %f "%(times, net_ave)) 
        print(f"max score {net_max:.6f} \
                min score {net_min:.6f} ")
        print(f"median score {net_med:.6f} \
                std score {net_std:.6f} ")
        print(f"average accuracy: {acc_ave:.6f} ")
        print(f"max accuracy: {acc_max:.6f} \
                min accuracy: {acc_min:.6f} ")
        print(f"median accuracy: {acc_med:.6f} ")
