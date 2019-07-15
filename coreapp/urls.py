from django.conf.urls import url

from coreapp import views

urlpatterns = [
    url(r'getfunds', views.GetFundsView.as_view()),
    url(r'getportfolio', views.GetPortfolioView.as_view()),
    url(r'^', views.HomePageView.as_view()),
]
