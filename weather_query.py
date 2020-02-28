import requests
import time

from bs4 import BeautifulSoup
from wxpy import *


bot = Bot()   # 初始化微信类
sentTo = bot.friends().search('好友名称')[0]    # 选择群组作为消息接收对象


def weatherQuery():
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
	content = requests.get("http://forecast.weather.com.cn/town/weather1dn/101210504006.shtml", headers=headers)	# 中国天气网
	content.encoding = content.apparent_encoding	# 编码
	soup = BeautifulSoup(content.text, "html.parser")    # 解析网页

	"""获取天气信息"""
	address = soup.find("div", "selectCity").text
	temp = soup.find("div", "tempDiv").text.replace("\n", "")
	weather = soup.find("div", "weather dis").text
	wind = soup.find("div", "todayLeft").find_all("p")[0].text.replace(" ", ":")
	humidity = soup.find("div", "todayLeft").find_all("p")[1].text.replace(" ", ":")
	timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	sentTo.send("{}  {}  {}  {}  {}  {}".format(timeNow, address, temp, weather, wind, humidity))

	"""写入天气查询日志"""
	with open(r"C:\Users\Administrator\Desktop\天气查询日志.txt", "a+") as f:
	    f.write("{}  {}  {}  {}  {}  {}".format(timeNow, address, temp, weather, wind, humidity))
	    f.write("\n")

	print("{}  {}  {}  {}  {}  {}".format(timeNow, address, temp, weather, wind, humidity))
	print("查询结束并生成日志，已发送至微信\n")
	print("下次查询时间,{0}小时后".format(round(second/3600)))


if __name__ == '__main__':
	print("天气查询计划已开始，将在整点为你通知...\n")
	while True:
		queryTime = time.ctime()
		queryTimeMinite = queryTime.split(" ")[3].split(":")[1:]
		second = 3590   # 查询间隔时间
		if queryTimeMinite == ["00", "00"]:
			queryTimeHour = int(queryTime.split(" ")[3].split(":")[0])
			if 18<=queryTimeHour<24 or 00<queryTimeHour<9:    # 晚上6点至第二天9点之间，每5小时查询一次，其他时间1小时查询一次
				second = 17990
				weatherQuery()
				time.sleep(second)
			else:
				weatherQuery()
				time.sleep(second)
		else:
			continue
