from django.shortcuts import render
from enrichment_analysis.enrichment import enrichment
from django.http import JsonResponse
# Create your views here.

def enrichment_page(request):
    return render(request, 'enrichment.html')

def enrichment_ajax(request):
    seq_data = request.POST["seq"]
    correction = request.POST["Correction"]
    p_limit = float(request.POST["p_limit"])
    #############################################################
    ## 將enrichment作業中的enrichment function複製到這裡
    enrichment_result = enrichment(seq_data, correction, p_limit)
    #############################################################
    return JsonResponse({"enrichment_result":enrichment_result})