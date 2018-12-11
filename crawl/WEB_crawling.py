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
# import Lib.queue as Queue
from queue  import Queue


def crawl(district_name, restaurant_list, phantom_path, see_status=False, thread_cnt=1, minimum_time_limit=3,minimum_time_limit2=3):
    '''
    :param district_name:           string              / district name
    :param restaurant_list:         list[string]        /  restaurant name string list
    :param phantom_path:            string              /  phantom js path
    :param see_status:              bool                / true:   see seconds ,   false:  don't   see
    :param thread_cnt:              int                 /  기본 스레드 갯수 1
    :param minimum_time_limit:      int                 /  네이버 최소 벤 피하기 시간 3초(실험완료)
    :param minimum_time_limit2:      int                /  망플 최소 벤 피하기 시간 3초(실험필요)
    :return: restaurant_noinfo_list list[string]        / restaurant which doesn't enough info
    :return: restaurant_info_list   list[dictionary]    / restaurant dictionary list
        'page_name'             :   string          /   상호명
        'input_name'            :   string          /   검색명
        'kwd_dict'              :   dictionary      /   해시태그
            ex)     'kwd_dict': {'분위기': ['이국적', '아기자기'], '인기토픽': ['치킨'], '찾는목적': ['숨은맛집']}
        'age_percent_list'      :   list[int(6)]    /   10,20,30,40,50,60대 퍼센트
        'prime_menu'            :   list[string]    /   음식 장르, 주력 음식
        'phone'                 :   string          /   전번
        'time_list'             :   list[string]    /   운영시간 정보
        'major_menu_price_int'  :   int             /   주메뉴 가격
        'menu_price_dict'       :   dictionary      /   {메뉴(string): 가격(int)}
        'category'              :   int             /   음식점 종류   ex) 한(1),중(2),일(3),양(4),외(5)
        'gender_ratio_list'     :   list[int(2)]    /   여,남 비율
        'rating'                :   float           /   별점 5점만점 (출처 망플)
    '''
    # output value
    restaurant_info_list = []
    restaurant_noinfo_list = set()

    # inner value
    restaurant_list = list(set(restaurant_list))
    last_chance_set = set()
    # thread_cnt=len(restaurant_list)//5
    start_time1 = time.time()
    exitFlag = 0
#     workQueue = Queue.Queue(len(restaurant_list))
    workQueue = Queue(len(restaurant_list))
    name_to_idx = {}
    threads = []
    threadID = 0
    threadList = []
    for i in range(thread_cnt):
        threadList.append("Thread-%d" % i)
    korean = ['만두', '칼국수', '쭈꾸미', '족발', '보쌈''육류', '돼지고기구이', '소고기구이', '갈비탕', '백반', '한식','한식당', '죽', '고기요리', '닭발', '국밥', '두부요리',
              '곰탕', '설렁탕', '닭갈비', '국수', '향토', '찜닭', '곱창', '막창', '낙지요리','분식']
    western = ['양식당','양식','스테이크', '그리스', '터키', '립', '양식', '스파게티', '파스타', '프랑스', '멕시코', '남미', '이탈리아', '스페인', '햄버거','핫도그']
    chinese = ['중식당','중식','양꼬치','짬뽕','짜장','탕수육','깐풍기','마라','북경',]
    japan = ['일식','일식집','일식당','라면', '일본', '우동', '소바', '일식', '돈가스', '라면', '초밥', '롤', '카레', '샤브샤브', '덮밥', '오니기리','이자카야']
    necessary_key=['age_percent_list','category','major_menu_price_int','gender_ratio_list','rating']

    class myThread(threading.Thread):
        def __init__(self, threadID, name, q):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.q = q
            # phantomjs download link http://phantomjs.org/download.html
            self.driver = webdriver.PhantomJS(phantom_path)
            # # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
            self.driver.implicitly_wait(3)

        def run(self):
            if (see_status):
                print("Starting " + self.name)
            process_data(self.driver, self.name, self.q)
            if (see_status):
                print("Exiting " + self.name)

    def process_data(driver, name, q):
        pretime=0
        while not exitFlag:
            if not workQueue.empty():
                data = q.get()
                idx = name_to_idx[data]
                start_time = time.time()

                # 네이버 크롤링
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
                    if (see_status):
                        print('%s %s page load step#1 error' % (name, data))
                    if data not in last_chance_set:
                        last_chance_set.add(data)
                        workQueue.put(data)
                        continue
                # 페이지의 elements 모두 가져오기
                html = driver.page_source

                # BeautifulSoup parse
                soup = BeautifulSoup(html, 'html.parser')

                # 링크저장
                # restaurant_info_list[idx]['link_str'] = driver.current_url

                # 식당이름
                theme_kwd_area = soup.select('div.content > div.ct_box_area > div.biz_name_area > strong.name')
                for n in theme_kwd_area:
                    restaurant_info_list[idx]['page_name'] = n.text.strip()

                # page load check 1번더 기회줌
                if 'page_name' not in restaurant_info_list[idx]:
                    if (see_status):
                        print('%s %s soup error' % (name, data))
                    if data not in last_chance_set:
                        last_chance_set.add(data)
                        workQueue.put(data)
                        continue
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
                    age_percent.append(int(float(n.text.strip()[:3])))
                    restaurant_info_list[idx]['age_percent_list'] = age_percent
                if 'age_percent_list' not in restaurant_info_list[idx]:
                    restaurant_info_list[idx]['age_percent_list']=[-1,-1,-1,-1,-1,-1]

                # 여남 비율
                theme_kwd_area = soup.select('g.c3-chart-arc > text[class]')
                gender_ratio = []
                for n in theme_kwd_area:
                    gender_ratio.append(int(n.text.strip()))
                    restaurant_info_list[idx]['gender_ratio_list'] = gender_ratio
                if 'gender_ratio_list' not in restaurant_info_list[idx]:
                    restaurant_info_list[idx]['gender_ratio_list']=[-1, -1]

                # 식당 음식종류
                theme_kwd_area = soup.select('div.content > div.ct_box_area > div.biz_name_area > span.category')
                for n in theme_kwd_area:
                    restaurant_info_list[idx]['prime_menu'] = n.text.strip().split(',')

                # 식당종류 분류
                if 'prime_menu' in restaurant_info_list[idx]:
                    genre = 5
                    for menu in restaurant_info_list[idx]['prime_menu']:
                        if menu in korean:
                            genre = 1
                            break
                        elif menu in western:
                            genre = 4
                            break
                        elif menu in japan:
                            genre = 3
                            break
                        elif menu in chinese:
                            genre = 2
                            break
                    restaurant_info_list[idx]['category'] = genre
                if 'category' not in restaurant_info_list[idx]:
                    restaurant_info_list[idx]['category']=-1

                # 전화번호
                theme_kwd_area = soup.select(
                    '#content > div.ct_box_area > div.bizinfo_area > div.list_bizinfo > div.list_item.list_item_biztel > div')
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
                        dummy=[]
                        for price in price_range:
                            try:
                                dummy.append(int(price))
                            except:
                                dummy.append(-1)
                        menu_price_list.append(dummy)
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
                if 'major_menu_price_int' not in restaurant_info_list[idx]:
                    restaurant_info_list[idx]['major_menu_price_int']=-1

                # 검색명
                restaurant_info_list[idx]['input_name'] = data

                # ban avoid
                if (float(time.time() - start_time) + pretime < minimum_time_limit2+0.1):
                    if (see_status):
                        print('ban avoid#2 sleep {:2.2} sec'.format(minimum_time_limit2 - float(time.time() - start_time)-pretime))
                    time.sleep(minimum_time_limit2 +0.1- float(time.time() - start_time)-pretime)
                midtime=time.time()
                
                # 망고플레이트 크롤링
                try:
                    # 망플
                    driver.get('https://www.mangoplate.com/')
                    # 식당 이름 넣기
                    driver.find_element_by_id("main-search").send_keys(district_name + ' ' + data)
                    # 검색 버튼 누르기
                    driver.find_element_by_xpath("/html/body/main/article/header/fieldset/input").click()
                except:
                    if (see_status):
                        print('%s %s page load step#2 error' % (name, data))
                    if data not in last_chance_set:
                        last_chance_set.add(data)
                        workQueue.put(data)
                        continue

                # 페이지의 elements 모두 가져오기
                html = driver.page_source
                # BeautifulSoup parse
                soup = BeautifulSoup(html, 'html.parser')

                # 별점
                elements = soup.select(
                    'body > main > article > div.column-wrapper > div > div > section > div.search-list-restaurants-inner-wrap > ul > li.list-restaurant.server_render_search_result_item > div > figure > figcaption > div > strong')
                for n in elements:
                    try:
                        restaurant_info_list[idx]['rating'] = float(n.text.strip())
                    except:
                        print('%s %s page rating convert %s error' % (name, data,n.text.strip()))
                if 'rating' not in restaurant_info_list[idx]:
                    restaurant_info_list[idx]['rating']=-1

                print("{} processed {:10} / {:2.2} seconds ".format(name, data, (time.time() - start_time)))
                # ban avoid
                if (float(time.time() - start_time) < minimum_time_limit):
                    if (see_status):
                        print('ban avoid#1 sleep {:2.2} sec'.format(minimum_time_limit - float(time.time() - start_time)))
                    time.sleep(minimum_time_limit - float(time.time() - start_time))
                pretime=float(time.time()-midtime)
            else:
                if (see_status):
                    print("%s is not processing " % (name))

    i = 0
    for word in restaurant_list:
        workQueue.put(word)
        name_to_idx[word] = i
        i += 1
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
    district_name = '신수동'
    restaurant_list = [ '을밀대 본점',
'연남서식당',
'조선초가한끼',
'아소정 공덕본점',
'옛맛서울불고기',
'역전회관',
'형제갈비',
'신촌서서갈비',
'꽃게랑새우랑',
'통큰갈비 신촌본점',
'이찌멘 신촌점',
'여우골',
'원마산아구찜 본관',
'참나무본가',
'생고기제작소 홍대점',
'락희옥 마포본점',
'가야밀면신촌칼국수',
'로운샤브샤브 신촌점',
'하누소 서강점',
'원조조박집 본관',
'군자네',
'램랜드',
'철길왕갈비살',
'신촌해물칼국수',
'죽해수산',
'온달만두분식',
'가야가야 이대점',
'순남시래기 서강대점',
'메이찬',
'미분당',
'부탄츄 신촌점',
'청담동포장마차',
'곰탕수육전문',
'유닭스토리 신촌점',
'미분당 신촌2호점',
'소신이쏘',
'매일스시횟집',
'끼로끼로부엉이 노고산점',
'홍대개미 신촌점',
'찜수성찬 신촌본점',
'이박사의신동막걸리',
'계고기집',
'쭈꾸미블루스 신촌본점',
'블랑코 마포점',
'발리비스트로',]
    phantom_path='/Users/han/Desktop/phantomjs-2.1.1-windows/bin/phantomjs'
    restaurant_info_list,restaurant_noinfo_list = crawl(district_name, restaurant_list,phantom_path, see_status=True)

    for rest in restaurant_info_list:
        print(rest)
    print('key 없는식당')
    for rest in restaurant_noinfo_list:
        print(rest)
