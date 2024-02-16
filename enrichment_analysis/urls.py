from django.contrib import admin
from django.urls import path, include
from  enrichment_analysis import views

urlpatterns = [
    path('enrichment_ajax/', views.enrichment_ajax), 
]