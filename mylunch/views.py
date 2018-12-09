from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template.context_processors import csrf
from django.http import HttpResponse
from django.contrib.auth.models import User
from mylunch.forms import *
from crawl.WEB_crawling import crawl


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
                info = crawl('서강대', crawl_list, 'phantomjs-2.1.1-windows/bin/phantomjs')
                print(info)
                return redirect('/')
    else:
        form_data = Filter_form()

    context = {'filter': form_data}
    context.update(csrf(request))
    return HttpResponse(template.render(context))


def test(request):
    template = get_template('test.html')
    #if not request.user.is_authenticated:
    #    return redirect('/user/login/')
    if request.method == 'POST':
        print(request.POST)
        form_data = test_form(request.POST)
        if form_data.is_valid():
            sex = form_data.cleaned_data['sex']
            print(sex)

    context = {}
    context.update(csrf(request))
    return HttpResponse(template.render(context))