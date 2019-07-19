import os

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from django.conf import settings

from util.analyzer import WeightedAverage
from util.utils import BASE_DIR_CSVS

from apscheduler.schedulers.background import BackgroundScheduler

from subprocess import call

# Installing scheduler

def scrpper_job():
    print('In job')
    call(['python', 'util/scrapper.py', '--source', 'MC'])

scheduler = None

# Create your views here.

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        print('request1', request)
        return render(request, 'index.html', context=None)


class GetFundsView(TemplateView):
    def get(self, request, **kwargs):
        global scheduler
        if scheduler == None:
            scheduler = BackgroundScheduler()
            scheduler.add_job(scrpper_job, 'interval', seconds=600)
            scheduler.start()
        funds = list(map(lambda x: os.path.splitext(x)[0], filter(lambda y: not y.startswith('.'), os.listdir(BASE_DIR_CSVS))))
        return JsonResponse(funds, safe=False)

class GetPortfolioView(TemplateView):
    def get(self, request, **kwargs):
        funds = WeightedAverage(request.GET.dict(), to_json=True)
        return HttpResponse(funds, content_type='application/json')
