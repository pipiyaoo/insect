import requests
import re
from bs4 import BeautifulSoup
from datetime import date,timedelta
def combine(url):
    req=requests.get(url)#包含日期的网址
    soup=BeautifulSoup(req.text,"html.parser")
    soup2=soup.find_all("div",class_="border_a")
    if(soup2==[]):
        print("当天无比赛")
        exit()
    for tag in soup2:#遍历每个比赛的div
        #找到战报链接
        tag_zhanbao=tag.find("p",class_="tips")
        url_zhanbao=tag_zhanbao.a.get('href')
        number=re.sub("\D","",url_zhanbao)
        print("该场比赛编号："+number)
        #找到数据统计链接
        tag_shuju=tag.find("a",class_="d")
        url_shuju=tag_shuju.get('href')
        #找到文字实录链接
        tag_wenzi=tag.find("a",class_="b")
        url_wenzi=tag_wenzi.get('href')
        #爬取战报信息
        req_zhanbao=requests.get(url_zhanbao)
        soup_zhanbao=BeautifulSoup(req_zhanbao.text,"html.parser")
        soup2_zhanbao=soup_zhanbao.find("div","content")
        for tags_zhanbao in soup2_zhanbao.find_all("p"):
            print(tags_zhanbao.string)
        #爬取文字实录
        req_wenzi=requests.get(url_wenzi)
        soup_wenzi=BeautifulSoup(req_wenzi.text,"html.parser")
        soup2_wenzi=soup_wenzi.find("div","table_list_live playbyplay_td table_overflow")
        for tags_wenzi in soup2_wenzi.find_all("tr"):
            for tags2_wenzi in tags_wenzi.find_all("td"):
                print(tags2_wenzi.string)
        #爬取数据统计
        req_shuju=requests.get(url_shuju)
        soup_shuju=BeautifulSoup(req_shuju.text,"html.parser")
        soup2_shuju=soup_shuju.find("table",id="J_away_content")
        for tags_shuju in soup2_shuju.find_all("tr"):
            for tags2_shuju in tags_shuju.find_all("td"):
                if(tags2_shuju.string!=None):
                    print(tags2_shuju.string.strip())
                else:
                    if(tags2_shuju.span!=None):
                        print(tags2_shuju.span.string)
        #爬取比分
        req_bifen=requests.get(url_shuju)
        soup_bifen=BeautifulSoup(req_bifen.text,"html.parser")
        soup2_bifen=soup_bifen.find("table",class_="itinerary_table")
        for tags_bifen in soup2_bifen.find_all("tr"):
            for tags2_bifen in tags_bifen.find_all("td"):
                if(tags2_bifen.string!=None):
                    print(tags2_bifen.string.strip())


def gen_dates(bdate,days):
    day = timedelta(days=1)
    for i in range(days):
        yield bdate + day*i
bdate = date(2018, 5, 8)
for d in gen_dates(bdate,1):
    data = d.strftime('%Y-%m-%d')
    url="https://nba.hupu.com/games/"+data
    combine(url)




