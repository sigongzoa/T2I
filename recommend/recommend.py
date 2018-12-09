### 추천버튼 눌렀을때 실행될 모듈 ###

import random

# 임의로 만든데이터들
db = {'김가네 서강대점':{'category':3,'price':35000,'age10':30,'age20':80,'age30':60,'age40':20,'age50':10,'male':55,'female':45,'rating':4.0},
      '태양':{'category':2,'price':6000,'age10':60,'age20':75,'age30':50,'age40':40,'age50':20,'male':65,'female':35,'rating':2.0},
      '순이네칼국수':{'category':2,'price':12000,'age10':30,'age20':40,'age30':40,'age40':80,'age50':60,'male':30,'female':70,'rating':5.0},
      }
user_filter = {'category':1,'price':1,'explore':0,'distance':1}
user_data = {'ID':1234,'PW':1234,'age':31,'gender':0,'category':[10,50,10,10,10],'price':[50,30,0,0,0],'distance':[15,20,15,10,10]}


candi = []
temp_candi = []
temp_candi2 = []

with open('searchlist.txt') as data:
    lines = data.read().splitlines()
for line in lines:
    temp_candi.append({'name':line.split(',')[0],'distance':int(line.split(',')[1])})
data.close()

# filter option
# category  1:무관/2:한식/3:중식/4:일식/5:양식/6:기타
# price     1:무관/2:0-10000/3:10000-15000/4:15000-20000/5:20000-25000/6:25000-
# explore   0:기본점수낮게/1:기본점수높게
# distance  1:무관/2:5분이내/3:10분이내/4:15분이내/5:20분이내/6:25분이내



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
    if x['price'] < 10000:      x['partial_price'] = 2
    elif x['price'] < 15000:    x['partial_price'] = 3
    elif x['price'] < 20000:    x['partial_price'] = 4
    elif x['price'] < 25000:    x['partial_price'] = 5
    else:                       x['partial_price'] = 6

# 거리도 구간화
    if x['distance'] < 180:     x['partial_distance'] = 2
    elif x['distance'] < 225:   x['partial_distance'] = 3
    elif x['distance'] < 270:   x['partial_distance'] = 4
    elif x['distance'] < 315:   x['partial_distance'] = 5
    elif x['distance'] < 400:   x['partial_distance'] = 6
    else:                       x['partial_distance'] = 7


for x in temp_candi2:
    if user_filter['price'] == 1:                           # 가격대로 2차 필터링
        candi.append(x)
    elif x['partial_price'] == user_filter['price']:
        candi.append(x)


                 
##### 점수계산 #####

# category '무관' 선택시 모든 후보군에 성향 수치만큼 가산점
if user_filter['category'] == 1:
    for x in candi:
        x['score'] += user_data['category'][x['category']-2]


# price '무관' 선택시 모든 후보군에 성향 수치만큼 가산점
if user_filter['price'] == 1:
    for x in candi:
        x['score'] += user_data['price'][x['partial_price']-2]


# distance '무관' 선택시 모든 후보군에 성향 수치만큼 가산점
if user_filter['distance'] == 1:
    for x in candi:
        x['score'] += user_data['distance'][x['partial_distance']-2]

        
# age 자신이 해당하는 나이대의 선호도/10을 점수로 얻음
for x in candi:
    if user_data['age'] < 10:    continue
    elif user_data['age'] < 20:  x['score'] += x['age10']/10
    elif user_data['age'] < 30:  x['score'] += x['age20']/10
    elif user_data['age'] < 40:  x['score'] += x['age30']/10
    elif user_data['age'] < 50:  x['score'] += x['age40']/10
    elif user_data['age'] < 60:  x['score'] += x['age50']/10


# gender 0:남,1:여 선호비율/10의 점수를 얻음
for x in candi:
    if user_data['gender']: x['score'] += x['female']/10
    else:                   x['score'] += x['male']/10


# rate 별점수치만큼 점수+
for x in candi:
    x['score'] += x['rating']

    
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

'''
for x in candi:
    print(x['name'],x['hitrate'])
'''
# hitrate를 바탕으로 랜덤하게 식당을 선택
def random_select(candi):
    total_hitrate = 0
    random_num = random.random() * 100

    for x in candi:
        total_hitrate += x['hitrate']
        if total_hitrate > random_num:
            return x
        

result = random_select(candi)
print(result['name'])


