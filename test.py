import requests
import re
import random
from bs4 import BeautifulSoup
import feedparser

from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage

line_bot_api = LineBotApi('f5MPBMEvI7tMuBxVnKkb2kcvS8KdDGNoMhJqKkArhOxzSr3mSbs8Osw6GL/9iJL9phoUf9qzSCV30W4hrgjxbbMuSsBzvWEukfMzI8YQ9q+z1CM8Rdq2WuOfueDXllSVazWsW5QBMZ3RnombK7QrMAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('241c6fbaecef54029cea60d45d7da972')

def run():
	image_message = ImageSendMessage(
		original_content_url='https://example.com/original.jpg',
		preview_image_url='https://example.com/preview.jpg'
	)
	line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=image_message))
	pass

if __name__ == "__main__":
	run()