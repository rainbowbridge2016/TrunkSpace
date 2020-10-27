# 字典浅拷贝后自由使用，不涉及深层数据结构。
TRUNK = {
    "TrunkID": None, # unique id. link key.
    "TopoSegments": None, # some segments dict in list. [TOPOLOGYSEGMENT, TOPOLOGYSEGMENT, TOPOLOGYSEGMENT, ]
    "RouteNodes": None, # some nodes in string. exp. node-node-node.
    "TrunkName": None, # the name. ex. node-node-node-capa-dilver.
    "Capabiliy": None, # fiber number all of cable, is ends fiber number.
    "RouteSummary": None, # information of roads the cable climb.
    "Lenght": None, # best lenght of trunk. sum some segment lenght between trunk ends.
    "TrunkEnds": None, # link key. two ends for trunks, between two ends is longest. sometime have three, but i don't think this.
    "RoadSummary": None, # cable on the road in city.
    "TrunkTopologyType": None, # topology class, exm. line, triangle.
    "InfomationState": None # check all of infomation, recode state, is dict, logosegm, odf, etc., detiale info.
}
INFOMATIONCHECK = {
    "SegmentCheck": None,
    "ODFCheck": None,
    "CapabiliyCheck": None,
    "RouteCheck": None
}
TOPOLOGYSEGMENT = {
    "TrunkID": None, # using trunkid. link key.
    "SegmentEnds": None, # link key. two ends in one dict, is ENDPEER. 
    "Lenght": None,# long number in segment.
    "Capabiliy": None, # fiber number of segment.
    "FieberType": None, # fiber type of segment.
    "Color": None, # importent level, with color.
    "UnderGround": None # cable in earth or above earth.
}
ENDPEER = { # EndName of END is key, END dict is value, in this dict. created in program.
    "TrunkID": None
}
END = {
    "TrunkID": None, # link key. one node have some end of other trunk.
    "EndName": None, # link key. stop in somewhere, sometime in node. link key.
    "Location": None, # in building someone storey.
    "Room": None, # in room of someone storey.
    "ODF": None # row, frame, model, and some terminals. by something join with "-". link key.
}
ODF = {
    "TrunkID": None, # link key. 
    "EndName": None, # link key. two items can included in END dict as ODF's sub dict.
    "Area": None, # A or E or N some area in room.
    "Row": None, # line or row, some frame by frame.
    "Frame": None, # someone frame, is tall.
    "Case": None, # some cases in frame at somewhere, 01-72 terminals in one model, 
    "Pallet": None # some pallet in model, 01-12 or 8(etc.) terminals in one pallet.(T,T,T,T,T,....),the dict can be motify.
}
TERMINAL = {
    "Model": None, # FC or SC.
    "Inuse": None, # 1 or 0, yes or no.
    "Service": None, # Service lable include some information. 
    "JumpTo": None   # ODF string of Other side or device name and solt info. maybe using OTHERSIDE.
}
OTHERSIDE = {
    "ODF": None, # ODF info.
    "Device": None, # device info, etc. case solt port etc.
    "RouteInfo": None # something of get info.
}
