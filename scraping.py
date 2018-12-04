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
import sys


def each_page(id):

    URL = 'https://play.google.com/store/apps/details?id=' + id
    HTML = requests.get(url = URL)
    soup = BeautifulSoup(HTML.text, "lxml")
    '''
    with open(html_save + 'body.html', mode='w', encoding = 'utf-8') as f:
        f.write(soup.prettify())
    '''
    #category
    page_category = soup.find('meta', itemprop= 'applicationCategory')
    category = page_category.get('content')

    #真のweb url
    ss = soup.find('a', string = 'Visit website')
    if ss != None:
        web_url = ss.get('href')

    if ss == None:
        web_url = None

    #print('url=', web_url)
    #住所
    page_website = soup.find('div', class_='xyOfqd')
    page_weball = page_website.findAll('div')
    weball_size = len(page_weball)
    page_address = page_weball[weball_size -1]
    #print(page_address)
    address_navi = page_address.string
    address_unicode = str(address_navi)
    address_unicode = address_unicode.split()
    address = address_unicode[0]
    for i in range(1,len(address_unicode)):
        address += ' ' + address_unicode[i]
    print('address',type(address))
    #ddd = ddd.astype(str)
    #dds = address.shape[0]
    #print(dds)
    #print('len==',ddd[0][0])
    #print('address ==',address)

    #連絡先
    page_mail = soup.find('a', class_ = 'hrTbp KyaTEc')
    mail = page_mail.get('href')
    mail_size = len(mail)
    mail = mail[7:mail_size]
    #print('mail =', mail)

    return category, web_url, mail, address


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
    tex = each_page('com.supercell.brawlstars')
    c = 0
    #data = np.loadtxt("data.csv",delimiter=",", dtype='str')
    #print(data)
    data = np.empty((0,7), str)
    for count in page_r:
        list = np.array([])
        #id
        id = count.get('data-docid')
        #title
        page_title = count.find('img')
        title = page_title.get('alt')
        #company
        page_company = count.find('a', class_='subtitle')
        company = page_company.get('title')
        #each page
        print(id)
        category, web_url, mail, address = each_page(id)
        print(c)
        print('title =', title)
        print('id = ',id)
        print('company =',company)
        print('category=',category)
        print('web_url =',web_url)
        print('mail =',mail)
        print('address =',address)
        list = np.append(list,[title, id, company, category, web_url, mail, address])
        data = np.append(data, np.array([list]),axis = 0)
        c += 1
        sleep(2)
    np.savetxt('data.csv', data,fmt='%s', delimiter=',')

page_collect()
