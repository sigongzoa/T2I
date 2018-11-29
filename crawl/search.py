from selenium import webdriver

driver = webdriver.PhantomJS('/Users/Han/Desktop/phantomjs-2.1.1-windows/bin/phantomjs')
# 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
driver.implicitly_wait(5)

driver.get('https://map.naver.com/')
district_name='신촌'
restaurant_list=['한림돈가','타로로코','라구식당','공복']



# 식당 이름 넣기
driver.find_element_by_id('search-input').send_keys(search_name)
# 검색 버튼 누르기
driver.find_element_by_xpath('//div[@id="wrap"]/div[@id="header"]/div[@class="sch"]/fieldset/button').click()
# 상위 검색결과 누르기  panel_content
driver.find_element_by_xpath('//div[@id="wrap"]/div[@id="container"]/div[@id="aside"]/div[@id="panel"]/div[@class="panel_content nano has-scrollbar"]/div[@class="scroll_pane content"]/div[@class="panel_content_flexible"]/div[@class="search_result"]/ul/li[@data-index="0"]/div[@class="lsnx"]/dl/dt/a').click()
# 상위 검색결과 링크따기
pathes=driver.find_element_by_xpath('//div[@id="wrap"]/div[@id="container"]/div[@id="aside"]/div[@id="panel"]/div[@class="panel_content nano has-scrollbar"]/div[@class="scroll_pane content"]/div[@class="panel_content_flexible"]/div[@class="search_result"]/ul/li[@data-index="0"]/div[@class="sc_act lsnx_act NCR-STOP"]/ul/li[@class="detail"]/a')
# 하이퍼링크 복사후 이동
driver.get(pathes.get_attribute('href'))
print(driver.current_url)