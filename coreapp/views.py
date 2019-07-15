import os

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from django.conf import settings

from util.analyzer import WeightedAverage
# analyzer = apps.get_model('util', 'Analyzer')

# Create your views here.

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        print('request1', request)
        return render(request, 'index.html', context=None)


class GetFundsView(TemplateView):
    def get(self, request, **kwargs):
        funds = list(map(lambda x: os.path.splitext(x)[0], os.listdir(settings.BASE_DIR + '/util/mf-data')))
        return JsonResponse(funds, safe=False)

class GetPortfolioView(TemplateView):
    def get(self, request, **kwargs):
        funds = WeightedAverage(request.GET.dict(), to_json=True)
        return HttpResponse(funds, content_type='application/json')
