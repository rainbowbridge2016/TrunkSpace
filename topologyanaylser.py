################################################################################################################
# G topology anaylse.
# 
# 1. self-loop
# 2. planarity
# 3. cycle
# 4. bridge
# 5. neighbor
# 6. edge
# 7. node
#
#----------------------------------------------------------------------------------------------------------------
#
# Judge element
#
# 1 self-loop node nuber
# 2 planarity of G is true or false.
# 3 cycles number
# 4 bridegs number
# 5 max neighbor number
# 6 nodes number
# 7 edges number
#
#---------------------------------------------------------------------------------------------------------------
#
#  Logic of judge steps
#
# if self-loop number is 0:
#    if planarity is true:
#        if cycle number is 0:
#            if nodes number -edegs number is 1, and edges number = bridge number and max neighbor number <= 2
#                G topology is line. can be analyse.
#            elif nodes number -edegs number is 1, and edges number = bridge number and max neighbor number > 2
#                G topology is star. cna't be analyse.
#        else:
#            if bridge number is 0:
#                G.topology is pure cycles.
#                if cycle number = 1:
#                    G.topology is single cycles.
#                    if nodes number = 3:
#                        G.topology is three nodes cycle. can be anaylsed.
#                    elif nodes number = 4:
#                        G.topology is four nodes cycle. can be anaylsed.
#                    else:
#                        G.topology is more than nodes cycle. can't be anaylsed.
#                eles:
#                    G.topology is more than one cycle. can't be anaylsed.
#            else:
#                if bridge number is 1 and cycle number is 1:
#                    G.topology is one cycle and one bridge, can be anaylsed.
#                else: 
#                    G is blend cycle, can't be anaylsed.
#    else:
#        G can't anaylsed.
# else:
#     G has Error
#
#########################################################################################################


import networkx as nx

TOPOLOGY = {
    "Self-Loop": None,
    "Planarity": None,
    "Cycles": None,
    "Bridges": None,
    "MaxNeighbors": None,
    "Edges": None,
    "Nodes": None,
    "Summary": None,
    "NodeString": None
}

TOPOLOGYSYMBOL = {  # △ ◇ ☆ – ― 〇 ◎ ⊥≒≌∞○
    "一字形图": "―",
    "三角形图": "△",
    "四边形图": "◇",
    "多边形图": "*",
    "星形图": "☆",
    "多环图": "◎",
    "单环单桥图": "○―",
    "多环桥图": "◎=",
    "非平面图": "#",
    "未知图": "?"
}


#---1---将一线串多点的处理总结成'糖葫芦'函数,tanghulu().含再次判断-----------------#
def tanghulu(G = None):
    '''
    #---1---线型图.节点n,边n-1,桥n-1,节点邻居<=2(拒绝>2的星形)-------------------#
    #---1---三点两段,四点三段等.-----------------------------------------------------#
    #---1---判断:节点-边==1 and 边==桥 and 邻接 <=2 ---------------------------------#
    #---1---将一线串多点的处理总结成'糖葫芦'函数,tanghulu().含再次判断-----------------#
    '''
    trunknodestring = None
    #############################图拓扑判断的基本要素###################################
    nodesnumber = G.order()
    edgesnumber = len(nx.edges(G))
    bridgesnumber = len(list(nx.bridges(G)))
    maxadjnumber = max([len(v) for k,v in G.adjacency()])
    if (nodesnumber - edgesnumber == 1) and (edgesnumber == bridgesnumber) and (maxadjnumber <= 2):
        tlist = []
        mnode = []
        for n in list(nx.nodes(G)):
            if len(G.adj[n]) == 1: # 邻接数=1的节点是端节点.列表中只会有两个节点.
                tlist.append(n)
            else:
                mnode.append(n) # 邻接数>1的节点是中间节点.列表中节点数可以是0或多个.
        tlist.sort() # 端节点排个序,没啥用处,就是看着好看.
        starname = tlist[0]
        while len(mnode) >= 1: # 从端节点开始,将中间节点按照邻接顺序插入节点列表.
            nextname = list(G.neighbors(starname)).pop()
            tlist.insert(-1,nextname)
            starname = nextname
            mnode.pop(mnode.index(nextname)) # 将插入节点列表的节点,从中间节点集中删除.
        trunknodestring = "-".join(tlist) # 生成节点顺序字符串.
    else:
        pass
    return trunknodestring


def G_topologyanaylser(G = None):
    '''
    --------Judge element--------
    1 self-loop node nuber
    2 planarity of G is true or false.
    3 cycles number
    4 bridegs number
    5 max neighbor number
    6 nodes number
    7 edges number
    '''
    trunknodestr = None
    topologystruct = TOPOLOGY.copy()
    ############...G analyse element: selfloop, planarity, cycle, bridge, nodes, edges, maxneighbor.......#################
    topologystruct["Self-Loop"] = selfloopnumber = nx.number_of_selfloops(G) # if G has selfloop, return number.  nx.nodes_with_selfloops(G)
    topologystruct["Planarity"] = planartiyG = nx.check_planarity(G)[0] # if G is planartiy, return "True".
    topologystruct["Cycles"] = cyclenumber = len(nx.cycle_basis(G)) # if G has cycle, return smallest-cycle list.
    topologystruct["Bridges"] = bridgesnumber = len(list(nx.bridges(G))) # (nx.has_bridges(G) == False)  
    topologystruct["MaxNeighbors"] = maxadjnumber = max([len(v) for k,v in G.adjacency()])
    topologystruct["Edges"] = edgesnumber = len(nx.edges(G))
    topologystruct["Nodes"] = nodesnumber = G.order()
    topologystruct["Summary"] = []
    
    if selfloopnumber == 0:
        topologystruct["Summary"].append("无自环")
        if planartiyG is True:
            topologystruct["Summary"].append("平面图")
            if cyclenumber == 0:
                topologystruct["Summary"].append("无环图")
                ############无向图的检测:平面性，环，桥,节点数,边数,最大邻接数.......#################
                #----------------如何想处理图,就需要把图形归类,并化简-------------------------------#
                #---1---线型图.节点n,边n-1,桥n-1,节点邻居<=2(拒绝>2的星形)------------------------#
                #---1---三点两段,四点三段等.-------------------- ----------------------------------#
                #---1---判断:节点-边==1 and 边==桥 and 邻接 <=2 ----- -----------------------------#
                #---1---将一线串多点的处理总结成'糖葫芦'函数-->tanghulu().含再次判断-----------------#
                if (nodesnumber - edgesnumber == 1) and (edgesnumber == bridgesnumber) and (maxadjnumber <= 2):
                    topologystruct["Summary"].append("一字形图")
                    trunknodestr = tanghulu(G)
                elif (nodesnumber - edgesnumber == 1) and (edgesnumber == bridgesnumber) and (maxadjnumber > 2):
                    topologystruct["Summary"].append("星形图")
                    pass
                else:
                    topologystruct["Summary"].append("不知道")
                    pass
            else:
                topologystruct["Summary"].append("有环图")
                if bridgesnumber == 0:
                    topologystruct["Summary"].append("纯环图")
                    if cyclenumber == 1:
                        topologystruct["Summary"].append("单环图")
                        #---2---闭合三角形图.节点n,边n,桥0,节点邻居<=2-------------------------------------#
                        #---2---判断:节点数==3 节点数==边数 and 是否有桥==False and 邻接数 <=2 -------------#
                        #---2--三角形拓扑,消去最长边,成线型拓扑图------------------------------------------#
                        #if (nx.has_bridges(G) == False) and (nodesnumber == edgesnumber) and (nodesnumber == 3) and (maxadjnumber <= 2):
                        if (nodesnumber == edgesnumber) and (maxadjnumber <= 2) and (nodesnumber == 3) :
                            topologystruct["Summary"].append("三角形图")
                            #找出三角形的最长边
                            maxlenght = 0
                            for (u,v,l) in G.edges.data("lenght"):
                                if l > maxlenght:
                                    maxlenght = l
                                    maxlenghtedge = tuple([u,v])
                                else:
                                    pass
                            #删除三角形的最长边,形成一线串多点.
                            Gc = G.copy(as_view = False)
                            Gc.remove_edge(*maxlenghtedge)
                            trunknodestr = tanghulu(Gc)
                        elif (nodesnumber == edgesnumber) and (maxadjnumber <= 2) and (nodesnumber == 4) :
                            topologystruct["Summary"].append("四边形图")
                        elif (nodesnumber == edgesnumber) and (maxadjnumber <= 2) and (nodesnumber > 4) :
                            topologystruct["Summary"].append("多边形图")
                        else:
                            topologystruct["Summary"].append("未知图")
                            pass
                    else:
                        topologystruct["Summary"].append("多环图")
                        pass
                else:
                    topologystruct["Summary"].append("复合环图") 
                    if bridgesnumber == 1 and cyclenumber == 1:
                        topologystruct["Summary"].append("单环单桥图") # single cycle and one or two bridge graph is can be anaylsed
                        pass
                    else:
                        topologystruct["Summary"].append("多环桥图")
                        pass
                    pass
        else:
            topologystruct["Summary"].append("非平面图")
            pass
    else:
        topologystruct["Summary"].append(tuple(["有自环",selfloopnumber,[n for n in nx.nodes_with_selfloops(G)]]))
        pass
    #############################单条中继逻辑拓扑分析完毕###################################
    if trunknodestr is not None:
        topologystruct["NodeString"] = trunknodestr
    else:
        topologystruct["NodeString"] = "||".join(G.nodes())
    return topologystruct