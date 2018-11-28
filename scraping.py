# coding: UTF-8
from selenium import webdriver
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import numpy as np
import os
from time import sleep
import lxml.html
from pyvirtualdisplay import Display


def each_page(id):
    URL = 'https://play.google.com/store/apps/details?id=' + id
    HTML = requests.get(url = URL)
    soup = BeautifulSoup(HTML.content, "html.parser")
    #category
    page_category = soup.find('meta', itemprop= 'applicationCategory')
    category = page_category.get('content')
    #website
    #page_website = soup.find('div', class_='xyOfqd')
    ss = soup.find(string = 'ウェブサイトにアクセス')
    print(soup)
    return ss


def page_collect():
    display = Display(visible=0, size=(800, 600))
    display.start()

    driver = webdriver.Firefox()
    #事前登録ベージ
    driver.get("https://play.google.com/store/apps/collection/promotion_3000000d51_pre_registration_games?clp=SjMKMQorcHJvbW90aW9uXzMwMDAwMDBkNTFfcHJlX3JlZ2lzdHJhdGlvbl9nYW1lcxAHGAM%3D:S:ANO1ljIAI4o&gsr=CjVKMwoxCitwcm9tb3Rpb25fMzAwMDAwMGQ1MV9wcmVfcmVnaXN0cmF0aW9uX2dhbWVzEAcYAw%3D%3D:S:ANO1ljKWIwM")


    # ページのHTMLを取得
    html = driver.page_source

    driver.close()
    display.stop()

    soup = BeautifulSoup(html, "html.parser")
    page_r = soup.findAll('div', class_='card-content id-track-click id-track-impression')

    c = 0
    for count in page_r:
        #id
        id = count.get('data-docid')
        #title
        page_title = count.find('img')
        title = page_title.get('alt')
        #company
        page_company = count.find('a', class_='subtitle')
        company = page_company.get('title')
        #each page
        tex = each_page(id)
        print(c)
        #print(title)
        #print(id)
        #print(company)
        #print(tex)
        c += 1
        sleep(2)

page_collect()
