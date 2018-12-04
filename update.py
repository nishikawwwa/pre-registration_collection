#coding:UTF-8
import schedule
import time
import scraping

def job():
    #ここにメインの処理を書く
    print("時間ですよ～")


def db_update():
    scraping.page_collect()



#AM10:30にjobを実行
schedule.every().day.at("10:30").do(db_update)

while True:
    schedule.run_pending()
    time.sleep(1)
