from django.urls import path
from . import views


urlpatterns = [
    # path('search/', views.search_page),
    # path('detail/', views.detail_page),
    path('', views.screener_page),
    path('screener_cal_result_gene/', views.screener_cal_result_gene),
    path('primary_site_realtime/', views.primary_site_realtime)
    
    # path('cal_pvalue/', views.cal_pvalue_main),
    # path('sur_plot/', views.survival_plot),

]