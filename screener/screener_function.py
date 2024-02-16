from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')
import numpy as np
from screener.class_list import *
from screener.function_list import *
import os
from  more_itertools import unique_everseen
from lifelines.statistics import logrank_test
import csv
import multiprocessing
from tqdm import tqdm, trange
from statsmodels.stats.multitest import multipletests
current_path = os.path.dirname(__file__)


# query specific cancer data
def get_allcancer_data(column_table,search_by):
    stage_dict = {
        'stage i' : 'stage_1',
        'stage ii' : 'stage_2',
        'stage iii' : 'stage_3',
        'stage iv' : 'stage_4',
    }
    cursor = connections['default'].cursor()
    primary_key = 'gene_name' if search_by == 'genes' else 'isoform_name'
    # column = primary_key
    # column = stage_dict[column_table.split('|')[0]] if column_table.split('|')[0] != 'all stage' else ','.join(stage_dict.values())
    column = f"{primary_key}, {stage_dict[column_table.split('|')[0]] if column_table.split('|')[0] != 'all stage' else ','.join(stage_dict.values())}"
    print(column)
    table_name = column_table.split('|')[1]
    cursor.execute("SELECT %s FROM `%s`"%(column,table_name))
    result = list(cursor.fetchall())
    cursor.close()
    return result

# organize data and calculate pvalue
def organize_and_cal_pvalue(survival_data: list, Low_Percentile:float, High_Percentile:float) -> float:
    survival_str = ""
    case_id_list = []
    # print(f"before: {survival_data}")
    survival_data = survival_data[1:]
    # print(f"len: {len(survival_data)}")
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
    survival_days = []
    ele = "".join(survival_data).split(",")
    survival_days = [float(x.split("|")[2]) for x in ele if x.split("|")[2] != 'None']
    # print(survival_days)
    max_survival_days = max(survival_days)
    # survival_days = max(T1+T2)
    for stage in survival_data:
        for info in stage.split(','):
            FPKM = float(info.split('|')[0])
            case_id = info.split('|')[1]
            survival_times = float(info.split('|')[2]) if info.split('|')[2] != 'None' else info.split('|')[2] #存活天數
            # print(case_id,survival_times)
            survival_events = False if info.split('|')[3] == 'alive' else True #是否死亡
            if FPKM > high_quartile and (survival_times != 0 and survival_times != 'None') and survival_times <= float(max_survival_days):
                T1 += [survival_times]
                E1 += [survival_events]
                case_id_list += [case_id]
                high_case += [case_id]
                high_FPKM += [FPKM]
            elif FPKM < low_quartile and (survival_times != 0 and survival_times != 'None') and survival_times <= float(max_survival_days):
                T2 += [survival_times]
                E2 += [survival_events]
                case_id_list += [case_id]
                low_case += [case_id]
                low_FPKM += [FPKM]
    if (T2 != [] and E2 != []) and (T1 != [] and E1 != []):
        logrank_result = logrank_test(T1, T2, E1, E2)
        logrank_p_value = logrank_result.p_value
    else:
        # if error condition occur make pvalue very big 
        logrank_p_value = 1
    # print(logrank_p_value)
    return logrank_p_value, max_survival_days

# pvalue screener function
def cal_pvalue_main(input_type, cancer, stage, high_percent, low_percent, input_pvalue, cor_method):
    # input_type = request.POST["type"]
    # cancer = request.POST["cancer"]
    # stage = request.POST["stage"]
    # high_percent = request.POST["high_percent"]
    # low_percent = request.POST["low_percent"]
    # input_pvalue = float(request.POST["pvalue"])
    primary_site, project = cancer.split("|")
    table_name = '%s_%s_FPKM_Cufflinks'%(project,input_type)
    column_table = "%s|%s"%(stage,table_name)
    cursor = connections['default'].cursor()
    primary_key = 'gene_name' if input_type == 'genes' else 'isoform_name'
    stage_list = ['stage_1','stage_2','stage_3','stage_4']
    all_cancer_data = get_allcancer_data(column_table, input_type)
    result_list = []

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
    # for i in tqdm(range(len(all_cancer_data))):
    # for i in tqdm(range(1000)):
    #     p_value, max_time = organize_and_cal_pvalue(all_cancer_data[i], low_percent, high_percent)
    #     ## 之後需要改到計算後再進行篩選
    #     ## 需要考慮修正pvalue的篩選
    #     # if p_value <= float(input_pvalue):
    #     result_list.append({"name":all_cancer_data[i][0], "logrank_p_value":p_value, "max_time": max_time})
    # print(f"result_list: {result_list}")
    str_colmns = ','.join(stage_list)
    # 2d result list to df
    df = pd.DataFrame.from_dict(result_list)
    ## correction part
    df["FDR"] = multipletests(df["logrank_p_value"].values.tolist(),alpha=1, method= "fdr_bh")[1]
    df["Bonferroni"] = multipletests(df["logrank_p_value"].values.tolist(),alpha=1, method= "bonferroni")[1]
    if cor_method == "None":
        df = df[df["logrank_p_value"] <= input_pvalue].reset_index(drop=True)
    else:
        df = df[df[cor_method] <= input_pvalue].reset_index(drop=True)
    result_list = df.to_dict('records')
    return df, result_list
    # return JsonResponse({"result": result_list})

## function for multiprocessing star map
def process_data(data, low_percent, high_percent, input_pvalue, result_list):
    p_value, max_time = organize_and_cal_pvalue(data, low_percent, high_percent)
    # if p_value <= float(input_pvalue):
    result_list.append({"name": data[0], "logrank_p_value": p_value, "max_time": max_time})

def miRNAscreener_getdata(miRNA_list: list, set_operation: str) -> list:
    cursor = connections['default'].cursor()
    sql_command = ""
    if len(miRNA_list) <= 1:
        sql_command = f'SELECT DISTINCT mirna_name,gene_name FROM Homo_sapiens_miRNA WHERE mirna_name = "{miRNA_list[0]}";'
    else:
        for i in range(len(miRNA_list)):
            if i != 0:
                sql_command += f" UNION "
            sql_command += f'SELECT mirna_name,gene_name FROM Homo_sapiens_miRNA WHERE mirna_name = "{miRNA_list[i]}"'
    print(sql_command)
    cursor.execute(sql_command)
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    result_list = [dict(zip(columns, row)) for row in rows]
    if set_operation == "INTERSECT":
        df = pd.DataFrame(result_list)
        counts = df['gene_name'].value_counts()
        df = df[df['gene_name'].isin(counts[counts == len(miRNA_list)].index)]
        df.to_csv("test.csv", index=False)
        df = df[['gene_name']]
        df.drop_duplicates(inplace=True)
        result_list = df.to_dict('records')
    elif set_operation == "UNION":
        df = pd.DataFrame(result_list)
        df['value'] = 1
        # df.to_csv("test.csv", index=False)
        # 使用 pivot_table 將資料表進行轉換
        df = df.pivot_table(index='gene_name', columns='mirna_name', values='value', fill_value=0).reset_index()
        # 重新排序欄位
        df = df.sort_values(by='gene_name').reset_index(drop=True)
        # 將 0 與 1 轉換成 o 與 x
        df.iloc[:, 1:] = df.iloc[:, 1:].applymap(lambda x: 'o' if x == 1 else 'x')
        result_list = df.to_dict('records')
        # result.to_csv("test.csv", index=False)
    elif set_operation == "DIFFERENCE":
        df = pd.DataFrame(result_list)
        df.drop_duplicates(subset=['gene_name'], keep=False, inplace=True)
        df = df[df["mirna_name"] == miRNA_list[0]]
        # df.to_csv("test.csv", index=False)
        df = df[['gene_name']]
        result_list = df.to_dict('records')
    cursor.close()
    return result_list

def DEscreener_getdata(DE_level: str, primary_site: str, project: str, DE_filter:list) -> list:
    condition1 = DE_filter[0].split('|')[0]
    condition2 = DE_filter[1].split('|')[0]
    condition1_count = DE_filter[0].split('|')[2]
    condition2_count = DE_filter[1].split('|')[2]
    FC_select = DE_filter[2].strip()
    FC_input = DE_filter[3].strip()
    TEST_select = DE_filter[4]
    TESTstates_select = DE_filter[5].split(' (')[0].strip()
    cor_method = DE_filter[6].strip()
    TEST_input = DE_filter[7].strip()
    FC_input = float(FC_input) if FC_input else FC_input
    TEST_input = float(TEST_input) if TEST_input else TEST_input
    stage_to_num_dict = {
        'normal' :'n',
		'stage i' : '1',
		'stage ii' : '2',
		'stage iii' : '3',
		'stage iv' : '4',
	}
    table_name_cuffdiff = "%s_%s_%s_%s"%(project,stage_to_num_dict[condition1],stage_to_num_dict[condition2],DE_level)
    print(table_name_cuffdiff)
    print(f"TESTstates_select: {TESTstates_select}")
    if TESTstates_select == "Greater":
        # "Greater (Condition2 > Condition1)"
        TEST_column = "%s_%s"%(TEST_select.replace(' ','_'),"greater")
    else: # "Less (Condition2 < Condition1)"
        TEST_column = "%s_%s"%(TEST_select.replace(' ','_'),'less')    
    if cor_method == "FDR": 
        TEST_column += "(fdr_bh)"
    elif cor_method == "Bonferroni":
        TEST_column += "(bonferroni)"
    print(TEST_column)
    DE_df = pd.read_csv(f"{current_path}/../static/data/DE_data/{stage_to_num_dict[condition1]}_{stage_to_num_dict[condition2]}corr_test_result_web_ver.csv")
    # print(DE_df[DE_df["foldchange"] == np.inf])
    ## filter by q-value
    if TEST_input != '':
        DE_df = DE_df[DE_df[TEST_column] <= TEST_input]
    else: 
        pass
    ## filter by foldchange
    DE_df = DE_df[DE_df["foldchange"] >= 0.001]
    if FC_select == '≥':
        DE_df = DE_df[(DE_df["foldchange"] >= FC_input) & (DE_df["foldchange"] != np.inf)]
    elif FC_select == '≤':
        DE_df = DE_df[(DE_df["foldchange"] <= FC_input) & (DE_df["foldchange"] != np.inf)]
    else:
        pass
    DE_df = DE_df[['gene_name',TEST_column, 'avg_f_FPKM', 'avg_s_FPKM', 'foldchange']]
    DE_df['foldchange'] = DE_df['foldchange'].round(5)
    DE_df.replace(np.inf, '-', inplace=True)
    
    # print(DE_df["foldchange"].values.tolist())
    # diff_data,download_table_data, table_column = Filter.filter_logFC_Pvalue(TEST_column,table_name_cuffdiff,FC_select,FC_input,TEST_input,DE_level)
    if len(DE_df) != 0:
        return DE_df.values.tolist(), list(DE_df.columns), TEST_column
    else:
        return [], list(DE_df.columns), TEST_column