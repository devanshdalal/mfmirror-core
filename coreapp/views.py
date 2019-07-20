import os
from subprocess import call

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from util.analyzer import WeightedAverage
from util.utils import BASE_DIR_CSVS

from apscheduler.schedulers.background import BackgroundScheduler


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
            scheduler.add_job(scrpper_job, 'interval', seconds=60)
            scheduler.start()
        funds = list(map(lambda x: os.path.splitext(x)[0], filter(lambda y: not y.startswith('.'), os.listdir(BASE_DIR_CSVS))))
        return JsonResponse(funds, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class GetPortfolioView(TemplateView):
    def post(self, request, **kwargs):
        funds = WeightedAverage(request.GET.dict(), to_json=True)
        return HttpResponse(funds, content_type='application/json')
