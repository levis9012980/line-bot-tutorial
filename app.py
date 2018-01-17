import requests
import re
import random
from bs4 import BeautifulSoup
import feedparser
import json
from imgurpython import ImgurClient
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import func.mega as mega
import func.timliao as timliao
from config.config import imageconfig

app = Flask(__name__)

line_bot_api = LineBotApi(
    'f5MPBMEvI7tMuBxVnKkb2kcvS8KdDGNoMhJqKkArhOxzSr3mSbs8Osw6GL/9iJL9phoUf9qzSCV30W4hrgjxbbMuSsBzvWEukfMzI8YQ9q+z1CM8Rdq2WuOfueDXllSVazWsW5QBMZ3RnombK7QrMAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('241c6fbaecef54029cea60d45d7da972')


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sendType = event.message.text
    print(event)
    if re.search(r'^\/[\d.]{1,}[+\-*\/][\d.]{1,}$', sendType):
        n1 = re.search(r'\/([\d.]{1,})([+\-*\/])([\d.]{1,})', sendType).group(1)
        n2 = re.search(r'\/([\d.]{1,})([+\-*\/])([\d.]{1,})', sendType).group(2)
        n3 = re.search(r'\/([\d.]{1,})([+\-*\/])([\d.]{1,})', sendType).group(3)
        content = calculationNumber(n1, n3, n2)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=n1 + n2 + n3 + " 計算結果：" + str(content)))
        return 0

    if event.message.text.upper() == "PTT 表特":
        content = ptt_beauty()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text.upper() == "PTT 廢文":
        content = ptt_hot()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text.upper() == "PTT 台中":
        content = get_xml_for_str("http://rss.ptt.cc/TaichungBun.xml")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text.upper() == "PTT 台南":
        content = get_xml_for_str("http://rss.ptt.cc/Tainan.xml")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text.upper() == "PTT 高雄":
        content = get_xml_for_str("http://rss.ptt.cc/Kaohsiung.xml")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text.upper() == "PTT 日本":
        content = get_xml_for_str("http://rss.ptt.cc/Japan_Travel.xml")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text.upper() == "PTT 笨版":
        content = get_xml_for_str("http://rss.ptt.cc/StupidClown.xml")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text.upper() == "PTT 西斯":
        content = get_xml_for_str("http://rss.ptt.cc/sex.xml")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text.upper() == "PTT AV":
        content = get_xml_for_str("http://rss.ptt.cc/japanavgirls.xml")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text.upper() == "PTT 工作":
        content = get_xml_for_str("http://rss.ptt.cc/Tech_Job.xml")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "蘋果即時新聞":
        content = apple_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "免費資源網路社群":
        content = get_xml_for_str("http://feeds.feedburner.com/freegroup/")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text.upper() == "T客邦":
        content = get_xml_for_str("http://feeds.feedburner.com/techbang/")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "就是教不落":
        content = get_xml_for_str("http://feeds.feedburner.com/steach?format=xml")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "電腦玩物":
        content = get_xml_for_str("http://feeds.feedburner.com/playpc")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "小惡魔 最新文章":
        content = get_xml_for_str("http://www.mobile01.com/rss/newtopics.xml")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "小惡魔 單車":
        content = get_xml_for_str("http://www.mobile01.com/rss/topiclist268.xml")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "小惡魔 小米":
        content = get_xml_for_str("http://www.mobile01.com/rss/topiclist634.xml")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text.upper() == "dcard 西斯":
        content = getDcardPost("sex", "false")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "大樂透":
        _list = str(sorted(random.sample(range(1, 49), 6)))
        content = "您的大樂透號碼\n" + _list + "\n\n一起賺大錢吧!"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "威力彩":
        _list1st = sorted(random.sample(range(1, 38), 6))
        _list2st = sorted(random.sample(range(1, 8), 1))
        content = "您的威力彩號碼\n第一區：" + str(_list1st) + "\n"
        content += "第二區：" + str(_list2st) + "\n\n一起賺大錢吧!"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "今彩539":
        _list1st = sorted(random.sample(range(1, 39), 5))
        content = "您的今彩539號碼\n" + str(_list1st) + "\n\n一起賺大錢吧!"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "3星彩":
        _list1st = str(random.randint(0, 9))
        _list2st = str(random.randint(0, 9))
        _list3st = str(random.randint(0, 9))
        content = "您的3星彩號碼\n[" + _list1st + "," + _list2st + "," + _list3st + "]\n\nPS.沒中別怪我XD"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "4星彩":
        _list1st = str(random.randint(0, 9))
        _list2st = str(random.randint(0, 9))
        _list3st = str(random.randint(0, 9))
        _list4st = str(random.randint(0, 9))
        content = "您的4星彩號碼\n[" + _list1st + "," + _list2st + "," + _list3st + "," + _list4st + "]\n\nPS.沒中別怪我XD"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "正妹圖":
        url = "https://i.imgur.com/QZknQYw.jpg"
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0

    if event.message.text == "提姆正妹":
        _list = timliao.getlist()
        country, capital = random.choice(list(_list.items()))  # 隨機dict的一個資料
        content = capital
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "下載工具":
        content = ('SmartGet1.53➽https://goo.gl/344YLn')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if re.search(r'[\d.]{1,}\s[a-zA-Z]{3,4}', sendType):
        atm = re.search(r'([\d.]{1,})\s([a-zA-Z]{3,4})', sendType).group(1)
        cury = re.search(r'([\d.]{1,})\s([a-zA-Z]{3,4})', sendType).group(2)
        result = currency_chang(atm, cury.upper())
        chknumber = is_number(result)
        if chknumber != True:
            content = result
        else:
            am = round(result, 2)
            content = atm + cury.upper() + "=" + str(am) + "台幣"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "hey huihui":
        content = ('▁▂▃▄▅▆甲甲專用指令▆▅▄▃▂▁\n'
                   '軟體推廣，一樣有機器人\n'
                   '名稱：Telegram\n'
                   '官網：https://telegram.org/\n'
                   '我的群組：http://bit.ly/2vI2jwg\n'
                   '==============================\n'
                   'PTT 表特 -近期大於 10 推的文章\n'
                   'PTT 廢文 -近期熱門廢文\n'
                   'PTT 台中\n'
                   'PTT 台南\n'
                   'PTT 高雄\n'
                   'PTT 日本\nPTT 笨版\n'
                   'PTT 西斯\n'
                   'PTT AV\n'
                   'PTT 工作\n'
                   'dcard 西斯\n'
                   '蘋果即時新聞\n'
                   '免費資源網路社群\n'
                   '就是教不落\n'
                   '電腦玩物\n'
                   '大樂透\n'
                   '威力彩\n'
                   '今彩539\n'
                   '3星彩\n'
                   '4星彩\n'
                   '100 USD -幣別轉換(數值 幣別英文)\n'
                   '下載工具'
                   )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if re.match(r'^\/move+', event.message.text):
        texent = mega.getdata("hdmove")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=texent))
        # for x,v in texent.items():
        # 	if x == "460153":
        # 		continue
        # 	context = "片名：" + v + "\n編號：" + x
        # 	line_bot_api.reply_message(
        # 		event.reply_token,
        # 		TextSendMessage(text=context))
        return 0

    if re.match(r'^\/jave+', event.message.text):
        texent = mega.getdata("jav")
        # print(texent)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=texent))
        return 0

    if re.match(r'^\/plot_all+', event.message.text):
        texent = mega.getdata("plot_all")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=texent))
        return 0

    if re.match(r'^\/thanks\s[0-9]+', event.message.text):
        tid = re.match(r'^\/thanks\s([0-9]+)', event.message.text).group(1)
        texent = mega.thanksUser(tid)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=texent))
        return 0

    if event.message.text == "抽":
        content = getGirlImages()
        SendImages(content, event)
        return 0


def SendImages(content, event):
    try:
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=content,
                preview_image_url=content
            ))
        pass
    except linebot.exceptions.LineBotApiError as e:
        print(e.status_code)
        print(e.error.message)
        print(e.error.details)


@app.route("/")
def get_index():
    return "Welcome！！"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print(body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


def ptt_beauty():
    rs = requests.session()
    res = rs.get('https://www.ptt.cc/bbs/Beauty/index.html', verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
    page_term = 2  # crawler count
    push_rate = 10  # 推文
    index_list = []
    article_list = []
    for page in range(start_page, start_page - page_term, -1):
        page_url = 'https://www.ptt.cc/bbs/Beauty/index{}.html'.format(page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)
        else:
            article_list = craw_page(res, push_rate)
    content = ''
    for article in article_list:
        data = '[{} push] {}\n{}\n\n'.format(article.get('rate', None), article.get('title', None),
                                             article.get('url', None))
        content += data
    return content


def ptt_hot():
    target_url = 'http://disp.cc/b/PttHot'
    print('Start parsing pttHot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('#list div.row2 div span.listTitle'):
        title = data.text
        link = "http://disp.cc/b/" + data.find('a')['href']
        if data.find('a')['href'] == "796-59l9":
            break
        content += '{}\n{}\n\n'.format(title, link)
    return content


def apple_news():
    target_url = 'http://www.appledaily.com.tw/realtimenews/section/new/'
    head = 'http://www.appledaily.com.tw'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 15:
            return content
        if head in data['href']:
            link = data['href']
        else:
            link = head + data['href']
        content += '{}\n\n'.format(link)
    return content


def getDcardPost(kanban, type="false"):
    _response = requests.get("https://www.dcard.tw/_api/forums/" + kanban + "/posts?popular=" + type)
    getData = _response.json()
    result = ''
    count = 0
    for x in getData:
        _id = str(x["id"])
        title = x["title"]
        url = "https://www.dcard.tw/f/" + kanban + "/p/" + _id
        result += title + "\n" + url + "\n"
        count = count + 1
        if count >= 10:
            return result
        pass
    return result


def get_xml_for_str(url):
    restr = ''
    # url = "http://feeds.feedburner.com/freegroup/"
    feeds = feedparser.parse(url)
    count = 0
    for data in feeds.entries:
        # print(data.title + ": " + data.link)
        restr += data.title + "\n" + data.link + "\n"
        count = count + 1
        if count >= 10:
            return restr
    return restr


def currency_chang(_m, _curry):
    m = float(_m)
    try:
        data = requests.get('https://tw.rter.info/capi.php')
        currency = data.json()
        mcapi = m / currency["USD" + _curry]["Exrate"]
        getTWD = mcapi * currency["USDTWD"]["Exrate"]
        return getTWD
        pass
    except Exception as e:
        return "靠邀！出錯了！"


def calculationNumber(x, y, z):
    result = {
        '+': float(x) + float(y),
        '-': float(x) - float(y),
        '*': float(x) * float(y),
        '/': float(x) / float(y)
    }[z]
    return result


def is_number(_num):
    try:
        float(_num)
        return True
        pass
    except Exception as e:
        return False
        raise e


def get_page_number(content):
    start_index = content.find('index')
    end_index = content.find('.html')
    page_number = content[start_index + 5: end_index]
    return int(page_number) + 1


def craw_page(res, push_rate):
    soup_ = BeautifulSoup(res.text, 'html.parser')
    article_seq = []
    for r_ent in soup_.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']
            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                rate = r_ent.find(class_="nrec").text
                url = 'https://www.ptt.cc' + link
                if rate:
                    rate = 100 if rate.startswith('爆') else rate
                    rate = -1 * int(rate[1]) if rate.startswith('X') else rate
                else:
                    rate = 0
                # 比對推文數
                if int(rate) >= push_rate:
                    article_seq.append({
                        'title': title,
                        'url': url,
                        'rate': rate,
                    })
        except Exception as e:
            # print('crawPage function error:',r_ent.find(class_="title").text.strip())
            print('本文已被刪除', e)
    return article_seq


def getGirlImages(_page=0):
    client = ImgurClient(imageconfig['client_id'], imageconfig['client_secret'], imageconfig['access_token'],
                         imageconfig['refresh_token'])
    albumslist = []
    list = client.get_account_albums(imageconfig['username'], _page)
    for albums in list:
        albumslist.append(albums.id)
    slice = random.sample(albumslist, 1)
    album_id = slice[0]
    images = client.get_album_images(album_id)
    try:
        index = random.randint(0, len(images) - 1)
    except:
        getGirlImages(1)
    url = images[index].link
    return str(url)


if __name__ == "__main__":
    # app.run()
    getGirlImages()