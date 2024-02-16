from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')
import numpy as np
from screener.class_list import *
import os
from  more_itertools import unique_everseen
from lifelines.statistics import logrank_test
import csv
current_path = os.path.dirname(__file__)

def survival_plot_realtime(project, primary_site, search_by, GT_input,random_id, Low_Percentile, High_Percentile, survival_select, survival_days:int =None):
    if survival_days==None:
        survival_days = survival_max_days(project, GT_input, search_by, survival_select)["max_survival_days"]
    # project = request.POST['project']
    # primary_site = request.POST['primary_site']
    # search_by = request.POST['search_by']
    # GT_input = request.POST['GT_input']
    # random_id = request.POST['random_id']
    # Low_Percentile = request.POST['Low_Percentile']
    # High_Percentile = request.POST['High_Percentile']
    # survival_days = request.POST['survival_days']
    # survival_select = request.POST['survival_select']
    table_name = '%s_%s_FPKM_Cufflinks'%(project,search_by)
    column_table = "%s|%s"%(survival_select,table_name)
 #### patched by t50504
    survival_data = Survival_plot.survival_data_realtime(column_table,search_by,GT_input)
    survival_str = ""
    case_id_list = []

    FPKM_list = [float(y.split("|")[0]) for x in survival_data for y in x.split(',')]
    low_quartile = np.percentile(FPKM_list, float(Low_Percentile))
    high_quartile = np.percentile(FPKM_list, 100-float(High_Percentile))

    T1 = [] #high 存活天數
    E1 = [] #high 是否死亡
    T2 = []
    E2 = []
    high_case = []
    low_case = []
    high_FPKM = []
    low_FPKM = []

    for stage in survival_data:
        for info in stage.split(','):
            FPKM = float(info.split('|')[0])
            case_id = info.split('|')[1]

            survival_times = float(info.split('|')[2]) if info.split('|')[2] != 'None' else info.split('|')[2] #存活天數
            # print(case_id,survival_times)
            survival_events = False if info.split('|')[3] == 'alive' else True #是否死亡
            if FPKM > high_quartile and (survival_times != 0 and survival_times != 'None') and survival_times <= float(survival_days):
                T1 += [survival_times]
                E1 += [survival_events]
                case_id_list += [case_id]
                high_case += [case_id]
                high_FPKM += [FPKM]
            elif FPKM < low_quartile and (survival_times != 0 and survival_times != 'None') and survival_times <= float(survival_days):
                T2 += [survival_times]
                E2 += [survival_events]
                case_id_list += [case_id]
                low_case += [case_id]
                low_FPKM += [FPKM]

    if (T2 != [] and E2 != []) and (T1 != [] and E1 != []):
        _, img_str = Survival_plot.survival_plot(T1,E1,T2,E2,GT_input,primary_site,random_id,Low_Percentile,High_Percentile,max(T1+T2),survival_select)
        # survival_download = Survival_plot.survival_download(T1,E1,T2,E2,high_case,low_case,high_FPKM,low_FPKM,GT_input,primary_site,Low_Percentile,High_Percentile,'all stage')
        survival_csv = survival_download(T1,E1,T2,E2,high_case,low_case,high_FPKM,low_FPKM,GT_input,primary_site, random_id, Low_Percentile,High_Percentile,survival_select)
    else:
        survival_str = ' Survival analysis is not available for '+GT_input+' since more than half of the samples have zero expression.'
        img_str = ''
    return img_str
    # return render(request, 'query/query_by_gene2.html', locals())

def survival_max_days(project: str, GT_input: str, search_by: str, survival_select: str) -> dict:
    table_name = '%s_%s_FPKM_Cufflinks'%(project,search_by)
    column_table = "%s|%s"%(survival_select,table_name)
    survival_data = "".join(Survival_plot.survival_data_realtime(column_table,search_by,GT_input)).split(",")
    # print(f"survival_data: {survival_data}")
    survival_days = [float(x.split("|")[2]) for x in survival_data if x.split("|")[2] != 'None']
    max_survival_days = max(survival_days)
    return {"max_survival_days": max_survival_days}

def survival_download(T1,E1,T2,E2,high_case,low_case,high_FPKM,low_FPKM,GT_input,primary_site,random_id,Low_Percentile,High_Percentile,survival_select):
    output_data = [
                    ['Query: %s'%(GT_input)],
                    ['Primary site: %s'%(primary_site)],
                    ['Low Percentile: %s'%(Low_Percentile)],
                    ['High Percentile: %s'%(High_Percentile)],
                    ['Condition: %s'%(survival_select)],
                    [],
                    ['Patient','Days','Status','Expression','Group']
                ]
    
    for idx,row in enumerate(low_case):
        Status = 'Alive' if E2[idx] == False else 'Dead'
        output_data += [[row,T2[idx],Status,low_FPKM[idx],'Low']]
    for idx,row in enumerate(high_case):
        Status = 'Alive' if E1[idx] == False else 'Dead'
        output_data += [[row,T1[idx],Status,high_FPKM[idx],'High']]
    print('survival_download')

    # download file
    filename=f"Survival_Profile_{primary_site}_{GT_input}_{High_Percentile}_{Low_Percentile}.csv"
    with open(f"{current_path}/../static/data/csv_result/{filename}", "w") as f:
        writer = csv.writer(f)
        for e in output_data:
            writer.writerow(e)
    return output_data