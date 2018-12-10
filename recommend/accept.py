### 사용자가 확인 눌렀을때 실행될 모듈 ###


# 임의로 만든 데이터

user_data = {'ID':1234,'PW':1234,'age':31,'gender':0,'category':[10,50,10,10,10],'price':[50,30,0,0,0],'distance':[15,20,15,10,10]}

result = {'name': '순이네칼국수', 'distance': 181, 'score': 72.0, 'category': 2, 'price': 12000, 'age10': 30, 'age20': 40, 'age30': 40, 'age40': 80, 'age50': 60, 'male': 30, 'female': 70, 'rating': 5.0, 'partial_price': 3, 'partial_distance': 3, 'hitrate': 29.674796747967477}


# 추천된 식당의 속성에 대한 사용자의 선호도를 올림
user_data['category'][result['category']-2] = user_data['category'][result['category']-2] + 5
user_data['price'][result['partial_price']-2] = user_data['price'][result['partial_price']-2] + 5
user_data['distance'][result['partial_distance']-2] = user_data['distance'][result['partial_distance']-2] + 5

print(user_data)
