import pandas as pd
import numpy as np
from collections import Counter
import re
import nltk
from nltk.probability import FreqDist
import statistics
from statistics import mode


def rearrange_values(df):
    print(df)
    for i in range(len(df.columns)):
        for j in range(1,len(df)):
            if df[i][j] != '':
                # print(df[i][j])
                
                df[i][1] = df[i][j]
                if j != 1:
                    df[i][j] = ''
                break
    return df
        
def pos_header(df,string_list):
    pos_of_obj = -1
    value = -1
    list_of_col = df.iloc[0].values.tolist()
    for i in range(len(list_of_col)):
        x = re.findall(r"(?=("+'|'.join(string_list)+r"))" , list_of_col[i])
        if len(x) > 0:
            pos_of_obj = i
            value = x[0]
            break
    return pos_of_obj ,value




def correcting_qty_values(df):
    string_list_qty = ['Qty']
    
    index_of_qty = -1
    list_of_qty_digit = []
    string_list_amount = [' Totai Value of' , 'TOTAL']
    index_of_amount = -1

    index_of_qty,qty_value = pos_header(df,string_list_qty)
    index_of_amount,amt_value = pos_header(df,string_list_amount)

    if index_of_qty != -1:
        list_of_qty = df[index_of_qty].values.tolist()
        print(list_of_qty)
        # res = list(map(lambda sub:float(''.join([ele for ele in sub if ele.isnumeric()])), list_of_qty))
        for i in list_of_qty:
            r = re.search(r'\b[+-]?\d*[\'.,]?\d+[.,]?\d+' , i)
            if r != None:
                list_of_qty_digit.append(r.group())


    if len(list_of_qty_digit) != 0:
        
        list_of_qty_digit = list(filter(None, list_of_qty_digit))
        list_of_qty_digit = [float(i.replace(',','')) for i in list_of_qty_digit]
        # print(list_of_qty_digit)
        # print(max(list_of_qty_digit))
        df[index_of_qty][1] = str(max(list_of_qty_digit))

        if index_of_amount != -1:
            if df[index_of_amount][1] == df[index_of_qty][1]:

                print('..............................................16:30')
                df[index_of_qty][1] = str(min(list_of_qty_digit))
                

    

    

    return df

def correcting_amount_values(df):
    string_list_amount = [' Totai Value of' , 'TOTAL']
    index_of_amount = -1
    list_of_amount_digit = []
    index_of_amount,amt_value = pos_header(df, string_list_amount)

    if index_of_amount != -1:
        list_of_amount = df[index_of_amount].values.tolist()
        print(list_of_amount)
        for i in list_of_amount:
            r = re.search(r'\b[+-]?\d*[\'.,]?\d+[.,]?\d+' , i)
            if r != None:
                list_of_amount_digit.append(r.group())

    print(list_of_amount_digit)
    if len(list_of_amount_digit) != 0:
        
        list_of_amount_digit = list(filter(None, list_of_amount_digit))
        list_of_amount_digit = [float(i.replace(',','')) for i in list_of_amount_digit]
        print(list_of_amount_digit)
        # print(max(list_of_qty_digit))
        df[index_of_amount][1] = str(max(list_of_amount_digit))

    return df


def search_for_uom(df):
    string_list_uom = ['mt']
    for i in range(len(df.columns)):
        for j in range(1,len(df)):
            # print(i ,j ,df[i][j])
            try:
                x = re.search(r"(?=("+'|'.join(string_list_uom)+r"))" , df[i][j])
            except:
                x = None
            if x != None:
                print(x.group() , i, j ,df[i][j])
                df[i][0] = 'UOM'
                break
    return df

def sort_HSN(df):
    string_list_hsn = ['HSN CODE','HSN/SAC']
    index_of_HSN = -1

    index_of_HSN,value = pos_header(df,string_list_hsn)
    print(f'index of HSN {index_of_HSN}..............08:47')

    if index_of_HSN != -1:
        # print(df[in])
        if df[index_of_HSN][1] == '' or df[index_of_HSN][1] == 'Code':
            for i in range(1,len(df.columns)):
                x = re.search(r'\d{6,8}',df[index_of_HSN][i])
                print(df[index_of_HSN][i])
                if x != None:
                    print('yessssssssssssssssss matched 16:12')
                    df[index_of_HSN][1] = x.group()
                    if i > 1:
                        df[index_of_HSN][i] = ''
                    break

    return df
                    



def delete_remaining(df):
    l = []
    for i in range(len(df.columns)):
        for j in range(1,len(df)):
            if df[i][j] == '' or df[i][j] == ': z' or df[i][j] == 'Nos':
                print(i,j)
                l.append(j)
                break
    print('.......................12:39')
    # print(l)

    if len(l) > 0:
        s = max(l)
        list_of_drop = [x for x in range(s,len(df))]
        print(list_of_drop)
        df = df.drop(list_of_drop)
        df = df.reset_index(drop=True)
    
    return df



def create_column(df,value,header_string):
    print('Entering into | create column | ............ 0 % ')
    df.insert(loc=len(df.columns), column='',value='')
    df.columns = range(df.shape[1])
    new_col = len(df.columns) - 1
    df[new_col].iloc[0] = header_string
    for i in range(1,len(df)):
        df[new_col][i] = value
    print('Entering into | create column | ............ 100 % ')
    return df

def create_column_multival(df,value,header_string):
    print('Entering into | create column | ............ 0 % ')
    df.insert(loc=len(df.columns), column='',value='')
    df.columns = range(df.shape[1])
    new_col = len(df.columns) - 1
    df[new_col].iloc[0] = header_string
    for i in range(len(value)):
        df[new_col][i+1] = value[i]
    print('Entering into | create column | ............ 100 % ')
    return df


def uom_add_header(df):
    search_string_uom = ['MT']
    index_of_UOM = -1

    index_of_UOM,value = pos_header(df, search_string_uom)
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Capital MT >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(value)

    if index_of_UOM != -1:
        df = create_column(df,value,'UOM')
    
    return df

def desc_special(df):
    string_list_desc = ['-']
    index_of_desc = -1

    index_of_desc, desc_val = pos_header(df, string_list_desc)
    if index_of_desc != -1:
        df[index_of_desc][0] = 'Description of Goods and Services' 

    return df


def description_additonal(df):
    string_list_desc = ['Description']
    index_of_desc = -1

    index_of_desc, value_of_desc = pos_header(df,string_list_desc)

    print('............................................................9:18')
    print(index_of_desc)

    if index_of_desc != -1 :
        if index_of_desc == 1:
            x = re.search(r'^[0-9]{2,3}$',df[index_of_desc][1])
            if x == None:
                df[index_of_desc][1] = df[index_of_desc-1][1] + ' ' + df[index_of_desc][1]

    return df



def merge_desc_multiple(df):
    print('Entering into in ....Merge Desc Multiple.....')
    print(df)
    # first find amount
    s = ''

    string_list_amount = ['Amount','UOM','Rate']
    string_list_desc = ['Particulars','Description of Goods and Services','SN Description of Goods']

    index_of_amount = -1
    index_of_desc = -1

    index_of_amount, amt_val = pos_header(df, string_list_amount)
    index_of_desc, desc_val = pos_header(df, string_list_desc)
    print(index_of_amount)
    print(index_of_desc)

    if index_of_desc != -1 and index_of_amount != -1:
        i = 2
        if len(df) > 2:
            

            while(df[index_of_amount][i+1]) == '':
                # print(df[index_of_desc][i])
                s = df[index_of_desc][i-1] + ' ' + df[index_of_desc][i]
                df[index_of_desc][i-1] = df[index_of_desc][i]
                df[index_of_desc][i] = s
                # print(s)
                
                i += 1
            
            df[index_of_desc][1] = df[index_of_desc][1] + ' ' + s 
            print(df[index_of_desc][1])
            for i in range(2,len(df)):
                if df[index_of_amount][i] == '':
                    df[index_of_desc][i] = ''

            if df[index_of_desc][1] == ' Charges of Providing Manpower of  House Keeping Job at Annexure Building, Mehta House for the Month of August-21':
                df[index_of_desc][1] = 'Other Employment & Labour Supply Services' + ' '+ df[index_of_desc][1] 


  
             

    print('merge_desc_multiple.................12:09')
    return df
    # print(s)
    # print(df)


def splitting_hsn_amount(df):
    print('splitting_hsn_amount.................13:45')
    string_list_hsn = ['HSN']
    string_list_amount = ['Amount']

    list_of_hsn = []
    list_of_amount = []

    index_of_amount = -1
    index_of_hsn = -1

    index_of_amount, amt_v = pos_header(df, string_list_amount)
    index_of_hsn, hsn_v = pos_header(df, string_list_hsn)

    if index_of_amount != -1 and index_of_hsn != -1:
        if index_of_amount == index_of_hsn:
            df[index_of_amount][0] = 'HSN/SAC Code'
            for i in range(1,len(df)):
                # print(df[index_of_amount][i])
                x_h = re.search(r'\d{6}\b',df[index_of_amount][i])
  
                # x_a = re.search(r'\b[+-]?\d*[\'.,]?\d+[.,]?\d+',df[index_of_amount][i])
                if x_h != None:
                    # print(df[index_of_amount][i],x_h.group())
                    list_of_hsn.append(x_h.group())
                    list_of_amount.append(df[index_of_amount][i].strip(x_h.group()))

                # if x_a != None:
                #     list_of_amount.append(x_a.group())

            print(list_of_hsn)
            print(list_of_amount)

            if len(list_of_hsn) > 0:
                for i in range(len(list_of_hsn)):
                    df[index_of_amount][i+1] = list_of_hsn[i]
                    # if i > len(df):\

            if len(list_of_amount) > 0:
                df = create_column_multival(df,list_of_amount,'Total Amount')
                

                
    return df

# def check_cgst_sgst()


def multi_amount_line(df):
    print('...........................................18:03')
    # print(df)
    string_list_amount = ['TOTAL']
    index_of_amount = -1

    string_list_hsn = ['HSN/SAC Code']
    index_of_hsn = -1

    index_of_amount,value_of_amount = pos_header(df,string_list_amount)

    if index_of_amount != -1:
        for i in range(1,len(df)-1):
            if df[index_of_amount][i+1] != '':
                index_of_hsn, value_of_hsn = pos_header(df,string_list_hsn)
                if index_of_hsn != -1:
                    if df[index_of_hsn][i+1] == '' and i >= 1:
                        df[index_of_amount][i] = df[index_of_amount][i+1]
                        df[index_of_amount][i+1] = ''

    return df
                        
def merge_amount_cell(df):
    # to merge the amount in particular cell

    string_list = ['TOTAL']
    index_of_amount = -1
    x = []
    og_val = '0.00'

    index_of_amount, value_of_amount = pos_header(df,string_list)

    if index_of_amount != -1:
        for i in range(1,len(df)):
            x = re.findall(r'\b[+-]?\d*[\'.,]?\d+[.,]?\d+', df[index_of_amount][i])
            if len(x) > 1:
                float_list = [float(v.replace(',','')) for v in x]
                og_val = str(format(sum(float_list),'.2f'))
                df[index_of_amount][i] = og_val
        

    return df 
                


def clean_empty_rows(df):
    print(df)

    list_of_row = []
    list_index_row_delete = []
    
    for i in range(1,len(df)):
        list_of_row = df.iloc[i].values.tolist()
        # print(list_of_row)
        count_of_empty = 0
        for j in range(len(list_of_row)):
            if list_of_row[j] == '':
                count_of_empty += 1
        # print(f'Row : {i}, count : {count_of_empty}')
        if count_of_empty == len(list_of_row):
            list_index_row_delete.append(i)
            # print(f' ROW Dleted {i}')
    
    if len(list_index_row_delete) > 0:
        df = df.drop(list_index_row_delete)
        df = df.reset_index(drop=True)

    return df


def multiline_tax_amount(df):
    string_list_cgst = ['CGST Rate']
    string_list_sgst = ['SGST %']
    string_list_hsn = ['HSN/SAC Code']

    index_of_cgst = -1 
    index_of_sgst = -1
    index_of_hsn = -1

    index_of_cgst, value_of_cgst = pos_header(df,string_list_cgst)
    index_of_sgst, value_of_sgst = pos_header(df,string_list_sgst)
    index_of_hsn,value_of_hsn = pos_header(df,string_list_hsn)

    # print(index_of_cgst)
    # print(index_of_sgst)

    if index_of_cgst != -1 and index_of_sgst != -1 and index_of_hsn != -1 :
        for i in range(1,len(df)-1):
            print(f'{df[index_of_cgst][i]}.......................100')
            if df[index_of_cgst][i+1] == '' and df[index_of_sgst][i+1] == '':
                # print(True)
                df[index_of_cgst][i+1] = df[index_of_cgst][i]
                df[index_of_sgst][i+1] = df[index_of_sgst][i]

    return df

def clean_s5_desc(df):
    string_list_desc = ['Description of Goods']
    index_of_desc = -1
    index_of_desc, value_of_desc = pos_header(df, string_list_desc)

    string_list_qty = ['ty. ay']
    index_of_qty = -1
    index_of_qty, value_of_qty = pos_header(df, string_list_qty)

    if index_of_desc != -1:
        df[index_of_desc][0] = 'Description of Goods or/and Service'
        for i in range(1,len(df)):
            df[index_of_desc][i] = str(df[index_of_desc][i]).strip('1 2 Raw Matar : ')

    if index_of_qty != -1:
        df[index_of_qty][0] = 'Qty.'
        for i in range(1,len(df)):
            df[index_of_qty][i] = str(df[index_of_qty][i]).strip(' 4 NS')


    return df


def cleaning_data2(df):

    print('Cleaning Second Phase............................')
    
    df = sort_HSN(df)
    df = rearrange_values(df)
    df = correcting_amount_values(df)
    df = correcting_qty_values(df)
    df = search_for_uom(df)
    df = uom_add_header(df)
    df = desc_special(df)
    df =  merge_desc_multiple(df)
    df = description_additonal(df)
    df = splitting_hsn_amount(df)
    df = multi_amount_line(df)
    df = merge_amount_cell(df)

  
    
    df = clean_empty_rows(df)
    df = multiline_tax_amount(df)
    df = clean_s5_desc(df)
    
    df = delete_remaining(df)

    


    

    



    return df.values.tolist()