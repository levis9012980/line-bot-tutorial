import requests
import re
import json
from bs4 import BeautifulSoup

forum = {
	"hdmove" : "376",   # 高畫質電影區
	"jav" : "421",      # 日本有碼
	"plot_all" : "373"  # 連續劇(全集)
}
changtext = {
	"【" : "[",
	"】" : "]",
	"：" : ":",
	"/" : ".",
	"Ⅰ" : "I",
	"Ⅱ" : "II",
}
def main():
	# init()
	getdata("hdmove")
	pass

def init():
	global s
	params = {
		'fastloginfield': 'username',
		'username': '楓痕',
		'password': 'XmZ382!P3gX2',
		'cookietime': '2592000',
		'quickforward': 'yes',
		'handlekey': 'ls',
	}
	s = requests.Session()
	r = s.post("http://megafunpro.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1", data=params)

	pass

def getdata(_id):
	global s
	init()
	flag = False
	r = s.get("http://megafunpro.com/forum.php?mod=forumdisplay&fid="+str(forum[_id])+"&filter=author&orderby=dateline")
	HTML = BeautifulSoup(r.text,"html.parser")
	table = HTML.find('table', attrs={"summary": "forum_"+str(forum[_id])})
	param = dict()
	_result = ''
	for x in table.find_all('tbody'):
		try:
			id = x["id"]
			if id == "separatorline":
				flag = True
				continue
			if flag == True:
				text = x.find("a", class_="xst").getText()
				for x, v in changtext.items():
					text = re.sub(x, v, text)
				_tid = str(id).split("_")
				tid = _tid[1]
				param[tid] = text
				_result += "名稱：" + str(text) + "\n編號：" + str(tid) + "\n\n"
		except Exception as e:
			print("error=" + str(e))
			continue
	# print(_result)
	return _result

def thanksUser(tid):
	global s
	init()
	checktid = json.loads(querydata(tid))
	if checktid["file"] == True:
		return checktid["url"]
	try:
		reHTML = ''
		r = s.get("http://megafunpro.com/thread-"+str(tid)+"-1-1.html")
		HTML = BeautifulSoup(r.text, "html.parser")
		# print(HTML)
		title = HTML.find("meta",attrs={"name":"keywords"})["content"]
		imgtag = HTML.find_all("img",class_="zoom")
		findthanks = HTML.findChild("div", class_="showhide")
		if findthanks == None:
			HTML = thanksGO(tid)

		reHTML += "<h4>" + str(title) + "</h4>\n\n"
		for _img in imgtag:
			img = str(_img["src"]).replace("/get_image.php?url=", "")
			reHTML += "<img src='" + str(img) + "'>\n"
		showhide = HTML.find_all("div", class_="showhide")
		# showhidlen = len(showhide)  # 找到的數目
		for x in showhide:
			reHTML += str(x) + "\n"
		url = getfileurl(tid,title,reHTML)
		return url
	except:
		return "取得資料發生錯誤！\n快聯絡胖瞎輝"

def thanksGO(tid):
	global s
	r = s.get("http://megafunpro.com/plugin.php?id=thanksplugin:thanks&action=thanks&tid="+str(tid)+"&infloat=yes&handlekey=thankswin&inajax=1&ajaxtarget=fwin_content_thankswin")
	formhash = re.search(r'name\=\"formhash\" value\=\"(.+?)\"',r.text).group(1)
	post_safecode = re.search(r'name\=\"post_safecode\" value\=\"(.+?)\"',r.text).group(1)
	re_url = re.search(r'name\=\"re_url\" value\=\"(.+?)\"',r.text).group(1)
	params = {
		'tid': tid,
		'formhash': formhash,
		'post_safecode': post_safecode,
		're_url': re_url,
		'saying': '',
		'num': '3',
		'thanksubmit': 'true',
	}
	postr = s.post("http://megafunpro.com/plugin.php?id=thanksplugin:thanks&action=thanks",data=params)
	# time.sleep(5)
	return BeautifulSoup(postr.text, "html.parser")

def getfileurl(_tid,_title,_text):
	params = {
		'tid': str(_tid),
		'title': str(_title),
		'text': _text,
	}
	r = requests.post("http://file.imfzon.net/index.php",data=params)
	url = r.text
	return url

def querydata(_tid):
	params = {
		'tid': str(_tid),
	}
	r = requests.post("http://file.imfzon.net/query.php", data=params)
	res= r.text
	return res

if __name__ == '__main__':
	main()