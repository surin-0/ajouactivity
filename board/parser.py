#activity/parser.py
#web scraping

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

from .models import Post

def parse_activity() : 
    id_list = find_id()
    base_url = 'https://www.wevity.com/?c=active&s=1&gbn=viewok&gp=1&ix={}'
    
    for n in id_list :
        flag = False
        url = base_url.format(n)
        webpage = urlopen(url)
        soup = BeautifulSoup(webpage, 'html.parser')
        my_title = soup.select('#container > div.content-area > div.content-wrap > div.content > div > div.tit-area > h6')[0]
        my_img = soup.select('#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.img > div.thumb > img')[0]
        my_link = soup.select('#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li:nth-child(8) > a')
        #viewContents > p:nth-child(1)
        if my_link :
            my_company = my_link[0].get('href')
        else : 
            my_company = " "
        my_dcrp = soup.select('#viewContents > div')
        if not my_dcrp:
            my_dcrp = soup.select('#viewContents > p')
        my_dday = soup.select('#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li.dday-area')[0]
        tmp_src = my_img.get('src')
        tmp_src = "https://www.wevity.com" + tmp_src
        tmp_daylist = my_dday.text.split()
        tmp_day = " ".join(tmp_daylist[1:4])
        # tmp_day = " ".join(tmp_daylist[1:2])
        tmp_dcrp = ""
        for i in my_dcrp :
            tmp_dcrp = tmp_dcrp + i.text + "\n"
        a = Post(title = my_title.text, description = tmp_dcrp, company = my_company, created_at =tmp_day, image = tmp_src)
        dup = Post.objects.filter(title = my_title.text)
        
        if(dup):
            flag = True
            continue
        else : 
            a.save()
        if(flag):
            print("flag act")
            break

def find_id():
    base_url = 'https://www.wevity.com/?c=active&s=1&gp={}'
    id_list = []
    for n in range (1,2) :
        url = base_url.format(n)
        webpage = urlopen(url)
        soup = BeautifulSoup(webpage, 'html.parser')
        for i in range(0,12) :
            tmp = soup.select('#container > div.content-area > div.content-wrap > div.content > div.ext-area > ul > li> a')[i]
            li = tmp.get('href').split('=')
            id_list.append(li[len(li)-1])
    return id_list
    
if __name__ == '__main__' :
    parse_activity()