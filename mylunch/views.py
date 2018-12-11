from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template.context_processors import csrf
from django.http import HttpResponse
from django.contrib.auth.models import User
from mylunch.forms import *
from crawl.WEB_crawling import crawl
from mylunch.models import *
from recommend.recommend import recommend
from mylunch import choices
from recommend.update import update


def index(request):
    template = get_template('root.html')
    context = {}
    return HttpResponse(template.render(context))


def rec_page(request):
    if not request.user.is_authenticated:
        return redirect('/')
    template = get_template('recommend.html')

    crawl_list = []

    if request.method == 'POST':
        form_data = Filter_form(request.POST)
        if form_data.is_valid():
                type = form_data.cleaned_data['type']
                price = form_data.cleaned_data['price']
                exp = form_data.cleaned_data['exp']
                distance = form_data.cleaned_data['distance']
                #print(type, price, exp, distance)
                filter = {}
                filter['category'] = int(type)
                filter['price'] = int(price)
                filter['explore'] = int(exp)
                filter['distance'] = int(distance)
                #print(len(request.POST) - 6)
                for i in range(1, len(request.POST) - 6):
                    name, dis = request.POST[str(i)].split(',')
                    temp = {}
                    temp['name'] = name
                    temp['distance'] = int(dis)
                    crawl_list.append(temp)
                #print(crawl_list)

                result = recommend(crawl_list, request.user, filter)
                if result is False:
                    result = {'name': '해당 정보에 맞는 식당이 없습니다'}
                return result_page(request, result=result)

    else:
        form_data = Filter_form()

    context = {'filter': form_data}
    context.update(csrf(request))
    return HttpResponse(template.render(context))


def result_page(request, result={'name': 'dummy'}):
    if not request.user.is_authenticated:
        return redirect('/')
    template = get_template('result.html')
    data = []
    result_print = {'name': result['name']}
    if request.method == 'POST':
        if request.POST.get('yes') is not None:
            temp = list(request.POST.get('yes'))
            result['category'] = temp[0]
            result['partial_price'] = temp[1]
            result['partial_distance'] = temp[2]
            update(request.user, result, 0)
            print('yes')
            return redirect('rec')
        elif request.POST.get('no') is not None:
            temp = list(request.POST.get('yes'))
            result['category'] = temp[0]
            result['partial_price'] = temp[1]
            result['partial_distance'] = temp[2]
            update(request.user, result, 1)
            print('no')
            return redirect('rec')

    if result['name'] != '해당 정보에 맞는 식당이 없습니다':
        for key in result:
            if key is not 'name' and key is not 'rating':
                result[key] = int(result[key])
        for ch in choices.TYPE:
            if Decimal(result['category']) + 1 == ch[0]:
                result_print['category'] = ch[1]
                data.append(str(int(result['category'])))
                break
        for ch in choices.PRICE:
            if Decimal(result['partial_price']) + 1 == ch[0]:
                result_print['partial_price'] = ch[1]
                data.append(str(int(result['partial_price'])))
                break

        result_print['partial_distance'] = '30분 이내'
        data.append(str(int(result['partial_distance'])))
        for ch in choices.DISTANCE:
            if Decimal(result['partial_distance']) + 1 == ch[0]:
                result_print['partial_distance'] = ch[1]
                data[-1] = str(int(result['partial_distance']))
                break

        if result['rating'] == -1:
            result_print['rating'] = '정보 없음'
        else:
            result_print['rating'] = result['rating']
    print(result)
    print(data)
    data = ''.join(data)
    print(data)
    context = {'result': result_print, 'data': data}
    context.update(csrf(request))
    return HttpResponse(template.render(context))


def save_db(request):
    template = get_template('recommend.html')
    #if not request.user.is_authenticated:
    #    return redirect('/user/login/')
    crawl_list = []
    dis_list = []
    if request.method == 'POST':
        #print(request.POST)
        form_data = Filter_form(request.POST)
        if form_data.is_valid():
                type = form_data.cleaned_data['type']
                price = form_data.cleaned_data['price']
                exp = form_data.cleaned_data['exp']
                distance = form_data.cleaned_data['distance']
                print(type, price, exp, distance)
                print(len(request.POST) - 6)
                for i in range(1, len(request.POST) - 6):
                    name, dis = request.POST[str(i)].split(',')
                    crawl_list.append(name)
                    dis_list.append(dis)
                print(crawl_list)
                print(dis_list)
                print(request.POST['0'])
                #tblDemograph.objects.create(dbID=dbID[request.user], NoDemo=NoDemo, DoB=DoB, Sex=Sex, Marital_Status=Marital_Status, Rehab_Setting=Rehab_Setting)
                info = crawl(request.POST['0'], crawl_list, 'phantomjs-2.1.1-windows/bin/phantomjs')
                for item in info:
                    try:
                        obj = Restaurant.objects.get(name=item['input_name'])
                    except:
                        age = item['age_percent_list']
                        gender = item['gender_ratio_list']
                        print(age, gender)
                        Restaurant.objects.create(name=item['input_name'], age10=age[0], age20=age[1], age30=age[2],
                                                  age40=age[3], age50=age[4], age60=age[5], female=gender[0], male=gender[1],
                                                  rating=item['rating'], category=item['category'], price=item['major_menu_price_int'])

                return redirect('/')
    else:
        form_data = Filter_form()

    context = {'filter': form_data}
    context.update(csrf(request))
    return HttpResponse(template.render(context))