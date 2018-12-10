### 추천버튼 눌렀을때 실행될 모듈 ###

import random

# filter option
# category  1:무관/2:한식/3:중식/4:일식/5:양식/6:기타
# price     1:무관/2:0-10000/3:10000-15000/4:15000-20000/5:20000-
# explore   0:기본점수낮게/1:기본점수높게
# distance  1:무관/2:5분이내/3:10분이내/4:15분이내/5:20분이내/6:25분이내


###################### input data type #######################################
#                                                                            #
# temp_candi : {'name':'식당이름'(string), distance':거리(int)} 의 리스트    #
# USER       : django 객체. user.UserInfo.age 이런식으로 내부값 호출         #
# user_filter: {'category':1,'price':1,'explore':1,'distance':1}             #
#                                                                            #
##############################################################################

def recommend(temp_candi,USER,user_filter):
    temp_candi2 = []
    candi = []

    # 후보군 생성
    for x in temp_candi:
        x['score'] = 0
        for y in db:
            if x['name'] == y:                                  
                x.update(db[y])
            
        if 'category' in x:                                     # db에 존재하지 않는 음식점이라면 후보에서 제외
            if user_filter['category'] == 1:                    # 카테고리로 1차 필터링
                temp_candi2.append(x)
            elif x['category'] == user_filter['category']:      
                temp_candi2.append(x)

            
    # 가격을 구간화
    for x in temp_candi2:
        if x['price'] < 0:          x['partial_price'] = -1     # 예외처리
        elif x['price'] < 10000:    x['partial_price'] = 1
        elif x['price'] < 15000:    x['partial_price'] = 2
        elif x['price'] < 20000:    x['partial_price'] = 3
        else:                       x['partial_price'] = 4

    # 거리도 구간화
        if x['distance'] < 180:     x['partial_distance'] = 2
        elif x['distance'] < 225:   x['partial_distance'] = 3
        elif x['distance'] < 270:   x['partial_distance'] = 4
        elif x['distance'] < 315:   x['partial_distance'] = 5
        elif x['distance'] < 400:   x['partial_distance'] = 6
        else:                       x['partial_distance'] = 1


    for x in temp_candi2:
        if user_filter['price'] == 1:                           # 가격대로 2차 필터링
            candi.append(x)
        elif x['partial_price'] == user_filter['price']:
            candi.append(x)

                 
    ##### 점수계산 #####

    # category '무관' 선택시 모든 후보군에 성향 수치만큼 가산점
    if user_filter['category'] == 1:
        for x in candi:
            if x['category'] == 1:
                x['score'] += USER.UserInfo.category1
            if x['category'] == 2:
                x['score'] += USER.UserInfo.category2
            if x['category'] == 3:
                x['score'] += USER.UserInfo.category3
            if x['category'] == 4:
                x['score'] += USER.UserInfo.category4
            if x['category'] == 5:
                x['score'] += USER.UserInfo.category5




    # price '무관' 선택시 모든 후보군에 성향 수치만큼 가산점
    if user_filter['price'] == 1:
        for x in candi:
            if x['partial_price'] == -1:
                x['score'] += 10
            if x['partial_price'] == 1:
                x['score'] += USER.UserInfo.price1
            if x['partial_price'] == 2:
                x['score'] += USER.UserInfo.price2
            if x['partial_price'] == 3:
                x['score'] += USER.UserInfo.price3
            if x['partial_price'] == 4:
                x['score'] += USER.UserInfo.price4
                

    # distance '무관' 선택시 모든 후보군에 성향 수치만큼 가산점
    if user_filter['distance'] == 1:
        for x in candi:
            if x['partial_distance'] == 1:
                x['score'] += USER.UserInfo.distance1
            if x['partial_distance'] == 2:
                x['score'] += USER.UserInfo.distance2
            if x['partial_distance'] == 3:
                x['score'] += USER.UserInfo.distance3
            if x['partial_distance'] == 4:
                x['score'] += USER.UserInfo.distance4
            if x['partial_distance'] == 5:
                x['score'] += USER.UserInfo.distance5

        
    # age 자신이 해당하는 나이대의 선호도/10을 점수로 얻음
    for x in candi:
        if x['age10'] < 0:      x['score'] += 5
        elif USER.UserInfo.age < 10:     continue
        elif USER.UserInfo.age < 20:     x['score'] += x['age10']/10
        elif USER.UserInfo.age < 30:     x['score'] += x['age20']/10
        elif USER.UserInfo.age < 40:     x['score'] += x['age30']/10
        elif USER.UserInfo.age < 50:     x['score'] += x['age40']/10
        elif USER.UserInfo.age < 60:     x['score'] += x['age50']/10


    # gender 0:남/1:여 선호비율/10의 점수를 얻음
    for x in candi:
        if USER.UserInfo.gender < 0:     x['score'] += 5
        elif USER.UserInfo.gender:       x['score'] += x['female']/10
        else:                           x['score'] += x['male']/10


    # rate 별점수치만큼 점수+
    for x in candi:
        if x['rating'] < 0:             x['score'] += 2.5
        else:                           x['score'] += x['rating']

    
    # explore = 0:기본점수낮게/1:기본점수높게
    # 최종점수를 바탕으로 식당별 hitrate를 계산
    total_score = 0

    if user_filter['explore'] == 0:
        for x in candi:
            total_score += x['score']
        for x in candi:
            x['hitrate'] = 70 * x['score']/total_score + 30/len(candi)
    elif user_filter['explore'] == 1:
        for x in candi:
            total_score += x['score']
        for x in candi:
            x['hitrate'] = 30 * x['score']/total_score + 70/len(candi)



    # hitrate를 바탕으로 랜덤하게 식당을 선택
    total_hitrate = 0
    random_num = random.random() * 100
    
    for x in candi:
        total_hitrate += x['hitrate']
        if total_hitrate > random_num:
            return x['name']
        
# output : 랜덤하게 선택된 한개의 식당이름(string)
