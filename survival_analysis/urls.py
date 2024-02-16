from django.urls import path
from . import views


urlpatterns = [
    path('search/', views.search_page),
    path('detail/', views.detail_page),
    path('screener/', views.screener_page),
    path('cal_pvalue/', views.cal_pvalue_main),
    path('sur_plot/', views.survival_plot),

]