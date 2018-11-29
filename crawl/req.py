from selenium import webdriver
import time
from bs4 import BeautifulSoup
# https://www.tutorialspoint.com/python/python_multithreading.htm
start_time1 = time.time()

driver = webdriver.PhantomJS('/Users/Han/Desktop/phantomjs-2.1.1-windows/bin/phantomjs')
# 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
driver.implicitly_wait(5)

district_name='신촌'
restaurant_list=['타코로코','라구식당','공복','한림돈가']
db_list=[]
restaurant_info_list=[]
print("driver loading--- %s seconds ---" % (time.time() - start_time1))
for name in restaurant_list:
    start_time = time.time()
    db_dict={}
    # 네이버 지도이동
    driver.get('https://map.naver.com/')
    # 식당 이름 넣기
    driver.find_element_by_id('search-input').send_keys(district_name+' '+name)
    # 검색 버튼 누르기
    driver.find_element_by_xpath('//div[@id="wrap"]/div[@id="header"]/div[@class="sch"]/fieldset/button').click()
    # 상위 검색결과 누르기  panel_content
    driver.find_element_by_xpath('//div[@id="wrap"]/div[@id="container"]/div[@id="aside"]/div[@id="panel"]/div[@class="panel_content nano has-scrollbar"]/div[@class="scroll_pane content"]/div[@class="panel_content_flexible"]/div[@class="search_result"]/ul/li[@data-index="0"]/div[@class="lsnx"]/dl/dt/a').click()
    # 상위 검색결과 링크따기
    pathes=driver.find_element_by_xpath('//div[@id="wrap"]/div[@id="container"]/div[@id="aside"]/div[@id="panel"]/div[@class="panel_content nano has-scrollbar"]/div[@class="scroll_pane content"]/div[@class="panel_content_flexible"]/div[@class="search_result"]/ul/li[@data-index="0"]/div[@class="sc_act lsnx_act NCR-STOP"]/ul/li[@class="detail"]/a')
    # 하이퍼링크 복사후 이동
    driver.get(pathes.get_attribute('href'))

    # 링크저장
    db_dict['link_str']=driver.current_url

    # 페이지의 elements모두 가져오기
    html = driver.page_source
    # BeautifulSoup parse
    soup = BeautifulSoup(html, 'html.parser')

    # 키워드 항목 분류
    theme_kwd_area = soup.select('div.theme_kwd_area >  ul.list_theme > li.list_item > strong.tit')
    kwd_category=[]
    for n in theme_kwd_area:
        kwd_category.append(n.text.strip())

    # 항목별 키워드
    theme_kwd_area = soup.select('div.theme_kwd_area >  ul.list_theme > li.list_item > span')
    i=0
    kwd_dict={}
    for n in theme_kwd_area:
        kwd_dict[kwd_category[i]]=n.text.split(", ")
        i+=1
    db_dict['kwd_dict']=kwd_dict

    # 연령별 퍼센트 10,20,30,40,50,60
    age_percent=[]
    theme_kwd_area = soup.select('div.bar_chart >  ul.list_vertical_bar > li.list_item > span.bar > span ')
    for n in theme_kwd_area:
        age_percent.append(int(n.text.strip()[:2]))
    db_dict['age_percent_list']=age_percent

    # 남여 비율
    theme_kwd_area = soup.select('g.c3-chart-arc > text[class]')
    gender_ratio=[]
    for n in theme_kwd_area:
        gender_ratio.append(int(n.text.strip()))
    db_dict['gender_ratio_list'] = gender_ratio

    # 식당이름
    theme_kwd_area = soup.select('div.content > div.ct_box_area > div.biz_name_area > strong.name')
    for n in theme_kwd_area:
        db_dict['name_str'] = n.text.strip()

    # 식당 음식종류
    theme_kwd_area = soup.select('div.content > div.ct_box_area > div.biz_name_area > span.category')
    for n in theme_kwd_area:
        db_dict['category_list'] =n.text.strip().split(',')

    # 운영 시간 고쳐야됨
    theme_kwd_area = soup.select('div.ct_box_area > div.bizinfo_area > div.list_bizinfo > div.list_item_biztime > div.txt > a.biztime_area > div > div.biztime')# > span ')
    time_list=[]
    for n in theme_kwd_area:
        time_list.append(n.text.strip())
    db_dict['time_list']=time_list

    # '메뉴 가격'
    theme_kwd_area = soup.select('div.ct_box_area > div.bizinfo_area > div.list_bizinfo > div.list_item_menu > div > ul.list_menu > li > div.list_menu_inner > em.price')
    menu_price_list=[]
    for n in theme_kwd_area:
        price_range=n.text.strip().replace('원','').replace(',','').split('~')
        price_range=[int(price) for price in price_range]
        menu_price_list.append(price_range)
    db_dict['major_menu_price_int'] = menu_price_list[0][0]

    # 메뉴이름
    theme_kwd_area = soup.select('div.ct_box_area > div.bizinfo_area > div.list_bizinfo > div.list_item_menu > div > ul.list_menu > li > div.list_menu_inner > div.menu_area > div.menu > span.name')
    menu_price_dict={}
    i=0
    for n in theme_kwd_area:
        menu_price_dict[n.text.strip()]=menu_price_list[i]
        i+=1
    db_dict['menu_price_dict']=menu_price_dict
    restaurant_info_list.append(db_dict)
    print("--- %s seconds ---" % (time.time() - start_time))
for dic in restaurant_info_list:
    print(dic)
print("driver loading--- %s seconds ---" % (time.time() - start_time1))