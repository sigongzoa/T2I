import json
def save_json_dict(file_name,crawl_list,save_keys,is_initial=False):
    '''
    파일에 크롤링한 데이터를 키리스트에 해당하는 것만 저장(True)/업뎃(False)
    :param file_name:   string              file name with extension
    :param crawl_list:  list[dictionary]    data from crawling
    :param save_keys:   list[string]        selected keys from dictionary
    :param is_initial:  boolean             true if first else false
    :return:
    '''
    if is_initial:
        with open(file_name, "w") as fp:
            json_dict = {}
            # json dictionary convert
            for dic in crawl_list:
                val = {}
                for key, value in dic.items():
                    if key in save_keys:
                        val[key] = value
                json_dict[dic['input_name']] = val
            # save
            json.dump(json_dict, fp, sort_keys=True, indent=4)
    else:
        with open(file_name, "r+") as fp:
            # load dictionary
            json_dict = json.load(fp)
            # json dictionary convert
            for dic in crawl_list:
                val = {}
                for key, value in dic.items():
                    if key in save_keys:
                        val[key] = value
                json_dict[dic['input_name']] = val
            # save
            json.dump(json_dict, fp, sort_keys=True, indent=4)

def get_dict(file_name,rest_name):
    '''
    파일에서 식당 이름에 해당하는 사전 하나 반환(없으면 None 반환)
    :param file_name:   string          file name with extension
    :param rest_name:   string          restaurant name
    :return:            dictionary      one dictionary from file
    '''
    with open(file_name) as json_file:
        data = json.load(json_file)
        if data.get(rest_name,False):
            # print(data[rest_name])
            # for k in keys:
            #     print(k,',',data[rest_name].get(k,False))
            return data[rest_name]
        else:
            print("{:10} isn't stored in {}".format(rest_name,file_name))
            return None
def update_dict(file_name,rest_name,keys,values):
    '''
    파일에서 식당에 해당하는(식당없으면 생성) 사전의 키와 값 변경(키 없으면 생성)
    :param file_name:
    :param rest_name:
    :param keys:
    :param values:
    :return:
    '''
    with open(file_name, "r+") as fp:
        data = json.load(fp)
        for key, value in list(zip(keys, values)):
            print(key,value)
            data[rest_name][key] = value
        fp.seek(0)  # rewind
        json.dump(data, fp, sort_keys=True, indent=4)
        fp.truncate()
def delete_dict(file_name,rest_name):
    '''
    파일에서 해당 식당이름 데이터 삭제
    :param file_name:
    :param rest_name:
    :return:
    '''
    with open(file_name, "r+") as fp:
        data = json.load(fp)
        data.pop(rest_name)
        fp.seek(0)  # rewind
        json.dump(data, fp, sort_keys=True, indent=4)
        fp.truncate()
# {'page_name': '라구식당', 'kwd_dict': {'분위기': ['따뜻한느낌', '빈티지한', '분위기있는', '분위기좋은', '이국적'], '인기토픽': ['라자냐', '레스토랑', '가정식', '파스타', '심야식당'], '찾는목적': ['재방문', '데이트', '숨겨진맛집', '전통적인', '숨어있는']}, 'age_percent_list': [29, 87, 68, 42, 31, 26], 'gender_ratio_list': [51, 49], 'prime_menu': ['스파게티', '파스타전문'], 'category': 'western', 'phone': '02-364-2224', 'time_list': ['토요일 11:30 - 22:003~4시 브레이크타임', '일요일 휴무', '매일 11:30 - 22:003~5시 브레이크타임'], 'major_menu_price_int': 13000, 'menu_price_dict': {'라구파스타': 13000, '라자냐': 14000}, 'input_name': '라구식당', 'rating': 4.4}
# {'page_name': '미스터서왕만두 이대점', 'kwd_dict': {'분위기': ['친절하고', '재미있는', '개성있는'], '인기토픽': ['짬뽕', '군만두', '해물탕', '딤섬', '새우만두'], '찾는목적': ['깔끔한내부', '착한가격', '데이트', '재방문']}, 'age_percent_list': [23, 70, 39, 80, 36, 27], 'gender_ratio_list': [55, 45], 'prime_menu': ['만두'], 'category': 'korean', 'phone': '02-312-8869', 'major_menu_price_int': 5000, 'menu_price_dict': {'소룡포': 5000, '찐만두': 5000, '군만두': 5000}, 'input_name': '미스터서왕만두', 'rating': 4.4}
# {'page_name': '방콕익스프레스 신촌본점', 'kwd_dict': {'분위기': ['분위기좋은', '아담한', '이국적', '깔끔한인테리어', '모던한'], '인기토픽': ['치킨', '카레', '팟타이', '태국음식', '쌀국수'], '찾는목적': ['숨은맛집', '오픈키친', '착한가격', '데이트', '재방문']}, 'age_percent_list': [75, 94, 54, 57, 40, 27], 'gender_ratio_list': [55, 45], 'prime_menu': ['태국음식'], 'category': 'etc', 'phone': '02-6401-7793', 'major_menu_price_int': 13500, 'menu_price_dict': {'뿌팟퐁커리': 13500, '치킨그린커리': 8500, '원 팟카오무쌈': 9000, '얌운센샐러드': 8000, '새우팟타이': 7500}, 'input_name': '방콕익스프레스', 'rating': 4.4}
# {'page_name': '완차이', 'kwd_dict': {'인기토픽': ['짬뽕', '쟁반짜장', '중국집', '탕수육', '간짜장'], '찾는목적': ['데이트', '코스요리', '숨어있는']}, 'age_percent_list': [36, 90, 86, 70, 53, 45], 'gender_ratio_list': [46, 54], 'prime_menu': ['중식당'], 'category': 'etc', 'phone': '02-392-0302', 'major_menu_price_int': 23000, 'menu_price_dict': {'매운 홍합': 23000, '짜장면': 5000, '짬뽕': 6000}, 'input_name': '완차이', 'rating': 4.5}
# {'page_name': '헌치브라운', 'kwd_dict': {'분위기': ['분위기좋은'], '인기토픽': ['카페', '초콜릿', '디저트', '케이크', '생초콜릿']}, 'age_percent_list': [63, 97, 62, 45, 39, 25], 'gender_ratio_list': [57, 43], 'prime_menu': ['카페'], 'category': 'etc', 'phone': '02-711-2728', 'major_menu_price_int': 4500, 'menu_price_dict': {'아메리카노': 4500, '카페라떼': 5000, '바닐라라떼': 5500, '카라멜마끼아또': 6000, '카푸치노': 5500}, 'input_name': '헌치브라운', 'rating': 4.5}
# {'page_name': '연남서식당', 'kwd_dict': {'분위기': ['독특한분위기', '빈티지한', '고급진', '재미있는', '신비로운'], '인기토픽': ['소갈비', '양념갈비', '고기집', '돼지갈비', '갈비집'], '찾는목적': ['나들이', '신선한', '데이트', '자극적인', '재방문']}, 'age_percent_list': [6, 37, 39, 51, 77, 62], 'gender_ratio_list': [43, 57], 'prime_menu': ['육류', '고기요리'], 'category': 'korean', 'phone': '02-716-2520', 'major_menu_price_int': 15000, 'menu_price_dict': {'소 갈비 1대(150g)': 15000}, 'input_name': '연남서식당', 'rating': 3.9}
# {'page_name': '소신이쏘', 'kwd_dict': {'분위기': ['친절함', '친절한', '근사한', '친절하고', '친절해서'], '인기토픽': ['소갈비', '주먹밥', '갈비찜', '소갈비찜', '매운갈비'], '찾는목적': ['나들이', '재방문', '데이트', '새로오픈한', '점심특선']}, 'age_percent_list': [26, 86, 68, 41, 35, 40], 'gender_ratio_list': [50, 50], 'prime_menu': ['육류', '고기요리'], 'category': 'korean', 'phone': '02-324-3245', 'major_menu_price_int': 13500, 'menu_price_dict': {'매운소갈비찜 1인분': 13500, '크림소갈비찜 1인분': 14000, '평일점심 매운소갈비찜': 8500}, 'input_name': '소신이쏘', 'rating': 4.3}
# {'page_name': '히노키공방', 'kwd_dict': {'분위기': ['아담한', '친절하고'], '인기토픽': ['튀김', '일식', '생선구이', '아나고', '일본가정식'], '찾는목적': ['숨은', '재방문', '데이트', '자극적인']}, 'age_percent_list': [54, 91, 68, 51, 44, 38], 'gender_ratio_list': [51, 49], 'prime_menu': ['일식당'], 'category': 'etc', 'phone': '02-3143-2979', 'time_list': ['일요일 휴무일요일, 월요일 휴무', '매일 12:00 - 20:00재료소진시 영업종료, 시간관계없음', '매일 14:00 - 17:00브레이크타임, 재료소진시 영업종료', '월요일 휴무일요일, 월요일 휴무'], 'major_menu_price_int': 7500, 'menu_price_dict': {'가츠나베': 7500, '김치가츠나베': 8000, '새우텐동': 9000, '규야사이 무시야끼정식': 9500, '생선구이정식': 12000}, 'input_name': '히노키공방', 'rating': 4.3}
# {'page_name': '야바이', 'kwd_dict': {'분위기': ['친절하고', '재미있는', '분위기좋은', '친절한', '화려한'], '인기토픽': ['이자카야', '술집', '철판요리', '생맥주', '일식집'], '찾는목적': ['싱싱한', '비오는날', '데이트', '신선한', '나들이']}, 'age_percent_list': [26, 91, 69, 56, 42, 37], 'gender_ratio_list': [49, 51], 'prime_menu': ['일식당'], 'category': 'etc', 'phone': '070-8875-1024', 'time_list': ['토요일 16:00 - 01:00연중무휴', '매일 16:00 - 24:00연중무휴', '금요일 16:00 - 01:00연중무휴'], 'major_menu_price_int': 9000, 'menu_price_dict': {'오코노미야키': 9000, '몬자야키': 11000, '야끼소바': 10000}, 'input_name': '야바이', 'rating': 4.3}
# {'page_name': '반서울', 'age_percent_list': [47, 94, 57, 61, 54, 38], 'gender_ratio_list': [61, 39], 'prime_menu': ['퓨전음식'], 'category': 'etc', 'phone': '070-8882-0110', 'major_menu_price_int': 14000, 'menu_price_dict': {'파스타류': 14000, '밥류': 13000}, 'input_name': '반서울', 'rating': 4.5}
# {'page_name': '한림돈가신촌점', 'kwd_dict': {'분위기': ['느낌있는', '고급진', '분위기좋은', '모던한', '세련된'], '인기토픽': ['비빔국수', '명이나물', '갈치', '고기집', '삼겹살'], '찾는목적': ['나들이', '재방문', '데이트', '비오는날']}, 'age_percent_list': [46, 95, 67, 54, 46, 47], 'gender_ratio_list': [47, 53], 'prime_menu': ['돼지고기구이'], 'category': 'korean', 'phone': '02-338-6604', 'time_list': ['토요일 17:00 - 01:00명절 휴무', '일요일 휴무', '평일 17:00 - 01:00'], 'major_menu_price_int': 14000, 'menu_price_dict': {'삼겹살 / 알목살': 14000, '양념살': 14000}, 'input_name': '한림돈가', 'rating': 4.5}
# {'page_name': '충화반점', 'age_percent_list': [38, 87, 89, 86, 74, 72], 'gender_ratio_list': [48, 52], 'prime_menu': ['중식당'], 'category': 'etc', 'phone': '070-4100-6221', 'major_menu_price_int': 8900, 'menu_price_dict': {'라구짜장': 8900, '충화짬뽕': 8900, '고기 덴뿌라': 7900}, 'input_name': '충화반점', 'rating': 3.6}

data=[
{'page_name': '라구식당', 'kwd_dict': {'분위기': ['따뜻한느낌', '빈티지한', '분위기있는', '분위기좋은', '이국적'], '인기토픽': ['라자냐', '레스토랑', '가정식', '파스타', '심야식당'], '찾는목적': ['재방문', '데이트', '숨겨진맛집', '전통적인', '숨어있는']}, 'age_percent_list': [29, 87, 68, 42, 31, 26], 'gender_ratio_list': [51, 49], 'prime_menu': ['스파게티', '파스타전문'], 'category': 'western', 'phone': '02-364-2224', 'time_list': ['토요일 11:30 - 22:003~4시 브레이크타임', '일요일 휴무', '매일 11:30 - 22:003~5시 브레이크타임'], 'major_menu_price_int': 13000, 'menu_price_dict': {'라구파스타': 13000, '라자냐': 14000}, 'input_name': '라구식당', 'rating': 4.4},
{'page_name': '미스터서왕만두 이대점', 'kwd_dict': {'분위기': ['친절하고', '재미있는', '개성있는'], '인기토픽': ['짬뽕', '군만두', '해물탕', '딤섬', '새우만두'], '찾는목적': ['깔끔한내부', '착한가격', '데이트', '재방문']}, 'age_percent_list': [23, 70, 39, 80, 36, 27], 'gender_ratio_list': [55, 45], 'prime_menu': ['만두'], 'category': 'korean', 'phone': '02-312-8869', 'major_menu_price_int': 5000, 'menu_price_dict': {'소룡포': 5000, '찐만두': 5000, '군만두': 5000}, 'input_name': '미스터서왕만두', 'rating': 4.4},
{'page_name': '방콕익스프레스 신촌본점', 'kwd_dict': {'분위기': ['분위기좋은', '아담한', '이국적', '깔끔한인테리어', '모던한'], '인기토픽': ['치킨', '카레', '팟타이', '태국음식', '쌀국수'], '찾는목적': ['숨은맛집', '오픈키친', '착한가격', '데이트', '재방문']}, 'age_percent_list': [75, 94, 54, 57, 40, 27], 'gender_ratio_list': [55, 45], 'prime_menu': ['태국음식'], 'category': 'etc', 'phone': '02-6401-7793', 'major_menu_price_int': 13500, 'menu_price_dict': {'뿌팟퐁커리': 13500, '치킨그린커리': 8500, '원 팟카오무쌈': 9000, '얌운센샐러드': 8000, '새우팟타이': 7500}, 'input_name': '방콕익스프레스', 'rating': 4.4},
]
if __name__ == "__main__":
    crwal_data = [
        {'page_name': '라구식당',
         'kwd_dict': {'분위기': ['따뜻한느낌', '빈티지한', '분위기있는', '분위기좋은', '이국적'], '인기토픽': ['라자냐', '레스토랑', '가정식', '파스타', '심야식당'],
                      '찾는목적': ['재방문', '데이트', '숨겨진맛집', '전통적인', '숨어있는']}, 'age_percent_list': [29, 87, 68, 42, 31, 26],
         'gender_ratio_list': [51, 49], 'prime_menu': ['스파게티', '파스타전문'], 'category': 'western', 'phone': '02-364-2224',
         'time_list': ['토요일 11:30 - 22:003~4시 브레이크타임', '일요일 휴무', '매일 11:30 - 22:003~5시 브레이크타임'],
         'major_menu_price_int': 13000, 'menu_price_dict': {'라구파스타': 13000, '라자냐': 14000}, 'input_name': '라구식당',
         'rating': 4.4},
        {'page_name': '미스터서왕만두 이대점',
         'kwd_dict': {'분위기': ['친절하고', '재미있는', '개성있는'], '인기토픽': ['짬뽕', '군만두', '해물탕', '딤섬', '새우만두'],
                      '찾는목적': ['깔끔한내부', '착한가격', '데이트', '재방문']}, 'age_percent_list': [23, 70, 39, 80, 36, 27],
         'gender_ratio_list': [55, 45], 'prime_menu': ['만두'], 'category': 'korean', 'phone': '02-312-8869',
         'major_menu_price_int': 5000, 'menu_price_dict': {'소룡포': 5000, '찐만두': 5000, '군만두': 5000},
         'input_name': '미스터서왕만두', 'rating': 4.4},
        {'page_name': '방콕익스프레스 신촌본점',
         'kwd_dict': {'분위기': ['분위기좋은', '아담한', '이국적', '깔끔한인테리어', '모던한'], '인기토픽': ['치킨', '카레', '팟타이', '태국음식', '쌀국수'],
                      '찾는목적': ['숨은맛집', '오픈키친', '착한가격', '데이트', '재방문']}, 'age_percent_list': [75, 94, 54, 57, 40, 27],
         'gender_ratio_list': [55, 45], 'prime_menu': ['태국음식'], 'category': 'etc', 'phone': '02-6401-7793',
         'major_menu_price_int': 13500,
         'menu_price_dict': {'뿌팟퐁커리': 13500, '치킨그린커리': 8500, '원 팟카오무쌈': 9000, '얌운센샐러드': 8000, '새우팟타이': 7500},
         'input_name': '방콕익스프레스', 'rating': 4.4},
    ]
    name = '미스터서왕만두'
    Filename = 'ex.json'
    save_keys = ['kwd_dict', 'menu_price_dict', 'prime_menu', 'phone', ]

    # save craw data to json format
    save_json_dict(Filename,crwal_data,save_keys,True)

    # get one restaurant dictionary
    restinfo= get_dict(Filename,name)
    print(restinfo)

    # update
    update_dict(Filename,name,['key1','key2','key3'],['val1',1234,['val31','val32','val33']])
    # get one restaurant dictionary
    restinfo= get_dict(Filename,name)
    print(restinfo)

    # delete
    delete_dict(Filename,name)
    # get one restaurant dictionary
    restinfo = get_dict(Filename, name)
    print(restinfo)


