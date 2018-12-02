# multi threading ref
# https://www.tutorialspoint.com/python/python_multithreading.htm
# web driver download link
# https://sites.google.com/a/chromium.org/chromedriver/downloads
# phantomjs download link http://phantomjs.org/download.html
# crawl ref
# https://beomi.github.io/2017/02/27/HowToMakeWebCrawler-With-Selenium/

from selenium import webdriver
from bs4 import BeautifulSoup
import threading
import time
import Lib.queue as Queue

# input value
district_name = '신촌'
restaurant_list = ['타코로코', '라구식당', '공복', '한림돈가', '반서울', '완차이', '헌치브라운', '고타이','미스터서왕만두','방콕익스프레스','독수리다방','가야밀면신촌칼국수','소신이쏘','야바이','히노키공방','고냉지','고삼이','맘맘테이블']
restaurant_list = list(set(restaurant_list))

# output value
restaurant_info_list = []

# inner value
thread_cnt=len(restaurant_list)//5
start_time1 = time.time()
exitFlag = 0
workQueue = Queue.Queue(len(restaurant_list))
name_to_idx={}
threads = []
threadID = 0
threadList=[]
for i in range(thread_cnt):
    threadList.append("Thread-%d"%i)


class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        # phantomjs download link http://phantomjs.org/download.html
        self.driver = webdriver.PhantomJS('/Users/han/Desktop/phantomjs-2.1.1-windows/bin/phantomjs')
        # # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
        self.driver.implicitly_wait(1)
    def run(self):
        print("Starting " + self.name)
        process_data(self.driver,self.name,self.q)
        # self.driver.close()
        print("Exiting " + self.name)

def process_data(driver,name,q):
    while not exitFlag:
        # queueSema.acquire()
        if not workQueue.empty():
            data = q.get()
            idx=name_to_idx[data]

            start_time = time.time()
            try:
                # 네이버 지도이동
                driver.get('https://map.naver.com/')
                # 식당 이름 넣기
                driver.find_element_by_id('search-input').send_keys(district_name + ' ' + data)
                # 검색 버튼 누르기
                driver.find_element_by_xpath(
                    '//div[@id="wrap"]/div[@id="header"]/div[@class="sch"]/fieldset/button').click()
                # 상위 검색결과 누르기  panel_content
                driver.find_element_by_xpath(
                    '//div[@id="wrap"]/div[@id="container"]/div[@id="aside"]/div[@id="panel"]/div[@class="panel_content nano has-scrollbar"]/div[@class="scroll_pane content"]/div[@class="panel_content_flexible"]/div[@class="search_result"]/ul/li[@data-index="0"]/div[@class="lsnx"]/dl/dt/a').click()
                # 상위 검색결과 링크따기
                pathes = driver.find_element_by_xpath(
                    '//div[@id="wrap"]/div[@id="container"]/div[@id="aside"]/div[@id="panel"]/div[@class="panel_content nano has-scrollbar"]/div[@class="scroll_pane content"]/div[@class="panel_content_flexible"]/div[@class="search_result"]/ul/li[@data-index="0"]/div[@class="sc_act lsnx_act NCR-STOP"]/ul/li[@class="detail"]/a')
                # 하이퍼링크 복사후 이동
                driver.get(pathes.get_attribute('href'))
            except:
                print('%s %s page load error'%(name,data))
                workQueue.put(data)
                continue
                # queueSema.release()


            # 링크저장
            restaurant_info_list[idx]['link_str'] = driver.current_url
            # 페이지의 elements 모두 가져오기
            html = driver.page_source
            # BeautifulSoup parse
            soup = BeautifulSoup(html, 'html.parser')
            # 키워드 항목 분류
            theme_kwd_area = soup.select('div.theme_kwd_area >  ul.list_theme > li.list_item > strong.tit')
            kwd_category = []
            for n in theme_kwd_area:
                kwd_category.append(n.text.strip())
            # 항목별 키워드
            theme_kwd_area = soup.select('div.theme_kwd_area >  ul.list_theme > li.list_item > span')
            i = 0
            kwd_dict = {}
            for n in theme_kwd_area:
                kwd_dict[kwd_category[i]] = n.text.split(", ")
                i += 1
                restaurant_info_list[idx]['kwd_dict'] = kwd_dict
            # 연령별 퍼센트 10,20,30,40,50,60
            age_percent = []
            theme_kwd_area = soup.select('div.bar_chart >  ul.list_vertical_bar > li.list_item > span.bar > span ')
            for n in theme_kwd_area:
                age_percent.append(int(n.text.strip()[:2]))
                restaurant_info_list[idx]['age_percent_list'] = age_percent

            # 남여 비율
            theme_kwd_area = soup.select('g.c3-chart-arc > text[class]')
            gender_ratio = []
            for n in theme_kwd_area:
                gender_ratio.append(int(n.text.strip()))
                restaurant_info_list[idx]['gender_ratio_list'] = gender_ratio

            # 식당이름
            theme_kwd_area = soup.select('div.content > div.ct_box_area > div.biz_name_area > strong.name')
            for n in theme_kwd_area:
                restaurant_info_list[idx]['name_str'] = n.text.strip()

            # 식당 음식종류
            theme_kwd_area = soup.select('div.content > div.ct_box_area > div.biz_name_area > span.category')
            for n in theme_kwd_area:
                restaurant_info_list[idx]['category_list'] = n.text.strip().split(',')

            # 운영 시간 고쳐야됨
            theme_kwd_area = soup.select(
                'div.ct_box_area > div.bizinfo_area > div.list_bizinfo > div.list_item_biztime > div.txt > a.biztime_area > div > div.biztime')  # > span ')
            time_list = []
            for n in theme_kwd_area:
                time_list.append(n.text.strip())
                restaurant_info_list[idx]['time_list'] = time_list

            # '메뉴 가격'
            theme_kwd_area = soup.select(
                'div.ct_box_area > div.bizinfo_area > div.list_bizinfo > div.list_item_menu > div > ul.list_menu > li > div.list_menu_inner > em.price')
            menu_price_list = []
            for n in theme_kwd_area:
                price_range = n.text.strip().replace('원', '').replace(',', '').split('~')
                price_range = [int(price) for price in price_range]
                menu_price_list.append(price_range)
            try:
                restaurant_info_list[idx]['major_menu_price_int'] = menu_price_list[0][0]
            except:
                workQueue.put(data)
                print('%s %s major_menu_price_int error'%(name,data))

            # 메뉴이름
            theme_kwd_area = soup.select(
                'div.ct_box_area > div.bizinfo_area > div.list_bizinfo > div.list_item_menu > div > ul.list_menu > li > div.list_menu_inner > div.menu_area > div.menu > span.name')
            menu_price_dict = {}
            i = 0
            for n in theme_kwd_area:
                menu_price_dict[n.text.strip()] = menu_price_list[i]
                i += 1
            restaurant_info_list[idx]['menu_price_dict'] = menu_price_dict

            # queueSema.release()
            print("{} processed {} / {:2.2} seconds " .format(name, data,(time.time() - start_time)))
        else:
            print("%s is not processing %s" % (name, data))
            # time.sleep(0.5)
            # queueSema.release()
        # time.sleep(1)

# queueSema = threading.Semaphore(len(threadList))
i=0
for word in restaurant_list:
    workQueue.put(word)
    name_to_idx[word]=i
    i+=1
    restaurant_info_list.append({})
# Create new threads
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# Fill the queue
# queueSema.acquire()
# i=0
# for word in restaurant_list:
#     workQueue.put(word)
#     name_to_idx[word]=i
#     i+=1
#     restaurant_info_list.append({})
# queueSema.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()
print("Exiting Main Thread")
for rest in restaurant_info_list:
    print(rest)
print("total time--- %s seconds ---" % (time.time() - start_time1))
