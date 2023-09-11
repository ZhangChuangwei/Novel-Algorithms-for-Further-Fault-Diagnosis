# Here we generate the RGN(Randomly Generated Network)
# The vertex in AN has at least one neighbor in H and another in G-AN-H
import random

from Node.Node import Node
from utils.randomGenerateNetForDecGood import randomGenerateNetForDecGood
from utils.distribute import distribute
from utils.reload import *


class Network1(object):
    def __init__(self, parameters):
        self.H_p = parameters[0] # graph_id = 0 H_p means H network related parameters
        [self.H_nodes_num, self.H_good_num, self.H_degree] = self.H_p
        self.H_all_degree = self.H_degree * self.H_nodes_num
        self.AN_p = parameters[1] # graph_id = 1
        [self.AN_nodes_num, self.AN_decGood_num, self.AN_degree] = self.AN_p
        self.AN_all_degree = self.AN_degree * self.AN_nodes_num

        self.G_AN_H_p = parameters[2] # graph_id = 2
        [self.G_AN_H_nodes_num] = self.G_AN_H_p

        self.node_p = parameters[3]
        [self.Node_level, self.g_goodN] = self.node_p

        self.H = []
        self.AN = []
        self.G_AN_H = []
        self.all_net = []
        #The naming order of the nodes here is H + AN + (G-AN-H), and this order is universal throughout the simulation

        #The methods we generate the network
        randomGenerateNetForDecGood(self) #When modeling edges between vertices, all networks are identical
        self.randomGenerateNetOthers() #The edges between the AN network and other vertices are tentatively the same.

        self.H.sort(key=lambda x:x.node_id)
        self.AN.sort(key=lambda x:x.node_id)
        self.G_AN_H.sort(key=lambda x:x.node_id)

        self.all_node = self.H + self.AN + self.G_AN_H
        print("Network Has Been Generated!")
        #Just import the algorithm you want to use here, just pass in "self".

        # See the output
        # printParameters(self)

    def randomGenerateNetOthers(self):
        # Step 0: Generate faulty vertices in H and add them to self.H
        #print("faulty vertices in H are being generated!")
        #for index in range(self.H_nodes_num):
        #    if index not in self.faultFreeSetHids:
        #        node = Node(node_id=index, level=1, detection_function=False, goodN=0, degree=-1, graph_id=0)
        #        self.H.append(node)

        # Step 1: Each vertex in AN need to have an edge with that in G-AN-H
        # 1.1 select which vertex in AN with intact diagnosis capability.
        self.faulFreeSetAN = []
        self.faulFreeSetANids = []
        AN_ids = []

        start_node_id = self.H_nodes_num
        end_node_id = start_node_id + self.AN_nodes_num

        for index in range(start_node_id, end_node_id):
            AN_ids.append(index)

        # print("Vertices in AN with intact diagnosis capability in AN are being generated and their neighbors in G_AN_H are being arranged.")
        while(len(self.faulFreeSetANids) != self.AN_decGood_num):
            i = random.randint(0, len(AN_ids)-1)
            node_id = AN_ids[i]
            node = Node(node_id=node_id, level=random.randint(1, self.Node_level), detection_function=True, goodN=0, degree=0, graph_id=1) #There is no requirement for the number of faultless neighbors it has
            self.AN.append(node)
            self.faulFreeSetAN.append(node)
            self.faulFreeSetANids.append(node_id)
            rangeJ = random.randint(0, len(self.G_AN_H)-1)
            node.addNeighbor(2, self.G_AN_H[rangeJ].node_id)
            self.AN_all_degree -=1
            self.G_AN_H[rangeJ].addNeighbor(1, i)
            AN_ids.remove(node_id)

        #1.2 The remaining vertices in AN that have not been selected are those with no diagnosis capability.
        # print("Vertices with no diagnosis capability in AN are being randomly generated as neighbors and their neighbors in G_AN_H being arranged.")
        for node_id in AN_ids:
            node = Node(node_id = node_id, degree=0, detection_function=False, goodN=0, level=random.randint(1, self.Node_level), graph_id=1)
            self.AN.append(node)
            rangeJ = random.randint(0, len(self.G_AN_H)-1)
            node.addNeighbor(2, rangeJ)
            self.G_AN_H[rangeJ].addNeighbor(1, node_id)
        self.AN_all_degree -= self.AN_nodes_num# Because every vertex in AN needs to be connected to G_AN_H, just subtract one first

        for index in range(self.H_nodes_num):
            if index not in self.faultFreeSetHids:
                node = Node(node_id=index, degree=-1, detection_function=False, goodN=0,
                            level=1, graph_id=0)
                self.H.append(node)

        # print("Let a certain vertex in H have an edge with a vertex in AN")
        # Start looking for neighbors
        rangeI = random.randint(0, len(self.H)-1)
        rangeJ = random.randint(0, len(self.AN) - 1)
        node = self.H[rangeI]
        node.addNeighbor(1, rangeJ)
        self.AN[rangeJ].addNeighbor(0, node.node_id)
        self.AN_all_degree -= 1
        self.H_all_degree -= 1

        # Step 3:  Divide all degrees, ideally a normal distribution
        # print("The degree of the vertex of AN is being divided")
        an_degree = distribute( degree_sum=self.AN_all_degree, part_num=self.AN_nodes_num, covariance=self.AN_all_degree/self.AN_nodes_num/5)
        for index in range(self.AN_nodes_num):
            self.AN[index].degree = an_degree[index]

        # Step 4: Let H complete the degree distribution(if the 5th step is after the 4th step, then the degree in AN has been consumed, and the remaining degree of H can only be digested internally. In this case, the degree distribution pool could be empty, so let H be the first and then AN.

        for node in self.AN:
            AN_nei_candidate_list = reloadANinnerNeighbor(self, node)
            try:
                cur_node_num = 3
                if node.degree<cur_node_num:
                    continue
                while(cur_node_num):
                    rangeJ = random.randint(0, len(AN_nei_candidate_list)-1)
                    nodeN = AN_nei_candidate_list[rangeJ]
                    # Find a suitable neighbor again
                    while((nodeN.degree == 0) or nodeN.node_id in node.neighbors[nodeN.graph_id]):#In G_AN_H, the degree starts from -1 and can never be 0 because it has to keep decreasing.
                        AN_nei_candidate_list.remove(nodeN)
                        rangeJ = random.randint(0, len(AN_nei_candidate_list)-1)
                        nodeN = AN_nei_candidate_list[rangeJ]

                    if nodeN.graph_id == 0:
                        node.addNeighbor(0, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                        self.H_all_degree-=1
                    if nodeN.graph_id == 1:
                        node.addNeighbor(1, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                        self.AN_all_degree-=1
                    if nodeN.graph_id == 2:
                        node.addNeighbor(2, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                    self.AN_all_degree-=1
                    node.degree -=1
                    cur_node_num -=1
                    nodeN.degree-=1
            except:
                pass
        # print("Dividing degrees for H")
        h_degree = distribute(degree_sum=self.H_all_degree, part_num=self.H_nodes_num, covariance=self.H_all_degree/self.H_nodes_num/5)
        for index in range(self.H_nodes_num):
            self.H[index].degree = h_degree[index]
        #print("Let the nodes in H find suitable neighbor nodes")
        for node in self.H:
            H_nei_candidate_list = reloadHneighbor(self, node)
            while(node.degree>0):
                rangeJ = random.randint(0, len(H_nei_candidate_list)-1)
                nodeN = H_nei_candidate_list[rangeJ]
                # Find a suitable neighbor again
                while((nodeN.degree == 0) or nodeN.node_id in node.neighbors[nodeN.graph_id]):#In G_AN_H, the degree starts from -1 and can never be 0 because it has to keep decreasing.
                    H_nei_candidate_list.remove(nodeN)
                    rangeJ = random.randint(0, len(H_nei_candidate_list)-1)
                    nodeN = H_nei_candidate_list[rangeJ]

                if nodeN.graph_id == 0:
                    node.addNeighbor(0, nodeN.node_id)
                    nodeN.addNeighbor(0, node.node_id)
                    self.H_all_degree-=1
                if nodeN.graph_id == 1:
                    node.addNeighbor(1, nodeN.node_id)
                    nodeN.addNeighbor(0, node.node_id)
                    self.AN_all_degree-=1
                if nodeN.graph_id == 2:
                    node.addNeighbor(2, nodeN.node_id)
                    nodeN.addNeighbor(0, node.node_id)
                self.H_all_degree -=1
                node.degree -=1
                nodeN.degree-=1 #If it is a vertex of the G_H_AN, it does not matter whether the degree decreases or not.
        # Step 5: Find suitable neighbors based on the assigned degree of the vertex.
        # First create a set, which contains all AN nodes with degree

        # print("Looking for suitable neighbors for AN vertex")
        for node in self.AN:
            AN_nei_candidate_list = reloadANneighbor(self, node)
            try:
                while(node.degree):
                    rangeJ = random.randint(0, len(AN_nei_candidate_list)-1)
                    nodeN = AN_nei_candidate_list[rangeJ]
                    # Find a suitable neighbor again
                    while((nodeN.degree == 0) or nodeN.node_id in node.neighbors[nodeN.graph_id]):
                        AN_nei_candidate_list.remove(nodeN)
                        rangeJ = random.randint(0, len(AN_nei_candidate_list)-1)
                        nodeN = AN_nei_candidate_list[rangeJ]

                    if nodeN.graph_id == 0:
                        node.addNeighbor(0, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                        self.H_all_degree-=1
                    if nodeN.graph_id == 1:
                        node.addNeighbor(1, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                        self.AN_all_degree-=1
                    if nodeN.graph_id == 2:
                        node.addNeighbor(2, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                    self.AN_all_degree-=1
                    node.degree -=1
                    nodeN.degree-=1 #If it is a vertex of the G_H_AN, it does not matter whether the degree decreases or not.
            except:
                pass