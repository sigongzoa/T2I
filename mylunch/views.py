from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template.context_processors import csrf
from django.http import HttpResponse
from django.contrib.auth.models import User
from mylunch.forms import *

def index(request):
    template = get_template('root.html')
    context = {}
    return HttpResponse(template.render(context))


def rec_page(request):
    template = get_template('recommend.html')
    #if not request.user.is_authenticated:
    #    return redirect('/user/login/')
    if request.method == 'POST':
        #print(request.POST)
        form_data = Filter_form(request.POST)
        if form_data.is_valid():
                type = form_data.cleaned_data['type']
                price = form_data.cleaned_data['price']
                exp = form_data.cleaned_data['exp']
                distance = form_data.cleaned_data['distance']
                print(type, price, exp, distance)
                for i in range(len(request.POST) - 6):
                    print(request.POST[str(i)])
                #tblDemograph.objects.create(dbID=dbID[request.user], NoDemo=NoDemo, DoB=DoB, Sex=Sex, Marital_Status=Marital_Status, Rehab_Setting=Rehab_Setting)
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