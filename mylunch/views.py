from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template.context_processors import csrf
from django.http import HttpResponse
from django.contrib.auth.models import User
from mylunch.forms import *
from crawl.WEB_crawling import crawl
from mylunch.models import *
import json

def index(request):
    template = get_template('root.html')
    context = {}
    return HttpResponse(template.render(context))


def rec_page(request):
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
                #tblDemograph.objects.create(dbID=dbID[request.user], NoDemo=NoDemo, DoB=DoB, Sex=Sex, Marital_Status=Marital_Status, Rehab_Setting=Rehab_Setting)
                return redirect('/')
    else:
        form_data = Filter_form()

    context = {'filter': form_data}
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
                    print(item)
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