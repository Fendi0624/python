import  win32com.client#系统客户端包
speaker=win32com.client.Dispatch("SAPI.SPVOICE")#系统接口

# file_read = open(r'‪C:\Users\Administrator\Desktop\Python脏数据处理.txt','r')

try:
    # 词频统计.word_translate_add(file_read)
    speaker.Speak("""
                 《锦瑟》--李商隐
    锦瑟无端五十弦，一弦一柱思华年。
    庄生晓梦迷蝴蝶，望帝春心托杜鹃。
    沧海月明珠有泪，蓝田日暖玉生烟。
    此情可待成追忆，只是当时已惘然。 
""")
    speaker.Speak(" Two wrongs don't make a right")
except Exception as e:
    print(e)
finally:
    print("Done!")

# file_read.close()