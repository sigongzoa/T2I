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



def crawl(district_name, restaurant_list,see_status=False,  thread_cnt=1,   minimum_time_limit=3):
    '''
    :param district_name:           string              / district name
    :param restaurant_list:         list[string]        /  restaurant name string list
    :param see_status:              bool                / true:   see seconds ,   false:  don't   see
    :param thread_cnt:              int                 /  기본 스레드 갯수 1
    :param minimum_time_limit:      int                 /  최소 벤 피하기 시간 3초
    :return: restaurant_info_list   list[dictionary]    / restaurant dictionary list
        'name_str'              :   string          /   상호명
        'kwd_dict'              :   dictionary      /   해시태그
            ex)     'kwd_dict': {'분위기': ['이국적', '아기자기'], '인기토픽': ['치킨'], '찾는목적': ['숨은맛집']}
        'age_percent_list'      :   list[int(6)]    /   10,20,30,40,50,60대 퍼센트
        'prime_menu'            :   list[string]    /   음식 장르, 주력 음식
        'phone'                 :   string          /   전번
        'time_list'             :   list[string]    /   운영시간 정보
        'major_menu_price_int'  :   int             /   주메뉴 가격
        'menu_price_dict'       :   dictionary      /   {메뉴(string): 가격(int)}        
        'category'              :   string          /   음식점 종류   ex) korean, western, japan, etc
    '''
    # output value
    restaurant_info_list = []

    # inner value
    restaurant_list = list(set(restaurant_list))
    restaurant_noinfo_set = set()
    # thread_cnt=len(restaurant_list)//5
    start_time1 = time.time()
    exitFlag = 0
    workQueue = Queue.Queue(len(restaurant_list))
    name_to_idx={}
    threads = []
    threadID = 0
    threadList=[]
    for i in range(thread_cnt):
        threadList.append("Thread-%d"%i)
    korean=['만두','칼국수','쭈꾸미','족발','보쌈''육류','돼지고기구이','소고기구이','갈비탕','백반','한식','죽','고기요리','닭발','국밥','두부요리','곰탕','설렁탕','닭갈비','국수','향토','찜닭','곱창','막창','낙지요리']

    western=['스테이크','그리스','터키','립','양식','스파게티','파스타','프랑스','멕시코','남미','이탈리아','스페인','햄버거']

    japan=['라면','일본','우동','소바','일식','돈가스','라면','초밥','롤','카레','샤브샤브','덮밥','오니기리']


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
            if (see_status):
                print("Starting " + self.name)
            process_data(self.driver,self.name,self.q)
            if (see_status):
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
                    if(see_status):
                        print('%s %s page load error'%(name,data))
                    workQueue.put(data)
                    continue
                    # queueSema.release()
                # 페이지의 elements 모두 가져오기
                html = driver.page_source

                # BeautifulSoup parse
                soup = BeautifulSoup(html, 'html.parser')

                # 링크저장
                # restaurant_info_list[idx]['link_str'] = driver.current_url

                # 식당이름
                theme_kwd_area = soup.select('div.content > div.ct_box_area > div.biz_name_area > strong.name')
                for n in theme_kwd_area:
                    restaurant_info_list[idx]['name_str'] = n.text.strip()

                # page load check 1번더 기회줌
                if 'name_str' not in restaurant_info_list[idx]:
                    if (see_status):
                        print('%s %s soup error' % (name, data))
                    if data not in restaurant_noinfo_set:
                        restaurant_noinfo_set.add(data)
                        workQueue.put(data)
                        continue

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

                # 식당 음식종류
                theme_kwd_area = soup.select('div.content > div.ct_box_area > div.biz_name_area > span.category')
                for n in theme_kwd_area:
                    restaurant_info_list[idx]['prime_menu'] = n.text.strip().split(',')
                
                # 식당종류 분류
                if 'prime_menu' in restaurant_info_list[idx]:
                    genre='etc'
                    for genre in restaurant_info_list[idx]['prime_menu']:
                        if genre in korean:
                            genre='korean'
                            break
                        elif genre in western:                            
                            genre='western'
                            break
                        elif genre in japan:                            
                            genre='japan'
                            break
                    restaurant_info_list[idx]['category']=genre
                    
                # 전화번호
                theme_kwd_area = soup.select('#content > div.ct_box_area > div.bizinfo_area > div.list_bizinfo > div.list_item.list_item_biztel > div')
                for n in theme_kwd_area:
                    restaurant_info_list[idx]['phone'] = n.text.strip()

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
                if theme_kwd_area:
                    menu_price_list = []
                    for n in theme_kwd_area:
                        price_range = n.text.strip().replace('원', '').replace(',', '').split('~')
                        price_range = [int(price) for price in price_range]
                        menu_price_list.append(price_range)
                    restaurant_info_list[idx]['major_menu_price_int'] = menu_price_list[0][0]


                    # 메뉴이름
                    theme_kwd_area = soup.select(
                        'div.ct_box_area > div.bizinfo_area > div.list_bizinfo > div.list_item_menu > div > ul.list_menu > li > div.list_menu_inner > div.menu_area > div.menu > span.name')
                    menu_price_dict = {}
                    i = 0
                    for n in theme_kwd_area:
                        menu_price_dict[n.text.strip()] = menu_price_list[i][0]
                        i += 1
                    restaurant_info_list[idx]['menu_price_dict'] = menu_price_dict

                print("{} processed {:10} / {:2.2} seconds " .format(name, data,(time.time() - start_time)))
                if(float(time.time() - start_time)<minimum_time_limit):
                    if(see_status):
                        print('sleep {:2.2} sec'.format(minimum_time_limit-float(time.time() - start_time)))
                    time.sleep(minimum_time_limit-float(time.time() - start_time))
            else:
                if (see_status):
                    print("%s is not processing " % (name))
                # time.sleep(0.5)
            # time.sleep(1)

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

    # Wait for queue to empty
    while not workQueue.empty():
        pass

    # Notify threads it's time to exit
    exitFlag = 1

    # Wait for all threads to complete
    for t in threads:
        t.join()

    if (see_status):
        print("Exiting Main Thread")
        print("total time   --- {:2.2} seconds ---".format(time.time() - start_time1))

    # 빈사전 삭제
    restaurant_info_list = list(filter(None, restaurant_info_list))

    return restaurant_info_list

if __name__ == "__main__":
    # input value
    district_name = '신촌'
    restaurant_list = ['타코로코','맘맘테이블' ,'라구식당', '공복', '한림돈가', '반서울', '완차이', '헌치브라운', '고타이','미스터서왕만두','방콕익스프레스','독수리다방','가야밀면신촌칼국수','소신이쏘','야바이','히노키공방','고냉지','고삼이','맘맘테이블']

    restaurant_info_list=crawl(district_name,restaurant_list,see_status=True)

    for rest in restaurant_info_list:
        print(rest)
