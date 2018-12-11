### 사용자가 확인/다시 눌렀을때 실행될 모듈 ###
from member.models import UserInfo

############### input data ##################
#                                           #
# USER   : django 객체                      #
# result : recommend에서 리턴된 식당정보    #
# command: 0:확인/1:다시                    #
#                                           #
#############################################


def update(USER, result, command):
    info = UserInfo.objects.get(user=USER)
    print(result, command)

    if command == 0:
        # 추천된 식당의 속성에 대한 사용자의 선호도를 올림
        if result['category'] == '1':  info.category1 += 5
        if result['category'] == '2':  info.category2 += 5
        if result['category'] == '3':  info.category3 += 5
        if result['category'] == '4':  info.category4 += 5
        if result['category'] == '5':  info.category5 += 5
        if result['partial_price'] == '1':  info.price1 += 5
        if result['partial_price'] == '2':  info.price2 += 5
        if result['partial_price'] == '3':  info.price3 += 5
        if result['partial_price'] == '4':  info.price4 += 5
        if result['partial_distance'] == '1':  info.distance1 += 5
        if result['partial_distance'] == '2':  info.distance2 += 5
        if result['partial_distance'] == '3':  info.distance3 += 5
        if result['partial_distance'] == '4':  info.distance4 += 5
        if result['partial_distance'] == '5':  info.distance5 += 5

        
    elif command == 1:
        # 추천된 식당의 속성에 대한 사용자의 선호도를 내림
        if result['category'] == '1' and info.category1 > 5:  info.category1 -= 5
        if result['category'] == '2' and info.category2 > 5:  info.category2 -= 5
        if result['category'] == '3' and info.category3 > 5:  info.category3 -= 5
        if result['category'] == '4' and info.category4 > 5:  info.category4 -= 5
        if result['category'] == '5' and info.category5 > 5:  info.category5 -= 5
        if result['partial_price'] == '1' and info.price1 > 5:  info.price1 -= 5
        if result['partial_price'] == '2' and info.price2 > 5:  info.price2 -= 5
        if result['partial_price'] == '3' and info.price3 > 5:  info.price3 -= 5
        if result['partial_price'] == '4' and info.price4 > 5:  info.price4 -= 5
        if result['partial_distance'] == '1' and info.distance1 > 5:  info.distance1 -= 5
        if result['partial_distance'] == '2' and info.distance2 > 5:  info.distance2 -= 5
        if result['partial_distance'] == '3' and info.distance3 > 5:  info.distance3 -= 5
        if result['partial_distance'] == '4' and info.distance4 > 5:  info.distance4 -= 5
        if result['partial_distance'] == '5' and info.distance5 > 5:  info.distance5 -= 5

    info.save()
