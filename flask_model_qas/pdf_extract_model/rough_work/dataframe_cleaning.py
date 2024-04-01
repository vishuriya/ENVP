import pandas as pd
import numpy as np
from collections import Counter
import re
import nltk
from nltk.probability import FreqDist
import statistics
from statistics import mode


# to return the list of row index of garbage value rows above the header
def return_match_index_list(df,list_of_words_to_match):
    print('Entering into | return_match_index_list | ............ 0 % ')

    list_of_words = list_of_words_to_match
    list_of_index = []
    for i in range(len(df.columns)):
        for j in range(len(df)):
            for k in list_of_words:

                if df[i].iloc[j].find(k) != -1:
                    list_of_index.append(j)
                    break

    print('Entering into | return_match_index_list | ............ 100 % ')
    return list(set(list_of_index))


# Replacing the escape characters and everything with nan and then again with ""
def replacing_characters_with_nan(df):
    print('Entering into | replacing_characters_with_nan | ............ 0 % ')
    replacing_string = ['','.','on','"|','this Tax Invoice \nin	']
    for i in replacing_string:
        df.replace(i,np.nan,inplace=True)
    df = df.dropna(axis=1, how='all')
    df.replace(np.nan,'', inplace=True)
    df = df.reset_index(drop=True)

    print('Entering into | replacing_characters_with_nan | ............ 100 % ')
    return df


# after rmovng garbage values get the new header
def get_new_headers(df):
    print('Entering into | get_new_headers | ............ 0 % ')
    # Take a transpose of a df
    df_t = df.T

    # Convert all the transpose rows to list
    df_t_list = df_t.values.tolist()

    # Find the first string that encounters
    new_headers = []
    for i in df_t_list:
        for j in i:
            if j != '':
                new_headers.append(j)
                break
    # update the first column with new headers and reset column and row index
    df.iloc[0] = new_headers
    df.reset_index(inplace=True,drop=True)
    df.columns = range(df.shape[1])
    print('Entering into | get_new_headers | ............ 100 % ')

    return df


# Replacing the non identified column with 'Column'
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def replacing_header_with_column(df):
    print('Entering into | replacing_header_with_column | ............ 0 % ')

    # Check for numbers and float value
    for i in df.iloc[0]:
        if isfloat(i):
            print(isfloat(i))
            df.iloc[0]=df.iloc[0].str.replace(i,'Column')

    # Check for alphanumeric numbers
    for i in range(len(df.iloc[0].values.tolist())):
        matchalphanum = re.search('^(?=.*[a-zA-Z])(?=.*[0-9])',df[i].iloc[0])
        if matchalphanum != None:
            print(matchalphanum.group())
            df[i].iloc[0] = df[i].iloc[0].replace(df[i].iloc[0],'Column')

    print('Entering into | replacing_header_with_column | ............ 100 % ')
    return df


# Function to identify something common in a list
def no_of_common(list1,list2):
  list1_as_set = set(list1)
  intersection = list1_as_set.intersection(list2)
  intersection_as_list = list(intersection)

  if len(intersection_as_list) > 0:
    return True

  return False



# Delete the repeated search header
def delete_repeated_header(df):
    print('Entering into | delete_repeated_header | ............ 0 % ')
    list_of_drop = []
    for i in range(0,len(df.columns)):          
        for j in range(1,len(df[i])):
            if( df[i][0] == df[i].iloc[j] ):
                x = df.iloc[j].values.tolist()
                x = list(filter(None,x))
                temp_header = df.iloc[0].values.tolist()
                temp_header.remove(df[i].iloc[j])
                if (len(x) > 1 and no_of_common(x,temp_header) == True) or len(x) == 1 or df[i].iloc[j] == 'CURRENT':
                    list_of_drop.append(j)
                    break

    if len(list_of_drop) != 0:
        list_of_drop = list(set(list_of_drop))
        print(list_of_drop)
        df.drop(list_of_drop,inplace=True)
        df.reset_index(drop=True,inplace=True)                               

    print('Entering into | delete_repeated_header | ............ 100 % ') 
    return df


def find_search_index(df,serial_list):
    print('Entering into | find_search_index | ............ 0 % ')
    search_index = -1
    for i in range(len(df.iloc[0])):
        if(df[i].iloc[0] in serial_list ):
            search_index = i
            break

    print('Entering into | find_search_index | ............ 100 % ')
    return search_index


def get_selected_index(df,search_index):
    print('Entering into | get_selected_index | ............ 0 % ')
    selected_index = []
    df.reset_index(drop=True,inplace=True)
    for i in range(len(df[search_index])):
        if df[search_index].iloc[i] != '' and  (re.search('\d{6}',df[search_index].iloc[i]) == None and  re.search('\d{1}',df[search_index].iloc[i]) != None) :
            selected_index.append(i)

    print('Entering into | get_selected_index | ............ 100 % ')
    return selected_index


def merging_split_row(df,search_index,selected_index):
    print('Entering into | merging_split_row | ............ 0 % ')
    s=0
    for i in range(selected_index[0],len(df[search_index])): #traverse through the search inde column
    
    # keep on merging the rows untill you find the next numer(Fibonacci Series Logic)
        while df[search_index].iloc[i] == '':
            s = df.iloc[i-1] + df.iloc[i]
            df.iloc[i-1] = df.iloc[i]
            df.iloc[i] = s
            break
    
    print('Entering into | merging_split_row | ............ 100 % ')
    return df


# remove empty strings from list
def remove_empty(x):
    print('Entering into | remove_empty | ............ 0 % ')
    y = []
    for i in x:
        if i != '':
             y.append(i)

    print('Entering into | remove_empty | ............ 100 % ')
    return y

# remove the first time duplicate
def remove_duplicate(x):
    print('Entering into | remove_duplicate | ............ 0 % ')
    s = set(x)
    out = []

    for i,z in enumerate(x):
        if z in s:
            out.append(z)
            s.remove(z)
        else:
            break

    out += x[i+1:]

    print('Entering into | remove_duplicate | ............ 100 % ')

    return out

# Function to find HSN column index
def find_indice_HSN(df):
    print('Entering into | find_indice_HSN | ............ 0 % ')
    for i in range(len(df.columns)):
        if(df[i][0].find('HSN') != -1 or df[i][0].find('SAC') != -1 or df[i][0].find('Code') != -1):
            # print(i)
            indice_of_HSN = i
            df[indice_of_HSN].iloc[0] = 'HSN/SAC Code'
            break
        else:
            indice_of_HSN = 0

    print('Entering into | find_indice_HSN | ............ 100 % ')

    return indice_of_HSN

# Function to find Description column index
def find_indice_DESC(df):
    print('Entering into | find_indice_DESC | ............ 0 % ')
    for i in range(len(df.columns)):
  
        if(df[i][0].find('Description') != -1 or df[i][0].find('DESCRIPTION') != -1):
            print(i)
            indice_of_desc = i
            df[indice_of_desc].iloc[0] = 'Description of Goods'
            break

        if(df[i][0].find('Description') == -1):
            indice_of_desc = find_indice_HSN(df)

    print('Entering into | find_indice_DESC | ............ 100 % ')

    return indice_of_desc


# Function to map value and update the dataframe
def map_updated_values(df,i,selected_index,list_of_updated_values):
    print('Entering into | map_updated_values | ............ 0 % ')
    dictionary_for_column = dict(zip(selected_index, list_of_updated_values))
    df[i].update(pd.Series(dictionary_for_column))
    print('Entering into | map_updated_values | ............ 100 % ')


def final_drop_index(df,search_index):
    print('Entering into | final_drop_index | ............ 0 % ')
    final_drop = []
    for i in range(1,len(df[0])):
        if df[search_index].iloc[i] == '' or re.search(r'[0-9]+', df[search_index].iloc[i]) == None:
            # print(i)
            final_drop.append(i)
        
    df = df.drop(final_drop)
    df = df.reset_index(drop=True)

    print('Entering into | final_drop_index | ............ 100 % ')
    
    return df


def end_cleaning(df):
    print(' ------------------------ Dataframe during entering end_claning -------------------------------------------------------------------------------')
    # print(df)
    list_of_rows = []
    list_of_rows_merge = []
    list_of_count_of_row = []
    list_of_df = df.values.tolist()
    string_list = ['Unit','Total' , 'Description','Assessable','Value','Goods', 'Unit','Price','Qty','Quantity','CGST' ,'SGST','Rate','Amount','HSN','IGST','Assessable','Taxable value','SF2USLS','No.']
    for i in range(len(list_of_df)):
        for j in range(len(list_of_df[i])):
            # print(list_of_df[i][j])
            x = re.findall(r"(?=("+'|'.join(string_list)+r"))", list_of_df[i][j])
            if len(x) > 0 :
                print(f'Matched list {x} , row : {i}, column : {j}')
                list_of_rows.append(i)

    try:
        x = mode(list_of_rows)
        # print(x)
    except:
        x = -1

    if x != -1:
            
        list_of_rows_del = []
        for i in range(x+1):
            if i not in list_of_rows:
                list_of_rows_del.append(i)

        # print(list_of_rows_del)

        df = df.drop(list_of_rows_del)
        df = df.reset_index(drop = True)

        # print('After droping them ..............................')
        # print(df)

        next_index = x + 1
        print(f'For the merging of the next index {next_index}')
        for i in range(len(df.columns)):
            y = re.findall(r"(?=("+'|'.join(string_list)+r"))", df[i][next_index])
            # print(df[i][next_index])
            print(y)
            if len(y) > 0:
                list_of_rows_merge.append(y[0])
                

        if len(list_of_rows_merge) > 0:
            for i in range(len(df.columns)):
                df[i][x] = df[i][x] + ' ' + df[i][next_index]
            
            df = df.drop([next_index])
            df = df.reset_index(drop = True)
            # print('Again droppping them ...............................................')
            # print(df)

                

    # print('Merger of the two columns......................')
    # print(df)

    list_of_waste_strings = ['ee' , 'ie', 'of']
    df_list = df.values.tolist()
    list_of_waste_index = []
    list_of_delete_waste_index = []

    for i in range(len(df)):
        y = df_list[i].count('')
        x = len(df_list[i])

        if x - y == 1:
            # print(i)
            list_of_waste_index.append(i)

    for i in list_of_waste_index:
        # print(df_list[i])
        for j in df_list[i]:
            z = re.findall(r"(?=("+'|'.join(list_of_waste_strings)+r"))", j)
            if len(z) > 0:
                list_of_delete_waste_index.append(i)

    print(f'List of delete waste index {list_of_delete_waste_index}')
    # if len(list_of_delete_waste_index) > 0:
    #     df = df.drop(list_of_delete_waste_index)
    #     df = df.reset_index(drop = True)
    #     print(df)

                

        
        

    return df


def search_haeder_tax(df):
    print('Entering into | search_haeder_tax | ............ 0 % ')
    print(df)
    list_of_found = []
    for i in range(len(df.columns)):
        list_of_tax_words = ['CGST' , 'SGST' ,'GST']
        
        # print(df[i].iloc[0])
        x = re.findall(r"(?=("+'|'.join(list_of_tax_words)+r"))", df[i].iloc[0])
        # print(x)
        if len(x) > 0:
            list_of_found.append(x[0])

        # print(list_of_found)
    print('Entering into | search_haeder_tax | ............ 100 % ')
    return list_of_found

def search_haeder_hsn(df):
    print('Entering into | search_haeder_hsn | ............ 0 % ')
    list_of_found = []
    for i in range(len(df.columns)):
        list_of_hsn_words = ['HSN Code']
        
        # print(df[i].iloc[0])
        x = re.findall(r"(?=("+'|'.join(list_of_hsn_words)+r"))", df[i].iloc[0])
        # print(x)
        if len(x) > 0:
            list_of_found.append(x[0])

        # print(list_of_found)
    
    print('Entering into | search_haeder_hsn | ............ 100 % ')

    return list_of_found


def get_HSN(df , list_of_hsn_words):

    print('Entering into | get_hsn | ............ 0 % ')
    
    list_of_hsn_string = []
    list_of_df = df.values.tolist()
    for i in range(len(list_of_df)):
        for j in range(len(list_of_df[i])):
            x = re.findall(r"(?=("+'|'.join(list_of_hsn_words)+r"))", list_of_df[i][j])
            if len(x) > 0:
                list_of_hsn_string.append(list_of_df[i][j])
                pos_of_hsn = i

    # print(f'List of HSN String : {list_of_hsn_string}')

    list_of_hsn = []
    if len(list_of_hsn_string) > 0:
        for i in range(len(list_of_hsn_string)):
            y = re.findall(r'[0-9]+', list_of_hsn_string[i])
            if len(y) > 0:
                list_of_hsn.append(y[0])

    print('Entering into | search_haeder_hsn | ............ 100 % ')
    return list_of_hsn


    




def get_any_tax_value(df, list_of_tax_words):
    print('Entering into | get_any_tax_value | ............ 0 % ')
    value_of_tax = -1
    pos_of_tax = -1
    list_of_tax_string = []
    list_of_df = df.values.tolist()
    for i in range(len(list_of_df)):
        for j in range(len(list_of_df[i])):
            # print(list_of_df[i][j])
            x = re.findall(r"(?=("+'|'.join(list_of_tax_words)+r"))", list_of_df[i][j])
            if len(x) > 0 :
                print(f'Matched TAX {x} , row : {i}, column : {j}')
                
                list_of_tax_string.append(list_of_df[i][j])
                pos_of_tax = i
                


    # print(f'List of Tax strings : {list_of_tax_string}')


    if len(list_of_tax_string) > 0:
        for i in range(len(list_of_tax_string)):
            # x = re.findall(r'[0-9]+' , list_of_tax_string[i])
            x = re.findall(r'\d*\.?\d+' , list_of_tax_string[i])
            print(x)
            if len(x) > 0 :
                shortest = max(x)
                value_of_tax = shortest
                

    print(f'The value of the TAX is {value_of_tax} and pos is {pos_of_tax}')

    print('Entering into | get_any_tax_value | ............ 100 % ')


    return value_of_tax,pos_of_tax


def create_hsn(df,list_of_hsn):
    print('Entering into | get_hsn | ............ 0 % ')
    df.insert(loc=len(df.columns), column='HSN',value='')
    df.columns = range(df.shape[1])
    last_col = len(df.columns) - 1
    df[last_col].iloc[0] = 'HSN/SAC Code'
    
    for i in range(0,len(list_of_hsn)):
        print(list_of_hsn[i])
        df[last_col][i+1] = list_of_hsn[i]

    print('Entering into | get_hsn | ............ 100 % ')

    return df

def create_cgst_sgst(df,cgst,sgst):
    print('Entering into | create_cgst_sgst | ............ 0 % ')
    df.insert(loc=len(df.columns), column='CGST',value='')
    df.columns = range(df.shape[1])
    last_col = len(df.columns) - 1
    df[last_col].iloc[0] = 'CGST %'
    df[last_col][1] = cgst

    df.insert(loc=len(df.columns), column='SGST',value='')
    df.columns = range(df.shape[1])
    last_col = len(df.columns) - 1
    df[last_col].iloc[0] = 'SGST %'
    df[last_col][1] = sgst

    print('Entering into | create_cgst_sgst | ............ 100 % ')
    return df


def create_tcs(df,tcs):
    print('Entering into | create_tcs | ............ 0 % ')
    df.insert(loc=len(df.columns), column='TCS %',value='')
    df.columns = range(df.shape[1])
    last_col = len(df.columns) - 1
    df[last_col].iloc[0] = 'TCS %'
    df[last_col][1] = tcs

    print('Entering into | create_tcs | ............ 100 % ')
    return df

def create_gst(df,gst):
    print('Entering into | create_gst | ............ 0 % ')
    df.insert(loc=len(df.columns), column='GST %',value='')
    df.columns = range(df.shape[1])
    last_col = len(df.columns) - 1
    df[last_col].iloc[0] = 'GST %'
    df[last_col][1] = gst
    print('Entering into | create_gst | ............ 100 % ')
    return df

def insert_hsn(df, list_of_hsn):
    print('Entering into | insert_hsn | ............ 0 % ')
    df_test = df.copy()

    if len(list_of_hsn) > 0 :
        print('HSN Foound........')
        df = create_hsn(df_test ,list_of_hsn)
    else:
        print('HSN was not found')
        df = df_test.copy()

    print('Entering into | insert_hsn | ............ 100 % ')

    return df
    
def insert_cgst_sgst_value(df,cgst,sgst):
    print('Entering into | insert_cgst_sgst_value | ............ 0 % ')
    df_test = df.copy()

    if cgst != -1 and sgst != -1 :
        print('both gst found')
        df = create_cgst_sgst(df_test , cgst ,sgst)
        

    elif(cgst != -1 and sgst == -1):
        print('Not able to find sgst')
        sgst = cgst
        df = create_cgst_sgst(df_test , cgst ,sgst)

    elif (cgst == -1 and sgst != -1):
        print('Not able to find cgst')
        cgst = sgst
        df = create_cgst_sgst(df_test , cgst ,sgst)

    else :
        print('Noting was found')
        df = df_test.copy()

    print('Entering into | insert_cgst_sgst_value | ............ 100 % ')

    return df

def insert_tcs_value(df,tcs):
    print('Entering into | insert_tcs | ............ 0 % ')
    df_test = df.copy()

    if tcs != -1:
        df = create_tcs(df_test,tcs)
        print('TCS was found......')
    else:
        print('TCS was not found')
        df = df_test.copy()

    print('Entering into | insert_tcs | ............ 100 % ')
    return df

def insert_gst_value(df,gst):
    print('Entering into | insert_gst_value | ............ 0 % ')
    df_test = df.copy()

    if gst != -1:
        df = create_gst(df_test,gst)
        print('GST was found......')
        print(gst)
    else:
        print('GST was not found')
        df = df_test.copy()

    print('Entering into | insert_gst_value | ............ 100 % ')
    return df


def splitter(df):
    final_df = pd.DataFrame(index= range(len(df)))

    for j in range(len(df.columns)):
        
        if df[j].str.contains('\n').any():
        
            temp_df = pd.DataFrame()
            temp_df = df[j].str.split('\n', expand=True)
            final_df = pd.merge(final_df, temp_df, left_index=True, right_index=True)
        
            # for i in range(len(temp_df.columns)):
            #     temp_col = temp_df[i]
            #     df.insert(loc = j+i, column = 'col1', value = temp_col)

            final_df.columns = range(0,len(final_df.columns))

        else:
            final_df = pd.merge(final_df, df[j], left_index=True, right_index=True)
            final_df.columns = range(0,len(final_df.columns))
    
    return final_df

def remove_end_repeated_headers(df):
    print('Entering ............................... Remove end repedted headers....................................')
    # print(df)
    string_words_headers = ['Description','Goods','Rate','HSN','Quantity','Price','Value','CGST','SGST','Qty','\nNo.','Particulars','\nDescription  of  Goods  or/and  Service']
    for i in range(len(df.columns)):
        for j in range(len(df)):
            
            x = re.findall(r"(?=("+'|'.join(string_words_headers)+r"))",df[i].iloc[j])

            
            if len(x) > 0 :
                print(f'Got list {x} at cell with value {str(df[i][j])} at position {i,j}')
                if j > 0:
                    df[i][0] = df[i][j]
                    df[i][j] = ''
             
                break
    print('After first loopppp..............12.08')            
    print(df)
    for i in range(len(df.columns)):
        for j in range(len(df) - 1):
            if df[i][0] == df[i][j+1]:
                print(f'The same second element is {str(df[i][j])} at position {i,j}')
                df[i][j+1] = ''
                break

    
    df = df.replace('\n','', regex=True).replace('   ' , '',regex=True).replace('  ',' ' , regex=True)
    list_empty_row_index = []
    df_list = df.values.tolist()
    for i in range(len(df_list)):
        one_s = df_list[i].count('')
        two_s = df_list[i].count(' ')
        # print(i,df_list[i],one_s,two_s)

        if one_s + two_s > len(df_list[i]):
            list_empty_row_index.append(i)
    try:
        print('going in the try block.............................................................................')
        df = df.drop(list_empty_row_index)
        df = df.reset_index(drop = True)
        # print(df)
    except:
        print('going in except block....................................................................')
        df = df.copy()
    


    return df


    
def drop_empty_cols(df):
    print('Entering into | drop_empty_cols | ............ 0 % ')
    # print(df)
    print("############## drop_empty_cols ######################################################")

    list_of_empty_cols = []
    for i in range(len(df.columns)):
        x = len(df[i].values.tolist())
        # print(f'Length of list {x}')
        y = df[i].values.tolist().count('')
        # print(f' Length of empty list {y}')
        if x - y <= 1:
            list_of_empty_cols.append(i)

    try:
        df = df.drop(list_of_empty_cols,axis = 1)
        df = df.reset_index(drop = True)
        
    except:
        df = df.copy()

    # print(df)
    print('Entering into | drop_empty_cols | ............ 100 % ')
    return df

def check_row_digits(df):
    # print(df)
    print("######################################### Entering into Row digits Function #############################################")
    list_of_not_matching_digits = []
    for i in range(len(df.columns)):
        x = re.findall(r'[0-9]+',df[i][1])
        if len(x) <= 0:
            list_of_not_matching_digits.append(i)

    # if len(list_of_not_matching_digits) == len(df.columns):
    #     df = df.drop([1])
    #     df = df.reset_index(drop = True)
        


    print(df)   

    return df

def description_merge(df):
    print('Entering into | description_merge | ............ 0 % ')
    string_list_desc = ['Description of Goods', 'Description']
    string_list_amount = ['Amount', 'Assessable Value' , 'Assessable']
    index_of_desc = -1
    index_of_amount = -1
    flag = 0 
    string =""


    list_of_col = df.iloc[0].values.tolist()

    print(list_of_col)  
    df2 = pd.DataFrame(columns = df.columns)


    #------------------------------------ for Description of goods ----------------------------------------------
    for i in range(len(list_of_col)):
        x = re.findall(r"(?=("+'|'.join(string_list_desc)+r"))" , list_of_col[i])
        print(f'Expected list {x} at col {i}')
        if len(x) > 0:
            index_of_desc = i
            break


    # ----------------------------For Amount ---------------------------------------------
    for i in range(len(list_of_col)):
        x = re.findall(r"(?=("+'|'.join(string_list_amount)+r"))" , list_of_col[i])
        print(f'Expected list {x} at col {i}')
        if len(x) > 0:
            index_of_amount = i
            break
    print("-------------------------------------------------------------------------------------------------")
    # print(df)


    # if index_of_amount != -1:
    #     for i in range(len(df)):
    #         print(f'Row wise {df[i][index_of_amount]}')
    # if index_of_amount != -1:
    #     col_name = index_of_amount        
    #     for i in range(len(df[index_of_amount])):
    #         # print(df[index_of_desc][i])
    #         temp = df[col_name][i]
    #         x = re.findall('[+-]?\d*[\'.,]?\d+[.,]?\d+', temp)
    #         if len(x) > 0:
    #             print("len(x) > 0 {}".format(i))
    #             df2 = df2.append(df.iloc[i])
    #             flag = 1
    #             if index_of_desc != -1:
    #                 string= df[index_of_desc][i]
    #                 loc = i

    #         if flag == 0:
    #             df2 = df2.append(df.iloc[i])
    #         elif len(x) <= 0 and flag == 1:
    #             string = string + " " +  df[index_of_desc][i]
    #             df2[index_of_desc][loc] = string


    print('Entering into | description_merge | ............ 100 % ')

    return df

def rate_repeater(df):
    print("############################ Column Rate Repeating ##################################################")
    list_of_columns = df.iloc[0].values.tolist()
    print(list_of_columns)
    res = [idx for idx, val in enumerate(list_of_columns) if val in list_of_columns[:idx]]
    print(res)

    if len(res) > 0:
        df.drop(df.columns[res], axis = 1, inplace = True)
        df = df.reset_index(drop = True)



    return df


def sort_description(df):
    print('Entering into | sort_description | ............ 0 % ')
    string_list_desc = ['Description of Goods', 'Description','Description of Service']
    string_list_of_serial = ['S.No']
    index_of_desc = -1
    index_of_serial = -1
    list_of_desc = []
    list_of_serial = []
    selected_index = []
    list_of_del = []

    list_of_col = df.iloc[0].values.tolist()

    print('####################################### Found Description ############################################')
    for i in range(len(list_of_col)):
        x = re.findall(r"(?=("+'|'.join(string_list_desc)+r"))" , list_of_col[i])
        print(f'Expected list {x} at col {i}')
        if len(x) > 0:
            index_of_desc = i
            break
    print(f'index of desc {index_of_desc}')


    print('####################################### Found Serial ############################################')
    for i in range(len(list_of_col)):
        x = re.findall(r"(?=("+'|'.join(string_list_of_serial)+r"))" , list_of_col[i])
        print(f'Expected list {x} at col {i}')
        if len(x) > 0:
            index_of_serial = i
            break

    print(f'index of serial {index_of_serial}')


    if index_of_desc != -1 and index_of_serial != -1:
        i=1
        while df[index_of_serial].iloc[i] == '':
            s = df.iloc[i] + df.iloc[i+1]
            df.iloc[i] = df.iloc[i+1]
            df.iloc[i+1] = s
            break

        search_index = index_of_serial
        for i in range(len(df)):
            print(df[search_index].iloc[i])
            if re.search('\d{1}',df[search_index].iloc[i]) != None:
                selected_index.append(i)
        
        print("*********** Selected Index")
        print(selected_index)

        if len(selected_index) > 0 :
            if selected_index[0]-1 != 0:
                df.iloc[selected_index[0]] = df.iloc[selected_index[0]-1] + ' ' + df.iloc[selected_index[0]]

                for i in range(1,selected_index[0]):
                    list_of_del.append(i)

                if len(list_of_del) > 0:
                    df = df.drop(list_of_del)
                    df = df.reset_index(drop=True)


    
    print('Entering into | sort_description | ............ 100 % ')
        


    return df



def final_gst_issue(df):
    print('Entering into | final_gst_issue | ............ 0 % ')
    string_list_cgst = ['CGST']
    string_list_of_igst = ['IGST']
    index_of_cgst = -1
    index_of_igst = -1

    list_of_col = df.iloc[0].values.tolist()
    for i in range(len(list_of_col)):
        x = re.findall(r"(?=("+'|'.join(string_list_cgst)+r"))" , list_of_col[i])
        print(f'Expected list {x} at col {i}')
        if len(x) > 0:
            index_of_cgst = i
            break
    
    if index_of_cgst != -1:
        print('####################################### Found CGST ############################################')
        for i in range(len(list_of_col)):
            x = re.findall(r"(?=("+'|'.join(string_list_of_igst)+r"))" , list_of_col[i])
            print(f'Expected list {x} at col {i}')
            if len(x) > 0:
                index_of_igst = i
                break



            
        if index_of_igst != -1 :
            df.drop(df.columns[[index_of_igst]], axis = 1, inplace = True)
            df = df.reset_index(drop = True)


    print('Entering into | final_gst_issue | ............ 100 % ')

    return df


def sort_cgst_split(df):

    print('Entering into | sort_cgst_split | ............ 0 % ')
    string_list_cgst = ['CGST']
    index_of_cgst = -1

    list_of_col = df.iloc[0].values.tolist()
    print("**********************************************************Pain of splitting CGST*************************************8")
    df.columns = range(df.shape[1])
    for i in range(len(list_of_col)):
        x = re.findall(r"(?=("+'|'.join(string_list_cgst)+r"))" , list_of_col[i])
        print(f'Expected list {x} at col {i}')
        if len(x) > 0:
            index_of_cgst = i
            break

    # print(df)
    if index_of_cgst != -1:

        df[index_of_cgst][0] = 'CGST Rate'

        for i in range(1,len(df)):
            x = re.findall(r'[+-]?[\d]+(?:[\.][\d]+)?[\s]+[+-]?[\d]+(?:[\.][\d]+)?' , df[index_of_cgst].iloc[i])
            print(x)
            if len(x) > 0:
                l = x[0].split()
                if len(l) > 0:
                    x = [float(x) for x in l]
                    
                    print("---------------------")
                    print(x)
                    print(min(x))
                    print("---------------------")

                    df[index_of_cgst].iloc[i] = min(x)




    # print(df)

    print('Entering into | sort_cgst_split | ............ 100 % ')

    return df







def single_currency_calculate(amount):
    print('Entering into | single_currency_calculate | ............ 0 % ')
    if amount.count(',') == 1:
        if amount[-3] == ',':
            amount = amount.replace(',' , '^')
            idx = amount.index('^')

            if amount[0:idx].count('.') > 0:
                amount = amount.replace('.' ,',')

    amount = amount.replace('^','.')

    print('Entering into | single_currency_calculate | ............ 100 % ')

    return amount


def clean_digit(raw_element):
    print('Entering into | clean_digit | ............ 0 % ')
    get_digit = re.search(r'[+-]?\d*[\'.,]?\d+[.,]?\d+',raw_element)
    try:
        raw_element = single_currency_calculate(get_digit.group())
    except:
        raw_element = '0.00'
    
    raw_element = raw_element.replace(',','')
    raw_element = raw_element.replace("'",'')
    raw_element = float(raw_element)
    print('Entering into | clean_digit | ............ 100 % ')
    return raw_element


def add_sgst_cgst(df):
    print('Entering into | add_sgst_cgst | ............ 0 % ')
    string_list_cgst = ['CGST']
    string_list_sgst = ['SGST','Output SGST 9%']
    string_list_amount = ['Taxable value','Service Value','Taxable Value']
    index_of_cgst = -1
    index_of_sgst = -1
    index_of_amount = -1

    list_of_col = df.iloc[0].values.tolist()
    print("**********************************************************Pain of splitting CGST*************************************8")
    df.columns = range(df.shape[1])
    for i in range(len(list_of_col)):
        x = re.findall(r"(?=("+'|'.join(string_list_cgst)+r"))" , list_of_col[i])
        print(f'Expected list {x} at col {i}')
        if len(x) > 0:
            index_of_cgst = i
            break



    
    for i in range(len(list_of_col)):
        x = re.findall(r"(?=("+'|'.join(string_list_amount)+r"))" , list_of_col[i])
        print(f'Expected list {x} at col {i}')
        if len(x) > 0:
            index_of_amount = i
            break



    if index_of_cgst != -1 and index_of_amount != -1:
        df.insert(loc=index_of_cgst + 1, column='CGST Amount',value="")
        
        df.columns = range(df.shape[1])
        df[index_of_cgst+1].iloc[0] = 'CGST Amount'

        for i in range(1,len(df)):
            # print(df[index_of_cgst][i])
            # print(type(df[index_of_cgst][i]))
            cgst = clean_digit(str(df[index_of_cgst][i]))
            amount = clean_digit(str(df[index_of_amount][i]))
            print(amount)
            print(cgst)
            cgst_amount = (cgst/100)*amount
            df[index_of_cgst+1][i] = str(format(cgst_amount , '.2f'))
        

        # print(df)

        list_of_col = df.iloc[0].values.tolist()
        for i in range(len(list_of_col)):
            x = re.findall(r"(?=("+'|'.join(string_list_sgst)+r"))" , list_of_col[i])
            print(f'Expected list {x} at col {i}')
            if len(x) > 0:
                index_of_sgst = i
                break

        if index_of_sgst == -1:
            df.insert(loc=index_of_cgst + 2, column='SGST Rate',value="")
            df.insert(loc=index_of_cgst + 3, column='SGST Amount',value="")

            df.columns = range(df.shape[1])
            df[index_of_cgst+2].iloc[0] = 'SGST Rate'
            df[index_of_cgst+3].iloc[0] = 'SGST Amount'

            for i in range(1,len(df)):
                # print(df[index_of_cgst][i])
                # print(type(df[index_of_cgst][i]))
                cgst = clean_digit(str(df[index_of_cgst][i]))
                amount = clean_digit(str(df[index_of_amount][i]))
                print(amount)
                print(cgst)
                sgst_amount = (cgst/100)*amount
                df[index_of_cgst+2][i] = str(format(cgst , '.2f'))
                df[index_of_cgst+3][i] = str(format(sgst_amount , '.2f'))
            df.columns = range(df.shape[1])

        # for i in range(len(list_of_col)):
        #     x = re.findall(r"(?=("+'|'.join(string_list_sgst)+r"))" , list_of_col[i])
        #     print(f'Expected list {x} at col {i}')
        #     if len(x) > 0:
        #         index_of_sgst = i
        #         break


        if index_of_sgst != -1:
            df.insert(loc=index_of_sgst + 1, column='SGST Amount',value="")
        
            df.columns = range(df.shape[1])
            df[index_of_sgst+1].iloc[0] = 'SGST Amount'

            for i in range(1,len(df)):
                # print(df[index_of_cgst][i])
                # print(type(df[index_of_cgst][i]))
                sgst = clean_digit(str(df[index_of_sgst][i]))
                amount = clean_digit(str(df[index_of_amount][i]))
                print(amount)
                print(sgst)
                sgst_amount = (sgst/100)*amount
                df[index_of_sgst+1][i] = str(format(sgst_amount , '.2f'))


        df.columns = range(df.shape[1])

            
    print('Entering into | add_sgst_cgst | ............ 100 % ')
    
    return df





def discard_fake_discount(df):
    print('Entering into | discard_fake_discount | ............ 0 % ')
    string_list_discount = ['Discount']
    string_list_amount = ['Taxable value','Service Value','Taxable Value']
    index_of_discount = -1
    index_of_amount = -1

    match_count = 0

    list_of_col = df.iloc[0].values.tolist()
    print("********************************************************** Removing Fake Discounts *************************************8")
    df.columns = range(df.shape[1])
    for i in range(len(list_of_col)):
        x = re.findall(r"(?=("+'|'.join(string_list_discount)+r"))" , list_of_col[i])
        print(f'Expected list {x} at col {i}')
        if len(x) > 0:
            index_of_discount = i
            break

    df.columns = range(df.shape[1])
    for i in range(len(list_of_col)):
        x = re.findall(r"(?=("+'|'.join(string_list_amount)+r"))" , list_of_col[i])
        print(f'Expected list {x} at col {i}')
        if len(x) > 0:
            index_of_amount = i
            break



    if index_of_amount != -1 and index_of_discount != -1:
        for i in range(1,len(df)):
            discount_amount = clean_digit(str(df[index_of_discount][i]))
            amount = clean_digit(str(df[index_of_amount][i]))
            print(discount_amount , amount)

            if amount == discount_amount:
                match_count = match_count + 1
        
        print(f'Total Count matches : {match_count}')
        if match_count == len(df)-1:
            df.drop(df.columns[[index_of_discount]], axis = 1, inplace = True)
            df = df.reset_index(drop = True)
            df.columns = range(df.shape[1])

    print('Entering into | discard_fake_discount | ............ 100 % ')
            
    return df




            


def cleaning_data(x):
    df = pd.DataFrame(x)
    print('##################################################### Original Dataframe ############################################################ ')
    print(df)
    print('##################################################### Original Dataframe ############################################################ ')
    # Finding out the garbage values above the header details
    list_of_garbage_words = ['State','PAN  Number' , 'GSTINUIN' 'Tel \nNo. \n:02145-233302/41784','GSTIN','PAN No: AAHFS5211J','Total Amount Before Tax','Total Amount Before tax','Description  of  Packages:','Prices \n1.','TAX - INVOICE U/S. 31 READ WITH RULE M/S SHREERAJ TRADING CO.' , 'Pro. \n: \nB.K. \nGohil \nOffice \n:' , 'Pin \n:  362268','Gujarat  Sidhee  Cement  Ltd.','Recipient Details','TAX  INVOICE  NO.','Value  Rs.','WORKORDER  DATE  :- \n12  AUG  2021','oR 2 Clire a 4 VOM Rii TAXABLE VALUE OF GOODS/','WORKORDER  NO:-  SGJPO00005352122  REVENUE','oR  2  Clire  a \n4 \nVOM  Rii','Reverse  Charge    GST...........2  \nSeveutry','Add : Other Charges thoadey Flupjvex','Add  :  Other  Charges \nthoadey \nFlupjvex', '46,340.00','N  JW \n28673.00','YES  OR  NO','% \nYX','fa \nBio. \nTotal \nNet  Amount','E. \n \nO.E.  Rupees  EIGHTY  EIGHT']
    list_of_garbage_header = return_match_index_list(df,list_of_garbage_words)
    
    print(f'List of garbage words are as follwos : {list_of_garbage_header}')
    

    # drop all the garbage index
    if len(list_of_garbage_header) != 0:
        df.drop(list_of_garbage_header,inplace=True)
        df.reset_index(drop=True,inplace=True)

    # print("# drop all the garbage index")
    print(df)

    # Cleaning and droping some escape chahracters column
    df = replacing_characters_with_nan(df)
    # print("# Cleaning and droping some escape chahracters column")
    print(df)

    # Fetch the headers and update the first row with new headers
    df = get_new_headers(df)
    print("# Fetch the headers and update the first row with new headers")
    print(df)


    # Replacing empty numerical and alphanumerical headers with string 'Column'
    df = replacing_header_with_column(df)
    print("# Replacing empty numerical and alphanumerical headers with string 'Column'")
    print(df)

    # delete the repeated header if found
    df = delete_repeated_header(df)
    print("# delete the repeated header if found")
    print(df)



    # from list of serial_list find the search index(serial number column index)
    serial_list = ['Sr.' , 'Sr.no','ITEM  NO.','SNo HSN NO.','S.No.','Sr.No.']
    search_index = find_search_index(df,serial_list)
    print(f'search index...............12.05 {search_index}')

    if search_index != -1:

        selected_index = get_selected_index(df,search_index)
        print(selected_index)
        df_values = df.copy()

        if len(selected_index) != 0:
            df = merging_split_row(df,search_index,selected_index)

            # after merging update the selected index
            selected_index = []
            for i in range(1,len(df[search_index])):
                if re.search(r'[0-9]+', df[search_index].iloc[i]) != None or df[search_index].iloc[i] != '':
                    selected_index.append(i)
            if len(selected_index) != 0:

                drop_index = []
                for i in range(1,len(df)):
                    if i not in selected_index:
                        drop_index.append(i)

                df = df.reset_index(drop=True)

                df = df.drop(drop_index)


                df = df.reset_index(drop=True)

                # Extract the HSN index
                indice_of_HSN = find_indice_HSN(df)

                # Extract the DESCRIPTION index
                indice_of_DESC = find_indice_DESC(df)




                
                updated_dict_column_idx = max(indice_of_DESC,indice_of_HSN) + 1
                # print(updated_dict_column_idx)
                # print("Description : ",indice_of_DESC)

                list_drop_temp = []
                for i in range(len(df)):
                    x = df.iloc[i].values.tolist()
                    templist = list(filter(None, x))
                    if len(templist) <=1:
                        list_drop_temp.append(i)
                        break
                if len(list_drop_temp) != 0:                
                    df.drop(df.index[list_drop_temp],inplace=True)
                    df.reset_index(drop=True,inplace=True)

                selected_index = [0]
                for i in range(1,len(df[search_index])):
                    if re.search(r'[0-9]+', df[search_index].iloc[i]) != None  and  re.search('\d{6}',df[search_index].iloc[i]) == None  :
                        selected_index.append(i)

                # now map the remaining values according to selected index
                for i in range(updated_dict_column_idx,len(df.columns)):
                    x = df_values[i].tolist()
                    new_df_list = remove_empty(x)
                    if(len(new_df_list)) != len(df) and re.search('[0-9]+',new_df_list[1]) == None and new_df_list[0] != new_df_list[1]:
                        new_df_list[0] = new_df_list[0] + ' ' + new_df_list[1]
                        new_df_list.remove(new_df_list[1])
                    # dictionary_for_column = dict(zip(selected_index,  new_df_list))
                    # print(selected_index)
                    # df[i].update(pd.Series(dictionary_for_column))
                    map_updated_values(df,i,selected_index,new_df_list)

                
                df = final_drop_index(df, search_index)
                selected_index = []
                for i in range(1,len(df[search_index])):
                    if re.search(r'[0-9]+', df[search_index].iloc[i]) != None  and  re.search('\d{6}',df[search_index].iloc[i]) == None :
                        selected_index.append(i)

                list_of_HSN=[]
                list_of_description = []
                list_of_row_index = []
                desc_counter = 0
                for i in range(len(df)):
                    for j in range(0,len(df.iloc[i])):
                        matchObj = re.search( r'\d{6,8}', df[j].iloc[i])
                        if matchObj != None:
                            x = matchObj.group()
                            idx = matchObj.start()
                            y = df[j].iloc[i][:idx]
                            new = df[j].iloc[i].replace(x,'').replace(y,'')
                            list_of_HSN.append(matchObj.group())
                            list_of_row_index.append(i)

                            if new != '':
                                counter = 0
                                list_of_description.append(new)
                                break
                            else:
                                counter = 1
                                break


                # Drop HSN if possible from anyother merge
                for i in range(1,len(df[search_index])):
                    if re.search('\d{6}',df[search_index].iloc[i]) != None :
                        drop_HSN = i


                        df.drop(drop_HSN,inplace=True)
                        df.reset_index(drop=True,inplace=True)
                        break

                if counter == 1:
                    for i in range(1,len(df)):
                        list_of_description.append(df[indice_of_DESC].iloc[i])

                
                if indice_of_DESC == indice_of_HSN:
                    indice_of_DESC = indice_of_HSN + 1
                    df.insert(loc=indice_of_DESC, column='Description',value="random")
                    df.columns = range(df.shape[1])
                    df[indice_of_DESC].iloc[0] = 'Description of Goods'

                if indice_of_HSN == 0:
                    indice_of_HSN = indice_of_DESC + 1
                    df.insert(loc=indice_of_HSN, column='HSN',value="")
                    df.columns = range(df.shape[1])
                    df[indice_of_HSN].iloc[0] = 'HSN/SAC Code'
                # print(list_of_description)

                # Description and hsn updating the df values
                if len(list_of_description) != 0 and len(list_of_HSN) != 0 and len(list_of_row_index) != 0:
                    map_updated_values(df,indice_of_DESC,list_of_row_index,list_of_description)
                    map_updated_values(df,indice_of_HSN,list_of_row_index,list_of_HSN)

                df = df.replace(r'^\s*$', np.nan, regex=True)
                for i in range(len(df.columns)):
                    for j in range(len(df)):
                        df[i].iloc[j] = str(df[i].iloc[j]).strip()
                
                common_ele = []
                for i in range(len(df.columns)):
                    tokenized_word = df[i].tolist()
                    fdist = FreqDist(tokenized_word[1:])
                    common = fdist.most_common(3)
                    # print(common)
                    # print(common[0][0] + " : " + df[i].iloc[0])
                    common_ele.append(common[0][0])
                    
                    df[i] = df[i].replace(str(np.nan),common[0][0])


                # The Whole CGST and SGST problem
                
                for i in range(len(df.columns)):
                    # print(df[i].iloc[0])

                    if(df[i][0].find('CGST') != -1 or df[i][0].find('SGST') != -1):
                        

                        list_of_rate = []
                        list_of_cgst = []
                        list_of_sgst = []
                        list_row_rate_index = []
                        gst_values = ['9.00','9%','9.00%']

                        index_of_gst = []

                        for i in gst_values:
                            for j in range(len(common_ele)):
                                if common_ele[j].find(i) != -1:
                                    # print("J",j)
                                    index_of_gst.append(j)
                                

                        # print(index_of_gst)
                        len_index_of_gst = len(index_of_gst)
                        # print(len_index_of_gst)

                        if len_index_of_gst > 1:
                            df[index_of_gst[0]].iloc[0] = 'CGST'
                            df[index_of_gst[1]].iloc[0] = 'SGST'


                        if len_index_of_gst == 1:
                            df.insert(loc=index_of_gst[0]+2, column='SGST',value="random")
                            df.columns = range(df.shape[1])
                            df[index_of_gst[0]+1].iloc[0] = 'CGST'
                            df[index_of_gst[0]+2].iloc[0] = 'SGST'
                            df[index_of_gst[0]].iloc[0] = 'Rate'
                            df.columns = range(df.shape[1])


                        list_row_gst_index = []
                        list_of_CSR = df[index_of_gst[0]].values.tolist()
                        for i in range(1,len(list_of_CSR)):
                            matchObj = re.search( r'[0-9]+(\.[0-9][0-9]?)?', list_of_CSR[i])
                            
                            # print(matchObj)
                            if matchObj != None:
                                print(matchObj.group())
                                list_row_gst_index.append(i)
                                list_of_cgst.append(matchObj.group())
                                list_of_sgst.append(matchObj.group())
                                list_of_CSR[i] = list_of_CSR[i].replace(matchObj.group(),"")
                                matchObj = re.search( r'[0-9]+(\.[0-9][0-9]?)?', list_of_CSR[i])
                                if matchObj != None:
                                
                                
                                    list_of_rate.append(matchObj.group())
                                    list_row_rate_index.append(i)
                                # break

                        dict_for_CGST = dict(zip(list_row_gst_index,  list_of_cgst))
                        dict_for_SGST = dict(zip(list_row_gst_index,  list_of_sgst))
                        dict_for_rate = dict(zip(list_row_gst_index,  list_of_rate))


                        df[index_of_gst[0]+1].update(pd.Series(dict_for_CGST))
                        df[index_of_gst[0]+2].update(pd.Series(dict_for_SGST))
                        df[index_of_gst[0]].update(pd.Series(dict_for_rate))
                        break

                list_of_DCGST = []
                list_of_DSGST = []
                row_dgst_index = []
                for i in range(len(df.columns)):
                    for j in range(1,len(df)):
                        matchObj = re.search('(\d+(\.\d+)?%)',df[i].iloc[j])
                        if matchObj != None:
                            # print(matchObj.group())
                            idx = matchObj.start()
                            y = df[i].iloc[j][idx:]
                            
                            print(y)
                            df[i].iloc[j] = df[i].iloc[j].replace(y,"")
                            print(df[i].iloc[j])
                            list_of_DCGST.append(matchObj.group())
                            list_of_DSGST.append(matchObj.group())
                            row_dgst_index.append(j)

                if len(list_of_DCGST) > 0:
                    df.insert(loc=indice_of_DESC+2, column='CGST',value="random")
                    df.insert(loc=indice_of_DESC+3, column='SGST',value="random")
                    df.columns = range(df.shape[1])
                    df[indice_of_DESC+2].iloc[0] = 'CGST'
                    df[indice_of_DESC+3].iloc[0] = 'SGST'
                    dict_for_DCGST = dict(zip(row_dgst_index,  list_of_DCGST))
                    dict_for_DSGST = dict(zip(row_dgst_index,  list_of_DSGST))
                    df[indice_of_DESC+2].update(pd.Series(dict_for_DCGST))
                    df[indice_of_DESC+3].update(pd.Series(dict_for_DSGST))

    df = end_cleaning(df)
    print('After End Cleaninng.......................12.06')
    print(df)
    df = remove_end_repeated_headers(df)

    print('After End repeated Header Cleaninng.......................12.07')
    print(df)

    df = check_row_digits(df)
    # string_words_headers = ['Description','Goods','Rate','HSN']
    # for i in range(len(df.columns)):
    #     x = re.findall(r"(?=("+'|'.join(string_words_headers)+r"))",df[i].iloc[j])
    #     print(x)

    # print(df)

    list_of_found_HSN = search_haeder_hsn(df)
    if len(list_of_found_HSN) == 0:
        list_of_hsn_words = ['HSN Code']
        
        list_of_hsn = get_HSN(df,list_of_hsn_words)
        print(f'List of HSN encountered is : {list_of_hsn}')
        df = insert_hsn(df,list_of_hsn)
        print(f' HSN Code : {list_of_hsn} ||')
        print(len(df.columns))
        if len(df.columns) > 6:
            df = df[~df[6].isin(['Z'])]
            df = df.reset_index(drop = True)


   


 
    # list_of_found = []
    list_of_found = search_haeder_tax(df)
    print(f' List of found : {list_of_found}')
    if len(list_of_found) == 0:
        list_of_cgst_words = ['CGST' , 'C-GST','9.00  %','2.50']
        list_of_sgst_words = ['SGST','S-GST','ccs','9.00 %','2.50']
        list_of_tcs_words = ['TCS']
        list_of_gst_words = ['GST Rate']
        cgst,pos_of_cgst = get_any_tax_value(df, list_of_cgst_words)
        sgst,pos_of_sgst = get_any_tax_value(df, list_of_sgst_words)
        tcs,pos_of_tcs  = get_any_tax_value(df,list_of_tcs_words)
        gst,pos_of_gst = get_any_tax_value(df,list_of_gst_words)
        print(f'CGST value : {cgst} || SGST value : {sgst} || TCS Value : {tcs} || GST value : {gst}')
        df = insert_cgst_sgst_value(df, cgst , sgst)
        df = insert_tcs_value(df,tcs)
        df = insert_gst_value(df,gst)
        # print(df)

        deleting_index = -1
        if pos_of_tcs != -1 and pos_of_cgst != -1 and pos_of_sgst != -1:
            deleting_index = min(pos_of_cgst,pos_of_sgst,pos_of_tcs)

        if pos_of_tcs == -1 and pos_of_cgst != -1 and pos_of_sgst != -1:
            deleting_index = min(pos_of_cgst,pos_of_sgst)

        if pos_of_tcs != -1 and pos_of_cgst == -1 and pos_of_sgst != -1:
            deleting_index = min(pos_of_tcs,pos_of_sgst)

        if pos_of_tcs == -1 and pos_of_cgst != -1 and pos_of_sgst == -1:
            deleting_index = min(pos_of_cgst,pos_of_cgst)

        if pos_of_cgst != -1 and pos_of_sgst != -1 and pos_of_gst != -1 and pos_of_tcs != -1:
            deleting_index = min(pos_of_cgst,pos_of_sgst,pos_of_tcs,pos_of_gst) 

        if pos_of_tcs == -1 and pos_of_cgst == -1 and pos_of_sgst == -1:
            deleting_index = -1


        # print(f'Deleting index {deleting_index}')

        
     

        print(f'********************************Just before deleting the index**************************************')
        # print(df)
        list_of_after_tax_index = []
        if deleting_index != -1:
            for i in range(deleting_index,len(df)):
                list_of_after_tax_index.append(i)
            
            try:
                df = df.drop(list_of_after_tax_index)
                df = df.reset_index(drop = True)
            except:
                df = df.copy

        


    df = drop_empty_cols(df)
    print('Drop Empty Column.....................................................................21:16')
    print(df)

    df = description_merge(df)

    df = rate_repeater(df)

    df = sort_description(df)

    df = final_gst_issue(df)

    df = sort_cgst_split(df)

    df = add_sgst_cgst(df)

    df = discard_fake_discount(df)

    # df = splitter(df)
    
    # print(df.values.tolist())
   

    return df.values.tolist()
