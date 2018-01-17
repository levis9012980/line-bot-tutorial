# -*- encoding: utf8-*-
import requests,re
from bs4 import BeautifulSoup
from random import choice
def main():
    # getlist()
    pass

def getlist():
    getHTML = requests.get("http://www.timliao.com/bbs/forumdisplay.php?fid=18&filter=0&orderby=dateline&ascdesc=DESC")
    HTML = getHTML.text
    soup = BeautifulSoup(HTML,"html.parser")
    timliaotable = soup.find("div",class_="screenlimit-forumdisplay-940 clearfix")
    _list = dict()
    for data in timliaotable.find_all("li"):
        try:
            timliaourl = "http://www.timliao.com/bbs/"
            _img = data.find("img")["src"]
            _href = data.find("a")["href"]
            img = timliaourl+str(_img)
            href = timliaourl + str(_href)
            tid = re.search(r'viewthread\.php\?tid=([0-9]+)$',_href).group(1)
            _list[img] = href
        except:
            pass
    return _list


if __name__ == '__main__':
    main()