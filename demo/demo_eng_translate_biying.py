import urllib.request
from lxml import etree
import re
import time
from functools import reduce

#获得页面数据
def get_page(myword):
    basurl = "http://cn.bing.com/dict/search?q="
    searchurl=basurl+myword
    response =  urllib.request.urlopen(searchurl)
    html = response.read()
    return html

#获得单词释义
def get_chitiao(html_selector):
    chitiao=[]
    hanyi_xpath='/html/body/div[1]/div/div/div[1]/div[1]/ul/li'
    get_hanyi=html_selector.xpath(hanyi_xpath)
    for item in get_hanyi:
        it=item.xpath('span')
        chitiao.append('%s||%s'%(it[0].text,it[1].xpath('span')[0].text))
    if len(chitiao)>0:
        print(chitiao)
        return reduce(lambda x, y:"%s||||%s"%(x,y),chitiao)
    else:
        return ""

#获得单词音标和读音连接
def get_yingbiao(html_selector):
    yingbiao=[]
    yingbiao_xpath='/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div'
    bbb="(https\:.*?mp3)"
    reobj1=re.compile(bbb,re.I|re.M|re.S)
    get_yingbiao=html_selector.xpath(yingbiao_xpath)
    for item in get_yingbiao:
        it=item.xpath('div')
        if len(it)>0:
            ddd=reobj1.findall(it[1].xpath('a')[0].get('onmouseover',None))
            yingbiao.append("%s||%s"%(it[0].text,ddd[0]))
            ddd=reobj1.findall(it[3].xpath('a')[0].get('onmouseover',None))
            yingbiao.append("%s||%s"%(it[2].text,ddd[0]))
    if len(yingbiao)>0:
        return reduce(lambda x, y:"%s||||%s"%(x,y),yingbiao)
    else:
        return ""

#获得例句
def get_liju(html_selector):
    liju=[]
    get_liju_e=html_selector.xpath('//*[@class="val_ex"]')
    get_liju_cn=html_selector.xpath('//*[@class="bil_ex"]')
    get_len=len(get_liju_e)
    for i in range(get_len):
        liju.append("%s||%s"%(get_liju_e[i].text,get_liju_cn[i].text))
    if len(liju)>0:
        return reduce(lambda x, y:"%s||||%s"%(x,y),liju)
    else:
        return ""

def get_word(word):
    #获得页面
    pagehtml=get_page(word)
    selector = etree.HTML(pagehtml.decode('utf-8'))
    #单词释义
    chitiao=get_chitiao(selector)
    #单词音标及读音
    yingbiao=get_yingbiao(selector)
    #例句
    liju=get_liju(selector)
    print (chitiao)
    return "%s\t%s\t%s\t%s"%(word,yingbiao,chitiao,liju)

"""
filename=r'C:/Users/Administrator/Desktop/1.txt'
f=open(filename,"r")
words=f.readlines()
f.close()
filename2='5_jieguo.txt'
f=open(filename2,"wb")
i=0
for word in words:
    time.sleep(0.2)
    print(word.rstrip(),i)
    word_line=get_word(word.rstrip())
    f.write("%s\n"%(word_line))
    i=i+1
f.close()
"""
print(get_word('word'))