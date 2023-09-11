


def printParameters(self):
    self.decSpace = self.decConnectedSpace()
    print("Print current parameters")
    print("H_score:%f"%(self.calDecScoreH()))
    print("-------------------------------------------------------------------")
    print("Network H")
    print("H_nodes:%d" %(self.H_nodes_num))
    print("H_goodnodes:%d" %(self.H_good_num))
    print("H_averageNodeDegree:%f"%(self.calAverageD(self.H)))
    print("H_goodNode_connectedSpace:%d"%(self.decSpace))
    print("-------------------------------------------------------------------")
    print("Network AN")
    print("AN_nodes:%d"%(self.AN_nodes_num))
    print("AN_goodDecGene:%d"%(self.AN_decGood_num))
    # print("AN_goodDecOut:%d"%(len(self.faultFreeSet)))
    print("AN_nodeDegree:%d"%(self.AN_degree))
    print("AN_averageDegree:%f"%(self.calAverageD(self.AN)))
    print("-------------------------------------------------------------------")
    print("Network G_AN_H")
    print("G_AN_H_nodes:%d"%(self.G_AN_H_nodes_num))
    print("-------------------------------------------------------------------")
    return

