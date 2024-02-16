from django.shortcuts import render
import numpy as np
from screener.screener_function import *
import os
import random
from  more_itertools import unique_everseen
import json
from tqdm import tqdm, trange
from django.http import HttpResponse, JsonResponse #匯入http模組
from django.template.defaulttags import register
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from survival_analysis.models import *
import matplotlib
matplotlib.use('Agg')
current_path = os.path.dirname(__file__)

stage_dict = {
    'normal' :'normal',
    'stage i' : 'stage_1',
    'stage ii' : 'stage_2',
    'stage iii' : 'stage_3',
    'stage iv' : 'stage_4',
}

## this function can be called in html
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='divide')
def divide(value,arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return None

@csrf_exempt
def screener_page(request):
    # cursor = connections['default'].cursor()
    # cursor.execute("SELECT DISTINCT `primary_site`,`project` FROM `Mutual_Relationship` ORDER BY `primary_site`")
    # result = cursor.fetchall()
    primary_project_list = [["Liver", "TCGA-LIHC"]]
    with open(f'{current_path}/../static/data/miRNA/homo_mirna_list.csv', 'r') as file:
        reader = csv.reader(file)
        homo_miRNA_list = list(reader)
    # print(len(homo_miRNA_list))
    return render(request, 'screener.html', locals())

@csrf_exempt
def screener_cal_result_gene(request):
    switch_dict = json.loads(request.POST["switch_dict"])
    df = pd.DataFrame()
    switch_true_keys = [key for key, value in switch_dict.items() if value]
    switch_str = ', '.join(switch_true_keys)
    if switch_dict["survival"]:
        input_type = request.POST["type"]
        cancer = request.POST["cancer"]
        stage = request.POST["stage"]
        high_percent = request.POST["high_percent"]
        low_percent = request.POST["low_percent"]
        input_pvalue = float(request.POST["pvalue"])
        cor_method = request.POST["cor_method_sur"]
        ############################################################################################
        ## 放置survival analysis的作業函式 將符合使用者輸入修正方式下pvalue的列輸出
        ## 輸出欄位為"name", "logrank_p_value", "FDR", "Bonferroni"
        _, result_list = cal_pvalue_main(input_type, cancer, stage, high_percent, low_percent, input_pvalue, cor_method)
        df_pvalue = pd.DataFrame(result_list)
        ############################################################################################
        if len(df) == 0:
            df = df_pvalue
        else:
            df = pd.merge(df, df_pvalue, left_on="gene_name", right_on="name", how="inner")
    if switch_dict["miRNA"]:
        selected_miRNA = request.POST.getlist("selected_miRNA[]")
        set_select = request.POST["miRNA_set"]
        if set_select == "union": set_operation = "UNION"
        elif set_select == "intersection": set_operation = "INTERSECT"
        elif "difference" in set_select :
            # Set the value for the "difference" case
            if set_select == "difference2_1":
                selected_miRNA = [selected_miRNA[1], selected_miRNA[0]]
            set_operation = "DIFFERENCE"
        ## query mysql and get data
        #############################################################################
        ## 依據差集、交集或聯集的方式將miRNA的資料輸出，後續df處理方式依據大家寫的調整
        df_miRNA = pd.DataFrame(miRNAscreener_getdata(selected_miRNA, set_operation))
        df_miRNA.dropna(subset = ['gene_name'], inplace=True)
        if set_operation=="INTERSECT":
            for e in selected_miRNA:
                df_miRNA[e] = "o"
        elif set_operation=="DIFFERENCE":
            df_miRNA[selected_miRNA[0]] = "o"
            df_miRNA[selected_miRNA[1]] = "x"
        #############################################################################
        df = df_miRNA if len(df) == 0 else pd.merge(df, df_miRNA, left_on="name", right_on="gene_name", how="inner")
    if switch_dict["DE"]:
        DE_level = request.POST["type"]
        cancer = request.POST["cancer"]
        primary_site, project = cancer.split("|")
        DE_filter = request.POST.getlist("DE_filter[]")
        print(DE_filter)
        ########## need to check condition1 and condition2 column data ##########
        table_data, table_col, replace_col_name = DEscreener_getdata(DE_level, primary_site, project, DE_filter)
        df_DE = pd.DataFrame(table_data, columns=table_col)
        df_DE.rename(columns={replace_col_name: "q-value"}, inplace=True)
        lefton = "name" if "name" in df.columns else "gene_name"
        df = df_DE if len(df) == 0 else pd.merge(df, df_DE, left_on=lefton, right_on="gene_name", how="inner")
    if "name" not in df.columns:
        if "Gene" in df.columns:
            df.rename(columns={"Gene": "name"}, inplace=True)
        elif "gene_name" in df.columns:
            df.rename(columns={"gene_name": "name"}, inplace=True)
    ## js cant accept nan variable
    df.fillna(value=False, inplace=True)
    ## df.to_dict('records') this format can fit in datatable
    result_list = df.to_dict('records')
    return JsonResponse({"result": result_list, "screener_type":switch_str})

## query database by primary site to construct the condition1 and condition2 select option
@csrf_exempt
def primary_site_realtime(request):
    project_select = request.POST['project_select'].strip()
    cursor = connections['default'].cursor()
    cursor.execute("SELECT DISTINCT `project`,`condition1`,`#_of_normal`,`#_of_stage_1`,`#_of_stage_2`,`#_of_stage_3`,`#_of_stage_4`,`#_of_stage_5`,`#_of_nos`,`#_of_is`,`#_of_tumor` FROM `Mutual_Relationship` WHERE `project` = '%s'"%(project_select))
    result = cursor.fetchall()
    condition_list = [row for row in result]
    number_of_sample = {
                        'normal':result[0][2],
                        'stage i':result[0][3],
                        'stage ii':result[0][4],
                        'stage iii':result[0][5],
                        'stage iv':result[0][6],
                        'stage x':result[0][7],
                        'nos':result[0][8],
                        'is':result[0][9],
                        'tumor':result[0][10],
                        }
    return JsonResponse({"number_of_sample": number_of_sample, "condition_list": condition_list})