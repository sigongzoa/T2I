### 사용자가 확인/다시 눌렀을때 실행될 모듈 ###


############### input data ##################
#                                           #
# USER   : django 객체                      #
# result : recommend에서 리턴된 식당정보    #
# command: 0:확인/1:다시                    #
#                                           #
#############################################


def update(USER,result,command):

    if command == 0:
        # 추천된 식당의 속성에 대한 사용자의 선호도를 올림
        if result['category'] == 1:  USER.UserInfo.category1 += 5
        if result['category'] == 2:  USER.UserInfo.category2 += 5
        if result['category'] == 3:  USER.UserInfo.category3 += 5
        if result['category'] == 4:  USER.UserInfo.category4 += 5
        if result['category'] == 5:  USER.UserInfo.category5 += 5
        if result['partial_price'] == 1:  USER.UserInfo.price1 += 5
        if result['partial_price'] == 2:  USER.UserInfo.price2 += 5
        if result['partial_price'] == 3:  USER.UserInfo.price3 += 5
        if result['partial_price'] == 4:  USER.UserInfo.price4 += 5
        if result['partial_distance'] == 1:  USER.UserInfo.distance1 += 5
        if result['partial_distance'] == 2:  USER.UserInfo.distance2 += 5
        if result['partial_distance'] == 3:  USER.UserInfo.distance3 += 5
        if result['partial_distance'] == 4:  USER.UserInfo.distance4 += 5
        if result['partial_distance'] == 5:  USER.UserInfo.distance5 += 5

        
    elif command == 1:
        # 추천된 식당의 속성에 대한 사용자의 선호도를 내림
        if result['category'] == 1 & USER.UserInfo.category1 > 5:  USER.UserInfo.category1 -= 5
        if result['category'] == 2 & USER.UserInfo.category2 > 5:  USER.UserInfo.category2 -= 5
        if result['category'] == 3 & USER.UserInfo.category3 > 5:  USER.UserInfo.category3 -= 5
        if result['category'] == 4 & USER.UserInfo.category4 > 5:  USER.UserInfo.category4 -= 5
        if result['category'] == 5 & USER.UserInfo.category5 > 5:  USER.UserInfo.category5 -= 5
        if result['partial_price'] == 1 & USER.UserInfo.price1 > 5:  USER.UserInfo.price1 -= 5
        if result['partial_price'] == 2 & USER.UserInfo.price2 > 5:  USER.UserInfo.price2 -= 5
        if result['partial_price'] == 3 & USER.UserInfo.price3 > 5:  USER.UserInfo.price3 -= 5
        if result['partial_price'] == 4 & USER.UserInfo.price4 > 5:  USER.UserInfo.price4 -= 5
        if result['partial_distance'] == 1 & USER.UserInfo.distance1 > 5:  USER.UserInfo.distance1 -= 5
        if result['partial_distance'] == 2 & USER.UserInfo.distance2 > 5:  USER.UserInfo.distance2 -= 5
        if result['partial_distance'] == 3 & USER.UserInfo.distance3 > 5:  USER.UserInfo.distance3 -= 5
        if result['partial_distance'] == 4 & USER.UserInfo.distance4 > 5:  USER.UserInfo.distance4 -= 5
        if result['partial_distance'] == 5 & USER.UserInfo.distance5 > 5:  USER.UserInfo.distance5 -= 5

    return command                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
















