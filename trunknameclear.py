#--code with utf-8--
# Thinking and Writing by Rainbow.
# 自建数据处理模块
import characterclear
import dataprocess
import networkx as nx
from trunkstructer import *
from topologyanaylser import *

DefaultFileName = r"D:\RainbowThink\tkspace\all_trunk_201803_C_T_UTF-8.csv"

# 整理中继光路唯一名称.统一命名方便检索.
# 用到pandas扩展,数据处理(包括字符)很好用.
# 多段光缆的起始和终止判断,用到networkx扩展.
def maketrunkuniquename(filename = DefaultFileName):
    # 文件是ANSI编码,GBK编码python3会报错.
    fullname = input('请输入文件全名(包括路径和文件扩展,.csv(UTF-8)或.xslx(ANSI).):')
    if fullname.strip() == "":
        fullname = DefaultFileName
    else:
        pass

    import pandas as pd


    if (fullname.lower()).find(".xslx",len(fullname)-5,len(fullname)) != -1:
        df_file = pd.read_excel(fullname)
    elif (fullname.lower()).find(".csv",len(fullname)-4,len(fullname)) != -1:
        df_file = pd.read_csv(fullname)
    else:
        df_file = ""
        print("输入文件:{},不符合要求.请重新输入.", fullname)
        return "File extend is Error."

    df_group = df_file.groupby("唯一标识")
    trunkid = df_group.groups.keys()
    trunkinfo = [] # 按ID统计所有光缆的信息
    for ttid in trunkid:
        tid = str(ttid).sprit()
        subgraph = df_group.get_group(tid.upper())
        sgindex = (subgraph.index).to_list()
        sgcolumn = (subgraph.columns).to_list()
        aendloc = sgcolumn.index("起始端名称")
        zendloc = sgcolumn.index("对端名称")
        azlongloc = sgcolumn.index("光缆长度")
        azcapaloc = sgcolumn.index("对应芯数")
        aendodfloc = sgcolumn.index("起始端位置")
        zendodfloc = sgcolumn.index("对端位置")
        #-------------- 构建中继整条信息 ------------------------------------------------------------------------#
        onetrunk = TRUNK.copy()
        onetrunk["TrunkID"] = tid
        onetrunk["TopoSegments"] = []
        #----------------------构建单光缆各逻辑段拓扑------------------------------------------------------------#
        G = nx.Graph()
        for tr in sgindex:
            #----------------逻辑段端点信息构建==END--------------------------------------------#
            aendname = str(subgraph.loc[tr,:][aendloc]).strip()
            aendodf = str(subgraph.loc[tr,:][aendodfloc]).strip()
            zendname = str(subgraph.loc[tr,:][zendloc]).strip()
            zendodf = str(subgraph.loc[tr,:][zendodfloc]).strip()
            aend = END.copy()
            aend["TrunkID"] = tid
            aend["EndName"] = aendname
            aend["ODF"] = aendodf
            zend = END.copy()
            zend["TrunkID"] = tid
            zend["EndName"] = zendname
            zend["ODF"] = zendodf
            #----------------逻辑段端点信息构建完毕==END----------------------------------------#
            
            #-------------------逻辑段端点对儿信息==ENDPEER-----------------------------#
            azenddict = ENDPEER.copy() 
            azenddict["TrunkID"] = tid
            azenddict[aendname] = aend
            azenddict[zendname] = zend
            #------------------逻辑段端点对儿信息构建完毕==ENDPEER-----------------------#

            #--------------单光缆逻辑段信息==TOPOLOGYSEGMENT--------------------------------#
            azsegment = TOPOLOGYSEGMENT.copy()
            azlenght = subgraph.loc[tr,:][azlongloc]
            azcapability = subgraph.loc[tr,:][azcapaloc]
            azsegment["SegmentEnds"] = azenddict
            azsegment["TrunkID"] = tid
            azsegment["Lenght"] = azlenght
            azsegment["Capabiliy"] = azcapability
            #--------------单光缆逻辑段信息==TOPOLOGYSEGMENT--------------------------------#
            
            #-------------------消除单光缆中相同逻辑段长度值和纤芯数差异==TRUNK------------------------------------------# 
            # 参照列表--已加入中继段信息中的逻辑段。只检查段点名称，其他的不检查。
            logicsegmentendslist = [] 
            for ls in onetrunk["TopoSegments"]:
                templist = list(ls["SegmentEnds"].keys())
                templist.remove("TrunkID") # 逻辑段中的ENDPEER中的TrunkID比较碍事。
                templist.sort()
                logicsegmentendslist.append(templist)
                templist = []

            # 将要加入中继信息的逻辑段。只检查段点名称，其他的不检查。
            segmentends = list(azsegment["SegmentEnds"].keys())
            segmentends.remove("TrunkID")
            segmentends.sort()

            if segmentends in logicsegmentendslist:
                for sg in onetrunk["TopoSegments"]:
                    sgends = list(sg["SegmentEnds"].keys())
                    sgends.remove("TrunkID") # 逻辑段中的ENDPEER中的TrunkID比较碍事。
                    sgends.sort()
                    if sgends == segmentends:
                        # 取最长的长度值。
                        if sg["Lenght"] > azsegment["Lenght"]:
                            pass
                        else:
                            sg["Lenght"] = azsegment["Lenght"]
                        # 取最多的纤芯数。
                        if sg["Capabiliy"] > azsegment["Capabiliy"]:
                            pass
                        else:
                            sg["Capabiliy"] = azsegment["Capabiliy"]
                    else:
                        pass
            else:
                onetrunk["TopoSegments"].append(azsegment)
            #-------------------消除单光缆中相同逻辑段长度值和纤芯数差异完毕==TRUNK--------------------------------------#

        #######################构建单光缆逻辑拓扑#####################################################
        for logicsegm in onetrunk["TopoSegments"]:
            segmtid = logicsegm["TrunkID"]
            segmazendlist = list(logicsegm["SegmentEnds"].keys())
            segmazendlist.remove("TrunkID")
            segmlenght = logicsegm["Lenght"]
            segmcapability = logicsegm["Capabiliy"]
            edgeattributesdict = {  "lenght":segmlenght,
                                    "id":segmtid,
                                    "capability":segmcapability
                                }
            G.add_edge(segmazendlist[0],segmazendlist[1], **edgeattributesdict)
        #######################单光缆单逻辑拓扑构建完毕###############################################
        #############################单光缆逻辑拓扑分析#######################################
        G_topology = G_topologyanaylser(G)
        #############################单光缆逻辑拓扑分析完毕###################################        
        #------------------------单光缆总长度信息计算==TRUNK------------------------------------------------#
        #nx.floyd_warshall_predecessor_and_distance(G,weight="lenght")
        trunkdict = nx.floyd_warshall(G,weight="lenght") # ===> nx.floyd_warshall_predecessor_and_distance(G, weight=weight)[1]
        trunklenghtest = 0
        trunkendslist = []
        for aend in list(trunkdict):
            for zend in list(trunkdict[aend]):
                if trunkdict[aend][zend] > trunklenghtest:
                    trunklenghtest = trunkdict[aend][zend]
                    trunkendslist.clear()
                    trunkendslist.append(aend)
                    trunkendslist.append(zend)
                else:
                    pass
        onetrunk["Lenght"] = trunklenghtest # 数值计算和判断方法有误，有更多路径时，数值不是最长的；是最短路径里最长的。
        onetrunk["TrunkEnds"] = trunkendslist
        #------------------------单光缆总长度信息计算==TRUNK------------------------------------------------#

        #--------------------单光缆信息构建-----------------------------------------------------------------#
        onetrunk["RouteNodes"] = G_topology["NodeString"]
        onetrunk["TrunkTopologyType"] = G_topology["Summary"][-1]
         G_topology.update({"TruinID":tid})
        onetrunk["RouteSummary"] = G_topology # tuple([tid,G_topology])
        #------------------------单光缆容量信息计算==TRUNK------------------------------------------------#
        logicsegmentset = set()
        for logseg in onetrunk["TopoSegments"]:
            logendlist = list(logseg["SegmentEnds"].keys())
            logendlist.remove("TrunkID")
            logicsegmentset.add(tuple([logendlist[0],logendlist[1],logseg["Capabiliy"]]))
        logicnodedict = dict()
        for n in list(logicsegmentset):
            if n[0] in logicnodedict:
                logicnodedict[n[0]] += n[2]
            else:
                logicnodedict[n[0]] = n[2]
            if n[1] in logicnodedict:
                logicnodedict[n[1]] += n[2]
            else:
                logicnodedict[n[1]] = n[2]
        onetrunk["Capabiliy"] = max([logicnodedict[x] for x in onetrunk["TrunkEnds"]])
        #------------------------单光缆容量信息计算==TRUNK------------------------------------------------#
        #------------------------单光缆名称组合==TRUNK------------------------------------------------#
        tnamelist = []
        tnamelist.append(tid.upper())
        tnamelist.append("[" + str(onetrunk["Capabiliy"])  + "]")
        topotypedict = TOPOLOGYSYMBOL.copy()
        tnamelist.append("[" + topotypedict[onetrunk["TrunkTopologyType"]]  + "]")
        if "-" in onetrunk["RouteNodes"]:
            routenodeslist = onetrunk["RouteNodes"].split("-")
            bar = True
        elif "||" in onetrunk["RouteNodes"]:
            routenodeslist = onetrunk["RouteNodes"].split("||")
            bar = False
        heardend = True
        tempnodeslist = []
        for rn in routenodeslist:
            if rn in onetrunk["TrunkEnds"]:
                if heardend is True:
                    tempnodeslist.append(("[" + str(logicnodedict[rn]) + "]" + rn))
                    heardend = False
                else:
                    tempnodeslist.append((rn + "[" + str(logicnodedict[rn]) + "]"))
            else:
                tempnodeslist.append(("[" + str(logicnodedict[rn]//2) + "]" + rn + "[" + str(logicnodedict[rn]//2) + "]"))
        if bar is True:
            tempnodestring = "-".join(tempnodeslist)
        else:
            tempnodestring = "||".join(tempnodeslist)

        tnamelist.append(tempnodestring)
        onetrunk["TrunkName"] = "_".join(tnamelist)
        #------------------------单光缆名称组合==TRUNK------------------------------------------------#

        #------------------------检查trunk信息状态------------------------------------------------#
        tcheck = INFOMATIONCHECK.copy()
        segmnumber = len(onetrunk["TopoSegments"])
        if onetrunk["TrunkTopologyType"] == "一字形图" and segmnumber >= 1:
            tcheck["SegmentCheck"] = True
        elif onetrunk["TrunkTopologyType"] == "三角形图" and segmnumber == 3:
            tcheck["SegmentCheck"] = True
        elif onetrunk["TrunkTopologyType"] == "四边形图" and segmnumber == 4:
            tcheck["SegmentCheck"] = True
        else:
            tcheck["SegmentCheck"] = False

        if '-' in onetrunk["TrunkName"]:
            tknamecapalist = onetrunk["TrunkName"].split("_")[-1]
            tkncln = tknamecapalist.split("-")
            tka = tkncln[0]
            tkz = tkncln[-1]
            tknclac = int(tka[(tka.find("[")+1):(tka.find("]"))])
            tknclzc = int(tkz[(tkz.find("[")+1):(tkz.find("]"))])
            if tknclac == tknclzc:
                tcheck["CapabiliyCheck"] = True
            else:
                tcheck["CapabiliyCheck"] = False
        elif '||' in onetrunk["TrunkName"]:
            tcheck["CapabiliyCheck"] = False

        onetrunk["InfomationState"] = tcheck


        #------------------------检查trunk信息状态==完毕------------------------------------------------#

        #--------------------单光缆信息构建完毕-------------------------------------------------------------#
        #trunkinfo.append(onetrunk["RouteSummary"])
        trunkinfo.append(onetrunk)
        #############################中继信息汇集完毕###################################
        return trunkinfo

def makenodetofenju(tkfadict=FENJUAREAMAP.copy(), tknodedict=NODEAREAMAP.copy()):
    nodetofenjudict = dict()
    for fj in tkfadict.keys():
        for areafj in tkfadict[fj]:
            for areanode in tknodedict.keys():
                for n in tknodedict[areanode]:
                    if areafj == areanode:
                        nodetofenjudict[n] = fj
                    eles:
                        pass
    return nodetofenjudict

def makestandsegment(tkinfo=trunkinfo, tkdict=STANDTRUNKRECODER.copy()):
    nodetofj = makestandsegment()
    tklslist = list()
    serialnumber = 1
    for tk in tkinfo:
        for tks in tk["TopoSegments"]:
            trunklogicsegment = tkdict.copy()
            trunklogicsegment["记录序号"] = str("{:>4d}".format(serialnumber))
            trunklogicsegment["A端至Z端光缆标识"] = tk["TrunkID"]
            tksend = list(tks["SegmentEnds"].keys())
            tksend.remove("TrunkID")
            tksend.sort()
            trunklogicsegment["A端名称"] = tksend[0]
            #trunklogicsegment["A端位置"] = tks["SegmentEnds"][tksend[0]]["ODF"]
            trunklogicsegment["B端名称"] = tksend[1]
            #trunklogicsegment["B端位置"] = tks["SegmentEnds"][tksend[1]]["ODF"]
            trunklogicsegment["A端至B端光缆长度"] = tks["Lenght"]
            trunklogicsegment["A端至B端芯数"] = tks["Capabiliy"]
            trunklogicsegment["A端至Z端光缆名称"] = tk["TrunkName"]
            trunklogicsegment["A端至Z端拓扑类型"] = tk["TrunkTopologyType"]
            trunklogicsegment["A端至Z端逻辑数量"] = len(tk["TopoSegments"])
            trunklogicsegment["A端至Z端逻辑段检查"] = tk["InfomationState"]["SegmentCheck"]
            trunklogicsegment["A端至Z端容量"] = tk["Capabiliy"]
            trunklogicsegment["A端至Z端容量检查"] = tk["InfomationState"]["CapabiliyCheck"]
            trunklogicsegment["A端至Z端距离"] = tk["Lenght"]
            if tksend[0] in nodetofj:
                trunklogicsegment["A端信息填报单位"] = nodetofj[tksend[0]]
            else:
                trunklogicsegment["A端信息填报单位"] = tksend[0]
            if tksend[1] in nodetofj:
                trunklogicsegment["B端信息填报单位"] = nodetofj[tksend[1]]
            else:
                trunklogicsegment["B端信息填报单位"] = tksend[1]
            tklslist.append(trunklogicsegment)
            serialnumber += 1
    return tklslist
