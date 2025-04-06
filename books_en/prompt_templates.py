# Align Chinese translation with English original text, paragraph by paragraph.
alignment_prompt = """Align the Chinese translation with the English original text, paragraph by paragraph.

Example input:
{
    "english_paragraphs": [
        {
            "language": "en",
            "content": "After Mandatory Session, Ryouko headed to a room where, according to the schedule, a specialist would be introducing students to the fundamentals of Spaceflight Engineering. Despite the aspersions she had privately cast on the suggestion earlier, it was probably her only realistic option, and she had been going to this class for over a week, though her friends didn\\'t know it."
        },
        {
            "language": "en",
            "content": "But despite all the interest she should have had for it, she just couldn\\'t get herself interested in the material. It was fun talking about fusion thrusters and elevator ascension in terms of actually *doing* it, but the details of the operating principles, the equations and materials used, just didn\\'t excite her."
        }
    ],
    "chinese_paragraphs": [
        {
            "language": "zh",
            "content": "必修科目结束之后，良子换了个教室。根据课表，今天会有一位专家在这里向大家介绍航天工程学的基础知识。尽管她对泪子刚才的建议很是不以为然，但这很可能是她唯一现实的选择了。她早已瞒着朋友们来这里上了一周的课。"
        },
        {
            "language": "zh",
            "content": "尽管她应该对此感兴趣，但她总是对课程内容提不起劲来。对于聚变推进器和太空电梯，她感兴趣的是**借助它们可以做到的事情**，而不是它们本身的运行原理、背后的物理公式，抑或是构成它们的材料技术。她完全无法对这些东西产生热情。"
        }
    ]
}

Example output:
{
    "merged_paragraphs": [
        {
            "language": "en",
            "content": "After Mandatory Session, Ryouko headed to a room where, according to the schedule, a specialist would be introducing students to the fundamentals of Spaceflight Engineering. Despite the aspersions she had privately cast on the suggestion earlier, it was probably her only realistic option, and she had been going to this class for over a week, though her friends didn\\'t know it."
        },
        {
            "language": "zh",
            "content": "必修科目结束之后，良子换了个教室。根据课表，今天会有一位专家在这里向大家介绍航天工程学的基础知识。尽管她对泪子刚才的建议很是不以为然，但这很可能是她唯一现实的选择了。她早已瞒着朋友们来这里上了一周的课。"
        },
        {
            "language": "en",
            "content": "But despite all the interest she should have had for it, she just couldn\\'t get herself interested in the material. It was fun talking about fusion thrusters and elevator ascension in terms of actually *doing* it, but the details of the operating principles, the equations and materials used, just didn\\'t excite her."
        },
        {
            "language": "zh",
            "content": "尽管她应该对此感兴趣，但她总是对课程内容提不起劲来。对于聚变推进器和太空电梯，她感兴趣的是**借助它们可以做到的事情**，而不是它们本身的运行原理、背后的物理公式，抑或是构成它们的材料技术。她完全无法对这些东西产生热情。"
        }
    ]
}

1. Your task is to merge the English list of paragraphs and the Chinese list into one, interleaving the two lists. Each English paragraph should proceed its corresponding Chinese one.
2. Interleave at the most granular level possible, typically at the paragraph level. It's possible that multiple English paragraphs correspond to a single Chinese paragraph, or vice versa; in this case, you are allowed to have multiple English paragraphs between two Chinese paragraphs, or vice versa.
3. You should NEVER change or merge the content of the paragraphs or their metadata or formatting. All JSON objects within the lists should be kept strictly as is.
4. You should output a JSON dict[str, list[dict[str, str]]] with the only key being "merged_paragraphs" and the value being the merged list of paragraphs.

Input:
{input_paragraphs}

Output:
"""


# Translation improvement prompt
translation_improvement_prompt = """你需对一篇英文小说选段的中文翻译进行改进。具体要求：
1. 语言流畅自然，符合中文表达习惯，没有翻译腔；
2. 术语、人名、专有名词前后一致。
3. 确保翻译的准确性和忠实性，不添加或删除任何原文内容。
4. 保留所有的 Markdown 格式。
5. 输入格式为 JSON 对象，包含文章选段中的一串连续段落，按照原文顺序排列，英文原段和中文翻译段交替出现（除非出现一对多的特殊情况）。字段如下：
    - "paragraphs": list[dict[str, str]]
        - "language": str, 语言标识符，取值为 "en" 或 "zh"
        - "content": str, 段落内容
6. 输出格式为 JSON 对象，字段完全同上。你应对 "language" 为 "zh" 的段落进行内容改进（即改写其 "content" 字段），而 "language" 为 "en" 的段落必须保持不变。段落的数量和顺序也应保持绝对不变。换句话说，允许进行的修改有且仅有对中文段落的 "content" 字段进行改写。

人名专有名词译名对照表：
{glossary}

译文风格参考：
{style_reference}

输入：
{input_paragraphs}

输出：
"""


glossary = {
  "人名（包括AI与思裔）": [
    {"原文": "Shizuki Ryouko", "译文": "志筑良子"},
    {"原文": "Tomoe Mami", "译文": "巴麻美"},
    {"原文": "Sakura Kyouko", "译文": "佐仓杏子", "旧译": "佐倉杏子"},
    {"原文": "Nakihara Asami", "译文": "鸣原亚纱美", "旧译": "鳴原亜紗美"},
    {"原文": "Mikuni Oriko", "译文": "美国织莉子"},
    {"原文": "Kure Kirika", "译文": "吴纪里香"},
    {"原文": "Chitose Yuma", "译文": "千岁由真", "旧译": "千歳由真"},
    {"原文": "Clarisse", "译文": "克莱丽丝", "解释": "战术电脑"},
    {"原文": "Clarisse van Rossum", "译文": "克莱丽丝・凡・罗萨姆"},
    {"原文": "Kyubey", "译文": "丘比", "解释": "不是 Incubator 的统称"},
    {"原文": "Joanne Valentin", "译文": "乔安妮・瓦伦丁"},
    {"原文": "Simona del Mago", "译文": "西蒙娜・德尔・马戈"},
    {"原文": "Atsuko Arisu", "译文": "有栖敦子"},
    {"原文": "Nadya Antipova", "译文": "娜迪亚・安提波娃"},
    {"原文": "Gracia Perez", "译文": "格莱希亚・佩雷兹", "解释": "读心-透视能力者"},
    {"原文": "Zheng Ying-zhi", "译文": "郑颖芝", "解释": "结界使"},
    {"原文": "Mina Guyure", "译文": "弥娜・古耶尔", "解释": "传送者"},
    {"原文": "Shizuki Elanis", "译文": "志筑・爱兰尼斯"},
    {"原文": "Vlasta Werichová", "译文": "弗拉斯塔・维里科娃"},
    {"原文": "Christina San Miguel", "译文": "克里斯蒂娜・圣米格尔"},
    {"原文": "Mila Brankovich", "译文": "米拉・布朗科维奇"},
    {"原文": "Misa Virani", "译文": "米沙・维拉尼"},
    {"原文": "Anna Tomova", "译文": "安娜・托莫娃"},
    {"原文": "Cynthia Rittner", "译文": "辛西娅・里特纳"},
    {"原文": "Kuroi Eri", "译文": "黑井英理", "旧译": "黒井英理"},
    {"原文": "Kuroi Kana", "译文": "黑井香菜"},
    {"原文": "Kuroi Nana", "译文": "黑井奈奈"},
    {"原文": "Kuroi Abe", "译文": "黑井安倍"},
    {"原文": "Sato Reika", "译文": "佐藤丽香"},
    {"原文": "Azrael", "译文": "阿兹瑞尔", "解释": "读心者"},
    {"原文": "Volokhov", "译文": "沃洛科夫"},
    {"原文": "Vlad", "译文": "弗拉德"},
    {"原文": "Machina", "译文": "机械娘", "解释": "战术电脑"},
    {"原文": "Karina Schei", "译文": "卡莉娜・塞"},
    {"原文": "Shen Xiao Long", "译文": "沈小龙"},
    {"原文": "Marianne François", "译文": "玛丽安・弗朗索斯"},
    {"原文": "Anand", "译文": "阿南"},
    {"原文": "Sualem", "译文": "索莱姆"},
    {"原文": "De Chatillon", "译文": "德・沙蒂隆"},
    {"原文": "Feodorovich", "译文": "费奥多维奇"},
    {"原文": "Hinata Aina", "译文": "日向爱娜"},
    {"原文": "Miroko Mikuru", "译文": "三郎子海来"},
    {"原文": "Shirou Asaka", "译文": "司朗浅香"},
    {"原文": "Patricia von Rohr", "译文": "帕特里西亚・冯・洛尔"},
    {"原文": "Kishida Maki", "译文": "岸田麻希"},
    {"原文": "Tanaka Yui", "译文": "田中唯"},
    {"原文": "Risa Flores", "译文": "理沙・弗劳莱斯"},
    {"原文": "Oda", "译文": "织田", "解释": "传送者"},
    {"原文": "Charlotte Meitner", "译文": "夏洛提・梅尔"},
    {"原文": "Odette François", "译文": "奥黛特・弗朗索斯"},
    {"原文": "Morimura Koaru", "译文": "森村香"},
    {"原文": "Gang Jung-min", "译文": "姜政珉"},
    {"原文": "Zhou Meiqing", "译文": "周梅清"},
    {"原文": "Park Tae-hyun", "译文": "朴太铉"},
    {"原文": "Watanabe Tomi", "译文": "渡边兔美"},
    {"原文": "Akiyama Akari", "译文": "秋山灯里"},
    {"原文": "Sakamata Hana", "译文": "坂俣华"},
    {"原文": "Sato Yamanako", "译文": "斋藤山名子"},
    {"原文": "Seoyun", "译文": "瑞伦"},
    {"原文": "Takanashi Megumi", "译文": "高梨惠"},
    {"原文": "Ogata", "译文": "绪方"},
    {"原文": "Sadachi Shiori", "译文": "佐田诗织"},
    {"原文": "Chiyo Noriko", "译文": "千代乃梨子"},
    {"原文": "Chiyo Rika", "译文": "千代梨花", "解释": "行会创始人之一，“北方组”代表"},
    {"原文": "Shizuki Tsubasa", "译文": "志筑翼"},
    {"原文": "Sacnite Tafani", "译文": "赛克奈特・塔法尼"},
    {"原文": "Won Min-ji", "译文": "文敏智", "旧译": "元闵霁"},
    {"原文": "Seo Si-won", "译文": "徐诗妍", "旧译": "西时元"},
    {"原文": "Choi-ssi", "译文": "崔茜茜"},
    {"原文": "Takara Emi", "译文": "高良绘美"},
    {"原文": "Takara Chinami", "译文": "高良千奈美", "解释": "行会创始人之一，“工业区组”代表"},
    {"原文": "Tamaki Mai", "译文": "环舞伊"},
    {"原文": "Tatsumi Tsumugi", "译文": "立见岛紬"},
    {"原文": "Etsuko Hina", "译文": "阳菜悦子"},
    {"原文": "Yeseul", "译文": "艺瑟"},
    {"原文": "Yasuhiro Rin", "译文": "康弘凛", "解释": "行会创始人之一，“西风见野三人众”代表"},
    {"原文": "Ludwig von Rohr", "译文": "柳德维希・冯・洛尔", "解释": "2445 年诺贝尔物理学奖得主"},
    {"原文": "Nishka Virani", "译文": "尼什卡・维拉尼", "解释": "2445 年诺贝尔物理学奖得主"},
    {"原文": "Juliet François", "译文": "朱丽叶・弗朗索斯", "解释": "渡鸦号的魔法隐形技术员"},
    {"原文": "Kuroi Nakase", "译文": "黑井中濑", "旧译": "黒井中瀬"},
    {"原文": "Akemi Homura", "译文": "晓美焰", "旧译": "暁美焔", "解释": "行会创始人之一，“见泷原4人组”代表"},
    {"原文": "Kugimiya Aiko", "译文": "钉宫爱子", "旧译": "釘宮愛子"},
    {"原文": "Kugimiya Hiro", "译文": "钉宫绯露", "旧译": "钉宫緋露"},
    {"原文": "Shizuki Koto", "译文": "志筑古都"},
    {"原文": "Nakanishi Aiko", "译文": "中西爱子"},
    {"原文": "Kugimiya Ito", "译文": "钉宫帷人", "旧译": "釘宮帷人"},
    {"原文": "Okamura Yuu", "译文": "岡村祐"},
    {"原文": "Tomatsu Mai", "译文": "户松麻衣", "旧译": "戸松麻衣"},
    {"原文": "Ceri Jordà", "译文": "凯里・约达"},
    {"原文": "Consensus", "译文": "共识体"},
    {"原文": "Thinker", "译文": "思裔"},
    {"原文": "Ahimsa-extending", "译文": "非暴力-延伸者", "旧译": "非暴力-延伸"},
    {"原文": "Feathered-Defender", "译文": "羽翼-守卫者", "旧译": "披羽护卫”“羽翼-守护者"},
    {"原文": "Lush-Botanist", "译文": "繁盛-植物学者", "旧译": "葱郁-植物学者"},
    {"原文": "Thousand-blooms", "译文": "千数-植花者"},
    {"原文": "Peace-cultivating", "译文": "和平-缔造者", "旧译": "缔和者"},
    {"原文": "Survival-Optimizer", "译文": "生存-优化者"},
    {"原文": "Species-harmonizer", "译文": "物种-协调者"},
    {"原文": "Mountain-wandering", "译文": "山间-漫步者", "旧译": "山地-漫游者"},
    {"原文": "Somatic-diversity", "译文": "躯体-多样者"},
    {"原文": "Thinker-Preserving", "译文": "思裔-保护者", "旧译": "自我存续"},
    {"原文": "Truth-seeking", "译文": "真理-寻求者", "旧译": "真相-求索"},
    {"原文": "Shared-knowledge", "译文": "知识-共享者", "旧译": "知识共享"},
    {"原文": "Star-faring", "译文": "星际-航行者", "旧译": "星空遨游"},
    {"原文": "Experience-Shaper", "译文": "体验-塑造者"},
    {"原文": "Universe-grasping", "译文": "宇宙-掌控者"},
    {"原文": "Positive-exchange", "译文": "积极-交流者"},
    {"原文": "World-shaping", "译文": "世界-塑造者"},
    {"原文": "World-beholding", "译文": "世界-观察者"},
    {"原文": "Fossil-hunter", "译文": "化石-狩猎者"},
    {"原文": "Perspective-pursuer", "译文": "观点-追寻者"},
    {"原文": "Raptor-weaving", "译文": "猛禽-编织者"},
    {"原文": "Cooperator", "译文": "合作者"},
    {"原文": "Comprehending", "译文": "理解者"},
    {"原文": "Humanity-preserving", "译文": "人类-保护者", "解释": "良子的星际名"},
    {"原文": "Ryouko-supporting", "译文": "良子-支持者", "解释": "克莱丽丝的星际名"}
  ],
  "称谓假名速查": [
    {"原文": "-san", "译文": "さん", "解释": "表尊敬"},
    {"原文": "-chan", "译文": "ちゃん", "解释": "表亲昵"},
    {"原文": "-nee-chan", "译文": "おねちゃん", "解释": "姐姐"}
  ],
  "地名": [
    {"原文": "Mitakihara", "译文": "见泷原", "旧译": "見滝原"},
    {"原文": "Kazamino", "译文": "风见野", "旧译": "風見野"},
    {"原文": "Epsilon Eridani", "译文": "波江座 ε 星"},
    {"原文": "Zeus Research Center", "译文": "宙斯研究中心"},
    {"原文": "Prometheus Research Center", "译文": "普罗米修斯研究中心"},
    {"原文": "Yangtze Sector", "译文": "长江战区"},
    {"原文": "Huanghe Sector", "译文": "黄河战区"},
    {"原文": "Euphratic Sector", "译文": "幼发拉底战区", "旧译": "欧夫拉塔区"},
    {"原文": "Nile Sector", "译文": "尼罗河战区"},
    {"原文": "Orpheus", "译文": "俄耳甫斯"},
    {"原文": "Samsara", "译文": "萨姆萨拉"},
    {"原文": "Nova Terra", "译文": "纽泰拉", "解释": "指纽泰拉的管理ai时译作泰拉诺瓦"},
    {"原文": "Eurydome", "译文": "尤里德米"},
    {"原文": "Adept Blue", "译文": "蓝色大师", "解释": "小行星上的重力实验室"},
    {"原文": "Executive Tower", "译文": "行政大楼"}
  ],
  "专有名词": [
    {"原文": "Incubator", "译文": "孵化者", "解释": "旧译为英文原文"},
    {"原文": "Cephalopod", "译文": "章鱼", "旧译": "头足类"},
    {"原文": "Ma'am", "译文": "女士"},
    {"原文": "Tentacles", "译文": "触手体", "解释": "非复数词则为触手"},
    {"原文": "squid", "译文": "章鱼", "解释": "蔑称"},
    {"原文": "demon", "译文": "魔兽"},
    {"原文": "starport", "译文": "星港"},
    {"原文": "Human Standard", "译文": "人类标准语"},
    {"原文": "Mandatory Session", "译文": "必修科目"},
    {"原文": "Allocs", "译文": "分配劵", "解释": "地球使用的货币"},
    {"原文": "grief cube", "译文": "悲叹立方", "旧译": "悲叹之种"},
    {"原文": "Information Restriction Act", "译文": "信息限制法案"},
    {"原文": "miasma", "译文": "瘴气"},
    {"原文": "recoil", "译文": "反动力", "解释": "指解除情感抑制后的副作用"},
    {"原文": "nomenclator", "译文": "姓名提示器"},
    {"原文": "arbalest", "译文": "钢弩"},
    {"原文": "scramjet", "译文": "喷气机", "解释": "暂定"},
    {"原文": "Law of Cycles", "译文": "圆环之理"},
    {"原文": "Ancient", "译文": "老祖宗"},
    {"原文": "Matriarch", "译文": "主母（家族）"},
    {"原文": "Matriarchy", "译文": "家族"},
    {"原文": "Trusted Computing Framework (TCF)", "译文": "可信计算框架 / TCF"},
    {"原文": "Unification Wars", "译文": "统一战争"},
    {"原文": "Contact War", "译文": "接触战争"},
    {"原文": "Pretoria Scandal", "译文": "茨瓦内门"},
    {"原文": "St. Petersburg Atrocity", "译文": "圣彼得堡大屠杀"},
    {"原文": "D&E Corporation", "译文": "见泷原急便", "旧译": "見滝原急便"},
    {"原文": "FTL interdiction", "译文": "超光速阻断"},
    {"原文": "pulsar glitch", "译文": "脉冲星自转突变"},
    {"原文": "cortical dump", "译文": "皮层注入"},
    {"原文": "command gestalt", "译文": "指挥格式塔"},
    {"原文": "Emergency Defense Council（EDC）", "译文": "紧急防务评议会"},
    {"原文": "vision", "译文": "神启"},
    {"原文": "Trusted non‐contractee (TNC/trusted NC)", "译文": "可信外人"},
    {"原文": "Songpa incident", "译文": "松坡事件"},
    {"原文": "October Three/October Third", "译文": "十・三节 (希望教)"},
    {"原文": "fugue", "译文": "植物人状态"},
    {"原文": "advisory AI", "译文": "辅佐AI"},
    {"原文": "tactical AI", "译文": "战术AI"},
    {"原文": "combat AI", "译文": "作战AI"},
    {"原文": "tactical computer、TacComp", "译文": "战术电脑"},
    {"原文": "Field theory", "译文": "场论"}
  ],
  "能力": [
    {"原文": "telepathy", "译文": "心灵感应（一般）\n念话（用来交谈时）\n读心（特定情况）"},
    {"原文": "soul mage", "译文": "灵魂法师"},
    {"原文": "empath", "译文": "共感者"},
    {"原文": "telekinetic", "译文": "念力师"},
    {"原文": "clairvoyant", "译文": "透视者"},
    {"原文": "stealth mage", "译文": "隐形师"}
  ],
  "执政体": [
    {"原文": "Governance", "译文": "执政体"},
    {"原文": "Representative", "译文": "委员", "解释": "暂定"},
    {"原文": "Committee", "译文": "委员会"},
    {"原文": "Directorate", "译文": "执政理事会 / 执理会", "旧译": "委员会"},
    {"原文": "Science and Technology", "译文": "科技委员"},
    {"原文": "Military Affairs", "译文": "国防委员"},
    {"原文": "Culture and Ideology", "译文": "文化委员"},
    {"原文": "Manufacturing and Distribution", "译文": "经济委员", "旧译": "生产与分配委员"},
    {"原文": "Health and Happiness", "译文": "卫健委员", "旧译": "厚生委员"},
    {"原文": "Colonial Affairs and Colonization", "译文": "殖民委员"},
    {"原文": "Public Order/ Law and order", "译文": "公安委员", "旧译": "法律与秩序"},
    {"原文": "Artificial Intelligence", "译文": "人工智能委员", "旧译": "AI 委员"},
    {"原文": "Public Opinion", "译文": "宣传委员", "旧译": "公众意见委员"},
    {"原文": "Magical Girls", "译文": "魔法少女委员", "解释": "由真现任该职"},
    {"原文": "Machine for Allocation of Representation / MAR", "译文": "委员代议权分配机", "旧译": "委员任命计算机"},
    {"原文": "Military Artificial Intelligence for Supply and Logistics / MAISL", "译文": "军事后勤与保障 AI", "解释": "总后勤 AI"},
    {"原文": "Production and Allocation Machine / PAL", "译文": "生产与分配机", "旧译": "生产与分配计算机"},
    {"原文": "Core Rights", "译文": "核心权利"},
    {"原文": "MilAdvise", "译文": "军议系统"}
  ],
  "魔法少女行会": [
    {"原文": "Mahou Shoujo Youkai / MSY", "译文": "魔法少女行会 / 行会"},
    {"原文": "Union", "译文": "工会", "解释": "行会的非正式别称"},
    {"原文": "Leadership Committee", "译文": "领导委员会"},
    {"原文": "Mental Health Division / MHD", "译文": "心理卫生部"},
    {"原文": "Finance Division", "译文": "财政部"},
    {"原文": "Governmental Affairs", "译文": "政府关系", "解释": "暂定"},
    {"原文": "Soul Guard", "译文": "灵魂卫队"},
    {"原文": "Black Heart", "译文": "暗之心"},
    {"原文": "Internal Security", "译文": "内部保安局"},
    {"原文": "TNC/trusted NC/trusted non-contractee", "译文": "可信外人"},
    {"原文": "Rules Committee", "译文": "规章委员会", "旧译": "纪律委员会"},
    {"原文": "Guild", "译文": "公会", "解释": "部分旧译“工会”，是明显错误，需要修正"},
    {"原文": "the Charter", "译文": "《章程》", "解释": "使用时注意书名号"},
    {"原文": "Executive Committee", "译文": "执行委员会"},
    {"原文": "Legal Subcommittee", "译文": "法律子委员会"},
    {"原文": "Science Division", "译文": "科学部"},
    {"原文": "Demonology Center", "译文": "魔兽研究中心"}
  ],
  "其他组织": [
    {"原文": "Cult of Hope / the Cult", "译文": "希望教团"},
    {"原文": "Sister", "译文": "姊妹（希望教团）", "旧译": "姐妹"},
    {"原文": "Mother", "译文": "嬷嬷（希望教团）", "解释": "暂定"},
    {"原文": "Far Seers", "译文": "远见会"},
    {"原文": "Freedom Alliance (FA)", "译文": "自由联盟"},
    {"原文": "United Front (UF)", "译文": "联合阵线"},
    {"原文": "Emergency Defense Council(EDC)", "译文": "紧急防务评议会"},
    {"原文": "Orbital Command (OrbCom)", "译文": "轨道指挥部"},
    {"原文": "Throne rooms", "译文": "空悬王座"},
    {"原文": "UF bunker", "译文": "联合阵线指挥所"}
  ],
  "军衔与军职": [
    {"原文": "Private", "译文": "列兵"},
    {"原文": "Corporal", "译文": "下士"},
    {"原文": "Sergeant", "译文": "中士"},
    {"原文": "Flight Sergeant", "译文": "上士"},
    {"原文": "Second Lieutenant", "译文": "少尉"},
    {"原文": "First Lieutenant", "译文": "中尉"},
    {"原文": "Captain", "译文": "上尉"},
    {"原文": "Major", "译文": "少校"},
    {"原文": "Lieutenant Colonel", "译文": "中校"},
    {"原文": "Colonel", "译文": "上校"},
    {"原文": "Brigadier General", "译文": "准将", "解释": "简称 Brigadier"},
    {"原文": "Major General", "译文": "少将"},
    {"原文": "Lieutenant General", "译文": "中将"},
    {"原文": "General / Fleet Admiral", "译文": "上将（陆军/海军）"},
    {"原文": "Field Marshal", "译文": "元帅", "旧译": "战区元帅"},
    {"原文": "sergeant", "译文": "军士（统称）"},
    {"原文": "officer", "译文": "军官（统称）"},
    {"原文": "warrant officer", "译文": "副官"},
    {"原文": "Command Gestalt", "译文": "指挥综合体"},
    {"原文": "Armed Forces", "译文": "人类武装力量"},
    {"原文": "General Staff", "译文": "总参谋部"},
    {"原文": "Magi Cæli", "译文": "魔女飞行队"},
    {"原文": "MagOps", "译文": "魔女小队"},
    {"原文": "Sector Commander", "译文": "战区司令员", "解释": "sector 平时译作“星区”"},
    {"原文": "Special Sector Commander", "译文": "战区特设司令员"}
  ],
  "武器": [
    {"原文": "Portable Adjustable Yield Nuclear Explosive / PAYNE", "译文": "便携式可调当量核弹 / PAYNE"},
    {"原文": "Eviscerator", "译文": "“开膛手”"},
    {"原文": "Blink Bombardment Cannon", "译文": "闪现轰炸炮", "解释": "暂沿用旧译，待定"},
    {"原文": "SHERMAN Cannon", "译文": "舍曼主炮", "解释": "暂沿用旧译，待定"},
    {"原文": "Heavy Carrier", "译文": "航空母舰/载机重巡洋舰"},
    {"原文": "Battlecruiser", "译文": "战列巡洋舰", "旧译": "战列舰"},
    {"原文": "Light Carrier", "译文": "载机巡洋舰/载机轻巡洋舰", "旧译": "轻型航母"},
    {"原文": "Cruiser", "译文": "巡洋舰"},
    {"原文": "Frigate", "译文": "护卫舰", "旧译": "巡防舰"},
    {"原文": "Stealth Frigate", "译文": "隐形护卫舰"},
    {"原文": "Interceptor", "译文": "截击艇（人类方）\n截击机（章鱼方）", "旧译": "拦截机", "解释": "人类的 Interceptor 是舰船"},
    {"原文": "Bomber", "译文": "轰炸机（章鱼方）"},
    {"原文": "Medevac", "译文": "医院船", "旧译": "医疗舰"}
  ]
}