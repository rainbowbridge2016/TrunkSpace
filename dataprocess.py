import re
import exceldatastruct
import characterclear

# 利用等长字符串做替换,还是比较简洁.
# 清洗英文异常字符
EN_CHAR_QJ_upper_set = "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
EN_CHAR_upper_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
EN_CHAR_QJ_lower_set = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
EN_CHAR_lower_set = "abcdefghijklmnopqrstuvwxyz"

EN_CHAR_QJ_set = {
                 "＼": "/",
                 "，": ",",
                 "．": ".",
                 "；": ";",
                 "（": "(",
                 "）": ")",
                 "［": "[",
                 "］": "]",
                 "－": "-",
                 "｜": "|",
                 "＂": '"',
                 "＂": '"',
                 "＇": "'",
                 "＇": "'",
                 "～": "~",
                 "＆": "&",
                 "＋": "+",
                 "－": "-",
                 "×": "*",
                 "／": "/",
                 "＾": "^",
                 "％": "%",
                 "＄": "$",
                 "＃": "#",
                 "＠": "@",
                 "！": "!"
                 }

# 利用字典存储等长替换信息，没有规律不太方便用字符串格式。
# 清洗中文分隔符到字符分隔符。可以用字典迭代器完成。
CN_CHAR_set = {
              "～": "~",
              "。": ",",
              "，": ",",
              "、": ",",
              "（": "(",
              "）": ")",
              "【": "[",
              "】": "]",
              "—": "-",
              "“": '"',
              "”": '"',
              "丨": ",",  # 中文，棍（音），不知作何用，出现后会引起混乱。强烈建议表达式中不能出现此字符。
              "|": ","    # 英文，"|"作为分隔成端纤芯数使用，替换的是"()"，因此在表达式中不能出现。
              }

# 清洗中文数字写法到字符阿拉伯数字。
CN_NUM_set = {
            "〇": "0",
            "一": "1",
            "二": "2",
            "三": "3",
            "四": "4",
            "五": "5",
            "六": "6",
            "七": "7",
            "八": "8",
            "九": "9",

            "零": "0",
            "壹": "1",
            "贰": "2",
            "叁": "3",
            "肆": "4",
            "伍": "5",
            "陆": "6",
            "柒": "7",
            "捌": "8",
            "玖": "9",

            "貮": "2",
            "两": "2",
            "十": "1",
            "廿": "2"
            }

# 清洗全角阿拉伯数字到字符阿拉伯数字。
CN_QJNUM_set = {
                "０": "0", # 全角中文标点阿拉伯数字
                "１": "1",
                "２": "2",
                "３": "3",
                "４": "4",
                "５": "5",
                "６": "6",
                "７": "7",
                "８": "8",
                "９": "9",

                "０": "0", # 半角英文标点阿拉伯数字，同全角中文标点阿拉伯数字
                "１": "1",
                "２": "2",
                "３": "3",
                "４": "4",
                "５": "5",
                "６": "6",
                "７": "7",
                "８": "8",
                "９": "9"
                }

# 清洗ODF表达式中异常字符，异常分隔符。
CHAR_REPL_set = { 
                # "\n": "&", # 多个ODF的分隔符。
                "ODF": "",
                "--": "-",
                "---": "-",
                "----": "-",
                "~": "-"
                }

CN_UTF8_area_1 = r"\u4e00-\u9fa5" # 0x4e00-0x9fa5(中文)
CN_UTF8_area_2 = r"\u3400-\u4DB5" # 0x3400-0x4DB5(中文扩展汉字)
ASCII_set = r"\x00-\xff" # 正则表达式: [^\x00-\xff], 只匹配非ASCII码字符(也称双字节字符), 利用汉字为: 双字节字符的原理

# 拆分ODF表达式中的光纤盘，替换掉"()",统一用"|"，方便拆分动作。
CHAR_REPL_SPLIT_set = {
                      "\n": "&", # 多个ODF的分隔符。
                      "(": "|", # 拆分ODF信息用的。
                      ")": "|"  # # 拆分ODF信息用的。
                      }

# ('记录序号', 'fun_jlxh'),
def fun_jlxh(xh):
    '''
    # 序号，本来序号就是一串数字（光缆数量通常不超过3位），但在存入excel表格中的时候，会变成日期之类的东西。
    # 在没时间调整excel的时候，在序号前加上No.，固化成字符串。
    '''
    l = len(int(xh))
    inxh = str(int(xh))
    tempxh = ""
    cuttuple = tuple()
    if l >= 3 :
        tempxh = inxh
    elif l == 2:
        tempxh = "0" + inxh
    elif l == 1:
        tempxh = "00" + inxh
    elif l <= 0:
        tempxh = "000" + inxh
    tempxh = "No." + tempxh
    return tempxh, cuttuple

# ('A端至B端光缆标识', 'fun_adzbdglbs'),
def fun_adzbdglbs(glbs):
    '''
    # 规范了中继光缆编号的形式：一位大写字母+三位阿拉伯数字的形式，不够三位的用0补全。
    '''
    cableqz = r"([A-Fa-f])"
    cablenum = r"(\d+)"
    cableid = cableqz + cablenum # ID号必须是:字母+1-3个数字。
    cr = re.compile(cableid)
    cabmat = cr.match(str(glbs))
    tempglbs = ""
    cuttuple = tuple()
    if type(cabmat) == None:
        pass
    else:
        tempglbs += cabmat.group(1).upper()
        numl = len(cabmat.group(2))
        if numl >= 3:
            tempglbs += cabmat.group(2)[numl-3:numl]
        elif numl == 2:
            tempglbs = "0" + tempglbs
        elif numl == 1:
            tempglbs = "00" + tempglbs
        elif numl == 0:
            tempglbs = "000" + tempglbs
        else:
            pass
    return tempglbs, cuttuple

# ('A端名称', 'fun_admc'),
def fun_admc(name):
    '''
    # 规范局点的名称，“区域+局点名+设备间”命名。网络边界处会有“河北省”等大区域的命名，在本数据中忽略了，因为不知河北省交界处的细分区域是哪个地县。
    '''
    namec = "".join(name.strip(" ").split(" "))
    from fuzzywuzzy import fuzz
    tempname = ""
    # 使用fuzz的简单匹配partial函数，过滤需换名的局点。匹配率大概是68以上，相似度能达到65就认为是同一个局点。
    if fuzz.partial_ratio("通信枢纽楼东丽", namec) >= 65:
    	tempname = "东丽空港IDC"
    elif fuzz.partial_ratio("贯庄", namec) >= 65:
        tempname = "东丽空港"
    elif fuzz.partial_ratio("解放路", namec) >= 65:
        tempname = "塘沽草场街"
    elif fuzz.partial_ratio("胜利", namec) >= 65:
        tempname = "大港一中心"
    elif fuzz.partial_ratio("永明", namec) >= 65:
        tempname = "大港二中心"
    # 使用字符串find锁定两个IDC局，再加上fuzz的简单匹配partial函数，更换IDC局点名。两个IDC和属地局的混淆度在57左右，达到65就认为是同一个局点。
    elif namec.find("IDC") != -1 and fuzz.ratio(namec,"华苑IDC") > 65:
        tempname = "西青华苑IDC"
    elif namec.find("IDC") != -1 and fuzz.ratio(namec,"空港IDC") > 65:
        tempname = "东丽空港IDC"
    else:        
        for n in Node_Name_All_set:
            # 使用fuzz的非完全匹配函数partial_ratio函数，修正命名不规范的局点。相似度只有达到85才能认为是同一个局点。
            if fuzz.partial_ratio(n, namec) >= 85:
                tempname = n

    if tempname == "":
        return tempname, tuple(namec,"")
    else:
        return tempname, tuple()


# ('A端楼层', 'fun_adlc'),
def fun_adlc(lc):
    '''
    # 将楼层的汉字变成阿拉伯数字+L形式，方便运算和显示。
    '''
    cnnumset = "".join(CN_NUM_set.keys()) # "零一二三四五六七八九十廿"
    arabnumset = "".join(CN_NUM_set.values()) #"012345678912"
    templc = lc.replace("楼","F")
    for n in cnnumset:
        # 网上某个大神的好思路,源码用eval(n)函数直接找内存中的变量索引，但中文不能作为变量，没有索引位置，会产生异常；所以改用index()函数。
        templc = templc.replace(n,arabnumset[cnnumset.index(n)])
    return templc, tuple()

# ('A端区域', 'fun_adqy'),
def fun_adqy(qy):
    '''
     # 此处数据，由位置过滤后的剩余数据填充。
    '''
    pass

# ('A端位置', 'fun_adwz'),
def fun_adwz(wz):
    '''
    # 把ODF中的汉字，ABC等字母，还有多余的"ODF"字幕去掉，原则是只留数字、-、()，其他的都要过滤掉，并放到本端“区域”的位置里。
    '''
    #-----------------清洗ODF字符串--------------------
    # 消除字符串中的" "
    tempwz = "".join(wz.strip(" ").split(" ")) # 清洗

    # 将中文半角字符，替换成英文字符。
    # 使用字典迭代器省略了生成两个字符串的步骤。规避了占位符不等长的情况。
    for cn in CN_CHAR_set.items():
        tempwz = tempwz.replace(cn[0], cn[1])

    # 将英文全角字符，转换成英文字符（含大小写），扫描两遍。这两个set是两组字符串。
    for enu in EN_CHAR_QJ_upper_set: 
        tempwz = tempwz.replace(enu,EN_CHAR_upper_set[EN_CHAR_QJ_upper_set.index(enu)])
    for enl in EN_CHAR_QJ_lower_set:
        tempwz = tempwz.replace(enl,EN_CHAR_lower_set[EN_CHAR_QJ_lower_set.index(enl)])
    for ec in EN_CHAR_QJ_set.items():
        tempwz = tempwz.replace(ec[0], ec[1])
    
    # 将中文的全角阿拉伯数字，替换成英文阿拉伯数字
    # 字典迭代器代替字符串对应比较。
    for ca in CN_QJNUM_set.items():
        tempwz = tempwz.replace(ca[0], ca[1])

    # 消除字符串中的多余的字符。
    # 使用字典的迭代器，完成更多字符的替换。
    for cr in CHAR_REPL_set.items(): # 清洗
        tempwz = tempwz.replace(cr[0], cr[1])

    #----------------提取并清洗掉位置区域信息（中文和英文字符：xx楼 [a-Z]）---------------------
    #print(tempwz)
    import re
    # 中文作为区域信息。这个信息是要返回函数外，放置他处的。
    cn = r"[" + CN_UTF8_area_1 + "|" + CN_UTF8_area_2 + "]"
    cnlist = re.findall(cn,tempwz)
    cnstr = "".join(cnlist)
    #print(cnstr)
    an = r"[" + ASCII_set + r"]"
    asclist = re.findall(an,tempwz)
    tempwz = "".join(asclist)
    #print(tempwz)
    # 英文字母，作为行列信息。这个信息是要加入newodf的首端。
    alplist = re.findall(r"[a-z|A-Z]",tempwz)
    alpstr = "".join(alplist)
    noalplist = re.findall(r"[^a-z|^A-Z]",tempwz)
    tempwz = "".join(noalplist)
    #print(tempwz)
    
    #----------------重置ODF表达式中的分隔符-------------------------------------------------
    # 消除字符串软回车，用"&"替换掉"\n"，用"|"替换掉"()"，便于拆分字符串。拆分优先级，先"&",再"|"。
    # 分隔符"|"与某些中文符号utf-8编码集重合，最后再重置分隔符。
    for cs in CHAR_REPL_SPLIT_set.items():
        tempwz = tempwz.replace(cs[0], cs[1])

    # --------------重组ODF信息------------------------------------------------------------
    #print(tempwz)
    odflist = tempwz.split("&") # 拆分连体的多个ODF表达式。如果没有"&"字符，也将tempwz塞入list中。
    odflist = [i for i in odflist if (len(str(i)) != 0)] # 消除ODF表达式为"空"的信息，算是一种清洗。
    newodf = ""
    for odf in odflist: # 多个ODF表达式，迭代循环进行拆解。
        odfinfo = odf.split("|") # 单个ODF表达式拆分，拆成模块和成端，共两部分。
        odfinfo = [i for i in odfinfo if (len(str(i)) != 0)] # 消除ODF信息中为"空"的内容，算是一种清洗。
        odfinfotuple = tuple(odfinfo) # 固定list中数据的位置。属于是位置敏感型。

        odfmodel = odfinfotuple[0] # 模块
        odfmodelterminal = odfinfotuple[1] # 托盘
        
        # 处理odf成端表达格式。处理结果如：(01-72)，满配占位符。
        # 还需考虑这样的情形:(xx-ww,z,aa-bb)，所以先以","作为分隔符拆解，再以"-"作为分隔符拆解。
        alltlist = odfmodelterminal.split(",")
        #print(alltlist)
        alltlist = [i for i in alltlist if (len(str(i)) != 0)] # 清洗“托盘”内信息为""的元素。
        newodfmodelterminal = "" + "("
        #tcaptical = 0
        for allt in alltlist:
            tlist = allt.split("-")
            tlist = [i for i in tlist if (len(str(i)) != 0)] # 消除表达式为"空"的信息，算是一种清洗。
            if len(tlist) > 1: # 纤芯数是一个范围的，xx-yy
                tstart = tlist[0]
                tend = tlist[1]
                #tcaptical += int(tend) - int(tstart) + 1 # 成端纤芯数量。
                #newodfmodelterminal = "(" + str("{:0>2d}".format(int(tstart))) + "-" + str("{:0>2d}".format(int(tend))) + ")"
                newodfmodelterminal += str("{:0>2d}".format(int(tstart))) + "-" + str("{:0>2d}".format(int(tend)))
            else: # 纤芯数是单点位置的，xx。
                tstartend = tlist[0]
                #tcaptical += 1 # 单芯数量是1。
                newodfmodelterminal += str("{:0>2d}".format(int(tstartend)))
            newodfmodelterminal += ","
        newomtlist = list(newodfmodelterminal)
        newomtlist.pop()
        newodfmodelterminal = "".join(newomtlist)
        newodfmodelterminal += ")"

        # 处理odf列架模块表达式。处理结果
        flist = odfmodel.split("-")
        flist = [i for i in flist if(len(str(i))!=0)] # 消除表达式为"空"的信息，算是一种清洗。
        odfr = flist[0]
        odff = flist[1]
        odfm = flist[2]
        odfmlist = odfm.split("/")
        odfmlist = [i for i in odfmlist if(len(str(i))!=0)] # 消除表达式为"空"的信息，算是一种清洗。
        odfmnumber = len(odfmlist) # 模块数量

        # 组装ODF表达式。多个表达式之间用"&"符号连接。
        for m in odfmlist:  # 单、多各模块的共用的ODF表达式组装工具，可以在模块数前+"M"
            newodf += alpstr # ODF位置前，加入原生带来的字母（表示列面等位置信息）。
            #newodf += str("{:0>2d}".format(int(odfr))) + "-" + str("{:0>2d}".format(int(odff))) + "-" + "M" + str("{:0>2d}".format(int(m))) + newodfmodelterminal
            newodf += str("{:0>2d}".format(int(odfr))) + "-" + str("{:0>2d}".format(int(odff))) + "-" + str("{:0>2d}".format(int(m))) + newodfmodelterminal
            newodf += "&"
    # 去除结尾的"&"符号。
    newodflist = list(newodf)
    newodflist.pop()
    newodf = "".join(newodflist)
    
    # 如何返回所需数据，还是需要仔细考虑。
    return newodf,tuple(cnstr)

# ('A端适配器', 'fun_adspq'),
def fun_adspq(spq):
    '''
    # 适配器清洗，并返回大写字母。
    '''
    # 清除适配器字符串中的空格。
    tempspq = "".join(name.strip(" ").split(" "))
    # 返回适配器大写字母
    return tempspq.upper(), tulpe()


# ('A端至B端光缆名称', 'fun_adzbdglmc'),
def fun_adzbdglmc(lname):
    pass

# 数据位置不同，不使用函数传递。
# fun_adzbdglmc = fun_adwz # 函数传递

# ('B端适配器', 'fun_bdspq'),
# def fun_bdspq(spq):
#     pass
fun_bdspq = fun_adspq

# ('B端位置', 'fun_bdwz'),
def fun_bdwz(wz):
    pass

# ('B端区域', 'fun_bdqy'),
def fun_bdqy(qy):
    pass

# ('B端楼层', 'fun_bdlc'),
def fun_bdlc(lc):
    pass

# ('B端名称', 'fun_bdmc'),
# def fun_bdmc(name):
#     pass

fun_bdmc = fun_admc

# ('A端至B端芯数', 'fun_adzbdxs'),
def fun_adzbdxs(xs):
    if xs != '':
        return "'" + srt(int(xs))
    else:
        return ''

# ('A端至B端光缆长度', 'fun_adzbdglcd'),
def fun_adzbdglcd(lcd):
    if lcd != '':
        return "'" + str(float(lcd*1000,2))
    else:
        return ''

# ('A端占用芯数', 'fun_adzyxs'),
def fun_adzyxs(zyxs):
    if zyxs != '':
        return "'" + str(int(zyxs))
    else:
        return ''

# ('B端占用芯数', 'fun_bdzyxs'),
def fun_bdzyxs(zyxs):
    pass

# ('A端至B端占用率', 'fun_adzbdzyl'),
def fun_adzbdzyl(zyl,yz = int, zs = int):
    if yz == 0 or zs == 0:
        return "'" + str(float(zyl,2))
    elif yz != 0 or zs != 0:
        return "'" + str(float(yz/zs,2))

# ('A端至B端主要铺设方式', 'fun_adzbdzypsfs'),
def fun_adzbdzypsfs(fs):
    pass

# ('A端至B端光缆建设年份', 'fun_adzbdgljsnf'),
def fun_adzbdgljsnf(nf):
    if nf != '':
        return "'" + str(int(nf))
    else:
        return ""

# ('A端至B端光纤资源可用状态', 'fun_adzbdgxzykyzt'),
def fun_adzbdgxzykyzt(kyzt):
    return kyzt.strip(' ')

# ('A端至B端是否有竣工', 'fun_adzbdsfyjg'),
def fun_adzbdsfyjg(jg):
    return jg.strip(' ')

# ('A端至B端路由描述', 'fun_adzbdlyms'),
def fun_adzbdlyms(ms):
    return ms.strip(' ')

# ('A端备注', 'fun_adbz'),
def fun_adbz(bz):
    return bz.strip(' ')

# ('B端备注', 'fun_bdbz'),
def fun_bdbz(bz):
    return bz.strip(' ')

# ('A端至B端光缆备注', 'fun_adzbdglbz'),
def fun_adzbdglbz(lbz):
    return lbz.strip(' ')

# ('信息填报单位', 'fun_xxtbdw')
def fun_xxtbdw(dw):
    return dw.strip(' ')

