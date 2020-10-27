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