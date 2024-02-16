from django.shortcuts import render
import numpy as np
from survival_analysis.class_list import *
from survival_analysis.function_list import *
import os
import random
from  more_itertools import unique_everseen
import json
# from lifelines.statistics import logrank_test
from tqdm import tqdm, trange
from django.http import HttpResponse, JsonResponse #匯入http模組
from django.template.defaulttags import register
import multiprocessing
from functools import partial
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from survival_analysis.models import *
import matplotlib
# from survival_analysis.survival_analysis_v3 import *
matplotlib.use('Agg')
current_path = os.path.dirname(__file__)

stage_dict = {
    'normal' :'normal',
    'stage i' : 'stage_1',
    'stage ii' : 'stage_2',
    'stage iii' : 'stage_3',
    'stage iv' : 'stage_4',
}

# Create your views here.
def search_page(request):
    cursor = connections['default'].cursor()
    cursor.execute("SELECT `gene`,`transcripts` FROM `hg38_gene_transcripts_20180130`")
    result = cursor.fetchall()
    gene_list = [row[0] for row in result]
    gene_list = json.dumps(gene_list)
    # print(gene_list)
    transcript_list = []
    for row in result:
        for transcript in row[1].split(','):
            transcript_list += [transcript]
    transcript_list = pd.DataFrame({0:transcript_list})
    path = f'{current_path}/../static/data/error_isoforms.txt'
    f = open(path, 'r')
    error_isoforms = eval(f.read())
    f.close()
    transcript_list = transcript_list[~transcript_list[0].isin(error_isoforms)]
    transcript_list = json.dumps(list(transcript_list[0]))
    
    cursor.execute("SELECT DISTINCT `primary_site`,`project`,`#_of_normal`,`#_of_stage_1`,`#_of_stage_2`,`#_of_stage_3`,`#_of_stage_4`,`#_of_stage_5`,`#_of_nos`,`#_of_is`,`#_of_tumor` FROM `Mutual_Relationship_search3` ORDER BY `primary_site`")
    result1 = cursor.fetchall()
    primary_project_list = [row for row in result1]
    primary_project_samplenumber = OrderedDict()
    for row in result1:
        primary_project = "%s|%s"%(row[0],row[1])
        if primary_project not in primary_project_samplenumber:
            primary_project_samplenumber[primary_project] = {
                                                            'normal':row[2],
                                                            'stage i':row[3],
                                                            'stage ii':row[4],
                                                            'stage iii':row[5],
                                                            'stage iv':row[6],
                                                            'stage x':row[7],
                                                            'nos':row[8],
                                                            'is':row[9],
                                                            'tumor':row[10],
                                                            }
    # print(primary_project_samplenumber)
    primary_project_stage = OrderedDict()
    cursor.execute("SELECT DISTINCT `primary_site`,`project`,`condition1`,`condition2` FROM `Mutual_Relationship_search3`")
    result2 = cursor.fetchall()
    for row in result2:
        primary_project = "%s|%s"%(row[0],row[1])
        if primary_project not in primary_project_stage:
            primary_project_stage[primary_project] = list(unique_everseen([row[2],row[3]]))

        else:
            if row[2] not in primary_project_stage[primary_project]:
                primary_project_stage[primary_project] += [row[2]]
            if row[3] not in primary_project_stage[primary_project]:
                primary_project_stage[primary_project] += [row[3]]
    return render(request, 'survival_analysis_search.html', locals())

@csrf_exempt
def screener_page(request):
    cursor = connections['default'].cursor()
    cursor.execute("SELECT DISTINCT `primary_site`,`project` FROM `Mutual_Relationship` ORDER BY `primary_site`")
    result = cursor.fetchall()
    primary_project_list = [row for row in result]
    return render(request, 'screener.html', locals())

# this function can be called in html
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
def detail_page(request):
    stage_dict = {
        'normal' :'normal',
        'stage i' : 'stage_1',
        'stage ii' : 'stage_2',
        'stage iii' : 'stage_3',
        'stage iv' : 'stage_4',
    }
    primary_site, project = request.GET["cancer"].split("|")
    input_type = request.GET["type"]
    name = request.GET["name"]
    Low_Percentile = request.GET["lp"]
    High_Percentile = request.GET["hp"]
    stage = request.GET["stage"]
    max_days = survival_max_days(project, name, input_type, stage)["max_survival_days"]
    img_str = survival_plot_realtime(project, primary_site, input_type, name ,'0', Low_Percentile, High_Percentile, stage)
    gene = Detail.belong_gene(input_type,name) if input_type == 'isoforms' else name
    genelink_dict = Filter.gene_link([gene],input_type)
    all_transcript1 = Detail.all_transcript(gene)
    all_transcript = []
    path = f'{current_path}/../static/data/error_isoforms.txt'
    f = open(path, 'r')
    error_isoforms = eval(f.read())
    f.close()
    for i in all_transcript1:
        if(i not in error_isoforms):
            all_transcript.append(i)
    NCBI_gene_summary = Summary.NCBI_gene_summary(gene)
    NCBI_transcript_summary = Summary.NCBI_transcript_summary(all_transcript)
    # project_primary_dict = Filter.project_primary_dict()[0]
    # primary_list_all = list(project_primary_dict.values())
    # number_of_sample = Filter.project_primary_dict()[1]
    primary_key = input_type[:-1]+'_name'
    # TEST_column = "%s_%s"%(TEST_select.replace(' ','_'),TESTstates_select.replace(' ','').lower()) if TEST_select else ''

    # condition_FC_qv_list = Filter.filter(input_type,name,primary_key,list(project_primary_dict.keys()),FC_select,FC_input,TEST_column,TEST_input)
    # primary_list = sorted(list(set([project_primary_dict[x[0]] for x in condition_FC_qv_list])))
        
    # for cancer in primary_list:
    #     condition_FC_qv_list_cancer = []
    #     for row in condition_FC_qv_list:
    #         if project_primary_dict[row[0]] == cancer:
    #             condition_FC_qv_list_cancer += [row]
        # download_table = Filter.download_table(cancer,condition_FC_qv_list_cancer,name,FC_select,FC_input,TEST_select,TESTstates_select,TEST_input)
        # request.session["DE_Conditions_%s_%s"%(cancer,"0")] = download_table
    stage_dict_gather = {
        'normal' :'normal',
        'stage i' : 'stage_1',
        'stage ii' : 'stage_2',
        'stage iii' : 'stage_3',
        'stage iv' : 'stage_4',
    }
    stage_Arabic_dict = {
        'normal' :'N',
        'stage i' : '1',
        'stage ii' : '2',
        'stage iii' : '3',
        'stage iv' : '4',
    }
    primary_stage = OrderedDict()
    primary_condition = OrderedDict()
    project_list = []
    # primary_list = []
    # for row in condition_FC_qv_list:
    #     primary_project = "%s|%s"%(project_primary_dict[row[0]],row[0])
    #     c1_pair = "%s(%s_%s)"%(stage_dict_gather[row[1]],stage_Arabic_dict[row[1]],stage_Arabic_dict[row[2]])
    #     c2_pair = "%s(%s_%s)"%(stage_dict_gather[row[2]],stage_Arabic_dict[row[1]],stage_Arabic_dict[row[2]])
    #     if primary_project not in primary_stage:
    #         primary_stage[primary_project] = [[c1_pair,c2_pair]]
    #         primary_condition[primary_project] = [row[1],row[2]]
    #     else:
    #         primary_stage[primary_project] += [[c1_pair,c2_pair]]
    #         primary_condition[primary_project] += [row[1],row[2]]
    #     if row[0] not in project_list:
    #         project_list += [row[0]]
    primary_condition = OrderedDict(sorted(primary_condition.items()))
    primary_stage = OrderedDict(sorted(primary_stage.items()))

    condition_list = list(primary_condition.values())
    group_name = list(primary_stage.values())
    # condition_list = list(map(lambda x:sorted(x),list(primary_stage.values())))
    boxplot_data,primary_nodata = Boxplot.boxplot_data(primary_stage,input_type,name)
    print(boxplot_data)
    return render(request, 'survival_analysis_detail.html', locals())

@csrf_exempt
def survival_plot(request):
    project = request.POST["project"]
    primary_site = request.POST["primary_site"]
    input_type = request.POST["type"]
    name = request.POST["name"]
    Low_Percentile = request.POST["Low_Percentile"]
    High_Percentile = request.POST["High_Percentile"]
    stage = request.POST["stage"]
    # days = request.POST["days"]
    # img_str = survival_plot_realtime(project, primary_site, input_type, name ,'0', Low_Percentile, High_Percentile, stage, days)
    img_str = survival_plot_realtime(project, primary_site, input_type, name ,'0', Low_Percentile, High_Percentile, stage)
    return JsonResponse({"img_str": img_str})

def survival_analysis(request):
    search_by = request.GET.get('search_by')
    GT_input = request.GET.get('GTinput')
    stage_list = request.GET.get('stage_list').split(',')
    table_name = request.GET.get('table_name').replace(' ','')
    cancer = request.GET.get('cancer')  
    primary_check_value = [cancer+'|'+table_name.split('_')[0]]
    random_id = ""
    survival_str = ''
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    genelink_dict = Filter.gene_link([GT_input],search_by)
    for i in range(0,10) :
        random_id += possible[int(random.random() * len(possible))]
    
    primary_project_stage = Others.primary_project_stage()
    Low_Percentile = 50
    High_Percentile = 50
    column_list = []
    primary_site_list = [cancer]
    project_list = [table_name.split('_')[0]]
    for i in stage_list:
        column_list += [stage_dict[i]]
    column_table_list = ["%s|%s"%(','.join(column_list),table_name)]
    survival_data = Survival_plot.survival_data_default(column_table_list,search_by,GT_input)
    max_survival_times = []
    for idx,row in enumerate(survival_data):
        FPKM_list = [float(y.split("|")[0]) for x in row for y in x.split(',')]
        low_quartile = np.percentile(FPKM_list, float(Low_Percentile))
        # print(low_quartile)
        high_quartile = np.percentile(FPKM_list, float(100-High_Percentile))
        # print(high_quartile)
        T1 = [] #high 存活天數
        E1 = [] #high 是否死亡
        T2 = []
        E2 = []
        high_case = []
        low_case = []
        high_FPKM = []
        low_FPKM = []

        primary_site = primary_check_value[idx].split('|')[0]
        project = primary_check_value[idx].split('|')[1]
        for stage in row:
            for info in stage.split(','):
                FPKM = float(info.split('|')[0])
                case_id = info.split('|')[1]
                survival_times = float(info.split('|')[2]) if info.split('|')[2] != 'None' else info.split('|')[2] #存活天數
                survival_events = False if info.split('|')[3] == 'alive' else True #是否死亡
                if FPKM > high_quartile and (survival_times != 0 and survival_times != 'None'):
                    T1 += [survival_times]
                    E1 += [survival_events]
                    high_case += [case_id]
                    high_FPKM += [FPKM]
                elif FPKM < low_quartile and (survival_times != 0 and survival_times != 'None'):
                    T2 += [survival_times]
                    E2 += [survival_events]
                    low_case += [case_id]
                    low_FPKM += [FPKM]
        # print(T1,E1,T2,E2)
        if (T2 != [] and E2 != []) and (T1 != [] and E1 != []):
            Survival_plot.survival_plot(T1,E1,T2,E2,GT_input,primary_site,random_id,Low_Percentile,High_Percentile,max(T1+T2),'all stage')
            # survival_download = Survival_plot.survival_download(T1,E1,T2,E2,high_case,low_case,high_FPKM,low_FPKM,GT_input,primary_site,random_id,Low_Percentile,High_Percentile,'all stage')
            # request.session["Survival_Profile_%s_%s_%s_%s"%(primary_site.replace('(','').replace(')',''),Low_Percentile,High_Percentile,random_id)] = survival_download

        else:
            survival_str = ' Survival analysis is not available for '+GT_input+' since more than half of the samples have zero expression.'
        max_survival_times += [max(T1+T2)]
    return render(request, 'detail/survival_analysis.html', locals())

@csrf_exempt
def cal_pvalue_main(request):
    input_type = request.POST["type"]
    cancer = request.POST["cancer"]
    stage = request.POST["stage"]
    high_percent = request.POST["high_percent"]
    low_percent = request.POST["low_percent"]
    input_pvalue = request.POST["pvalue"]
    primary_site, project = cancer.split("|")

    table_name = '%s_%s_FPKM_Cufflinks'%(project,input_type)
    column_table = "%s|%s"%(stage,table_name)
    cursor = connections['edward_Cufflinks'].cursor()
    primary_key = 'gene_name' if input_type == 'genes' else 'isoform_name'
    stage_list = ['stage_1','stage_2','stage_3','stage_4']
    all_cancer_data = get_allcancer_data(column_table, input_type)
    result_list = []
    # print(all_cancer_data[0][1:])
    # print(all_cancer_data[0])

    ## multiprocessing
    with multiprocessing.Manager() as manager:
        result_list_m = manager.list()
        # 創建一個 multiprocessing.Pool
        pool = multiprocessing.Pool()
        # 使用 map 函數來平行處理數據
        # 注意: 如果 all_cancer_data 很大，可以考慮使用 imap 或者 imap_unordered 來節省記憶體
        pool.starmap(process_data, [(data, low_percent, high_percent, input_pvalue, result_list_m) for data in tqdm(all_cancer_data)])
        # 關閉 pool
        pool.close()
        pool.join()
        # 在這裡，result_list_m 包含所有符合條件的結果
        # print(result_list_m)
        result_list = list(result_list_m)
    
    ## original
    # # for i in tqdm(range(len(all_cancer_data))):
    # for i in tqdm(range(1000)):
    #     p_value, max_time = organize_and_cal_pvalue(all_cancer_data[i], low_percent, high_percent)
    #     if p_value <= float(input_pvalue):
    #         result_list.append({"name":all_cancer_data[i][0], "logrank_p_value":p_value, "max_time": max_time})
    # # print(f"result_list: {result_list}")
    str_colmns = ','.join(stage_list)
    return JsonResponse({"result": result_list})

## function for multiprocessing star map
def process_data(data, low_percent, high_percent, input_pvalue, result_list):
        p_value, max_time = organize_and_cal_pvalue(data, low_percent, high_percent)
        if p_value <= float(input_pvalue):
            result_list.append({"name": data[0], "logrank_p_value": p_value, "max_time": max_time})

# # function for multiprocessing imap
# def process_data(index, data, low_percent, high_percent, input_pvalue, result_list):
#     p_value, max_time = organize_and_cal_pvalue(data, low_percent, high_percent)
#     if p_value <= float(input_pvalue):
#         result_list[index] = {"name": data[0], "logrank_p_value": p_value, "max_time": max_time}

# def survival_max_days(project, GT_input, search_by, survival_select) -> float:
#   table_name = '%s_%s_FPKM_Cufflinks'%(project,search_by)
#   column_table = "%s|%s"%(survival_select,table_name)

#   survival_data = "".join(Survival_plot.survival_data_realtime(project, column_table,search_by,GT_input)).split(",")
#   survival_days = [float(x.split("|")[2]) for x in survival_data if x.split("|")[2] != 'None']
#   max_survival_days = max(survival_days)
#   return max_survival_days