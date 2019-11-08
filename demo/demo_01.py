import thulac
ch_text = """
                 《锦瑟》--李商隐
    锦瑟无端五十弦，一弦一柱思华年。
    庄生晓梦迷蝴蝶，望帝春心托杜鹃。
    沧海月明珠有泪，蓝田日暖玉生烟。
    此情可待成追忆，只是当时已惘然。 
"""
thu1 = thulac.thulac()  #默认模式
# i_str = 'Fendi'
# print(i_str[:2],i_str[2:])


text = thu1.cut(ch_text, text=True)  #进行一句话分词
print(type(text),text)