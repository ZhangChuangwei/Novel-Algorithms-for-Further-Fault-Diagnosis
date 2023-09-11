

class Node(object):
    def __init__(self, node_id, level=0, detection_function = True, goodN = 0, degree=-1, graph_id = -1):
        self.node_id = node_id
        self.neighbors = [[], [], []] #is a list, store neighbors_id, 0=H,1=AN,2=G-AN-H
        self.level = level #0 represent good;
        self.detection_function = detection_function #True represent good detection ability
        self.dec_level = -1 #This is used to calculate accuracy and other indicators.
        self.status = -1 # be checked or not in H
        self.g_goodN = goodN
        self.degree = degree
        self.graph_id = graph_id

    def addNeighbor(self, graph_id, node_id): # here, we will not check the number of neighbors; this work will be finished in creating Network
        self.neighbors[graph_id].append(node_id)

    def changeStatus(self, status):
        self.status = status

    def changeDec(self, dec=True):
        self.detection_function = True

    def changeGN(self, gN):
        self.g_goodN = gN

    def returnID(self):
        return self.node_id

    def returnStatus(self):
        return self.status

    def returnNeighbors(self):
        return self.neighbors

    def returnLevel(self):
        return self.level

    def returnID(self):
        return self.node_id

    def returnDF(self):
        return self.detection_function

