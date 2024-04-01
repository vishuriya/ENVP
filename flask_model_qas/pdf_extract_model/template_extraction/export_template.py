import json
import pandas as pd
from pdf_extract_model.language_currency.get_language_database import get_database
from pdf_extract_model.language_currency.detect_invoice_currency import search_currency
from pdf_extract_model.template_extraction.mg_dict import fetch
from pdf_extract_model.date_time.get_date_time_instance import get_date_time
from pdf_extract_model.database_connection.database_connect import database_conn
import re
import numpy as np


def single_currency_calculate(amount):
    if amount.count(',') == 1:
        if amount[-3] == ',':
            amount = amount.replace(',' , '^')
            idx = amount.index('^')

            if amount[0:idx].count('.') > 0:
                amount = amount.replace('.' ,',')

    amount = amount.replace('^','.')

    return amount



def currency_calculate(list_of_amount):
    for i in range(len(list_of_amount)):
        if list_of_amount[i].count(',') == 1:
            if list_of_amount[i][-3] == ',':
                list_of_amount[i] = list_of_amount[i].replace(',' , '^')
                idx = list_of_amount[i].index('^')
                
    
                if list_of_amount[i][0:idx].count('.') > 0:
                    list_of_amount[i] = list_of_amount[i].replace('.' , ',')
                    
                
 
        list_of_amount[i] = list_of_amount[i].replace('^' , '.')

 
    return list_of_amount


def get_sum_column(df,col_name):
    no_space_values = []
    new_no_space_list = []
    list_of_values = df[col_name].to_list()
    new_list_of_values = [x for x in list_of_values if str(x) != 'nan' and str(x) != '']
    # print(f'The list of values of {col_name} is {new_list_of_values}')
    for j in new_list_of_values:
        no_space_values.append(j.strip())

    for i in range(len(no_space_values)):
        match_values = re.search(r'[+-]?\d*[\'.,]?\d+[.,]?\d+' , no_space_values[i])
        if match_values != None:
            new_no_space_list.append(match_values.group())

    # print(f'The list of values of {col_name} is {new_no_space_list}')
    calculate_currency_numbers = currency_calculate(new_no_space_list)

    for i in range(len(calculate_currency_numbers)):
        calculate_currency_numbers[i] = calculate_currency_numbers[i].replace(',','')
        calculate_currency_numbers[i] = calculate_currency_numbers[i].replace("'",'')
    # print(f'The list of values of {col_name} is {calculate_currency_numbers}')

    float_list_values = [float(ele_amount) for ele_amount in calculate_currency_numbers]
    result_in_float = sum(float_list_values)
    

    return result_in_float

def get_value_after_decimal(value_in_float):
    x = value_in_float
    print(f' x :{x}......................................9:47')
    y = round(value_in_float)
    print(f'y : {y}.......................................9:48')
    value_after_decimal = str(round(abs(x - y) , 2))
    return value_after_decimal

def calculating_df_parameters(df,size,currency):
    total_tax_amount = get_sum_column(df,'Tax Amount')
    total_amount = get_sum_column(df,'Amount')
    total_discount_amount = get_sum_column(df,'Discount Amount')
    total_invoice_amount = total_amount+total_tax_amount-total_discount_amount

    print(f'total discount amount {total_discount_amount}')
    # round_off = get_value_after_decimal(total_invoice_amount)

    print(f'Total invoice amoiunt {total_tax_amount}.....................17:13')

    print(f'Calculated Total Invoice Amount is {total_invoice_amount}')
   
    if df['Total Invoice Amount'][0] == 'None':
        print('Total Invoice Amount is empty')
        for i in range(size):
            df['Total Invoice Amount'][i] = str(float(format(total_invoice_amount , '.2f')))
            # print('DF Value',df['Total Invoice Amount'][i])

    
    if df['Roundoff'][0] == 'None':
        print("Total Roundoff is empty")
        if str(format(total_invoice_amount,'.2f')) == df['Total Invoice Amount'][0]:
            print('Total Invoice Amount and calculated amount is equal')
            round_off = '0.00'
        else:
            round_off = get_value_after_decimal(total_invoice_amount)

        for i in range(size):
            df['Roundoff'][i] = round_off



    if df['Total Tax Amount'][0] == 'None':
        for i in range(size):
            df['Total Tax Amount'][i] = str(format(total_tax_amount , '.2f'))

       

    for i in range(size):    
        df['Itemno'][i] = str(format(i+1))
        df['Currency'][i] = currency

    tia = df['Total Invoice Amount'][0]
    ro = df['Roundoff'][0]
    tta = df['Total Tax Amount'][0]
    tr = df['Tax %'][0]
    print(f'Total Invoice Amount is {tia}')
    print(f'Total Roundoff value is {ro}')
    print(f'Total Tax Amount is {tta}')
    
    


    print("HSN Code : ",str(df['HSN/SAC Code'][0]))
    print(type(df['HSN/SAC Code'][0]))

    if str(df['HSN/SAC Code'][0]) != 'nan' :

        for i in range(len(df['HSN/SAC Code'])):
            df['HSN/SAC Code'][i] = re.sub(r"\s+", "", df['HSN/SAC Code'][i], flags=re.UNICODE)
            print(df['HSN/SAC Code'][i])
    
    return df



def convert_stringlist_to_intlist(p_list):
    list_int = p_list.strip('][').split(', ')
    for l in range(0 , len(list_int)):
        list_int[l] = int(list_int[l])

    return list_int

def get_start_end(page_list):
    if len(page_list) == 1:
        start = page_list[0]
        end = page_list[0]
    else:
        start = page_list[0]
        end = page_list[-1]


    return start,end


def filtering_requests(req):
    for i in range(len(req)):
        for j in range(len(req[i])):
            for k in range(len(req[i][j])):
                req[i][j][k] = req[i][j][k].strip()
                req[i][j][k] = req[i][j][k].replace("  "," ")
                # req[i][0][k] = req[i][0][k].encode("ascii" , "ignore")
                # req[i][0][k] = req[i][0][k].decode()
                req[i][0][k] = req[i][0][k].capitalize()
    print("Request Filtering Done.......................100%")
    return req

def combine_dataframe(df_h , df_i):
    df = pd.concat([df_h.reset_index(drop=True), df_i.reset_index(drop=True)], axis=1)
    return df

def get_empty_cols(df):
    try:
        no_of_nan = int(len(df.iloc[0]) - df.iloc[0].count())
        no_of_none = int(df.iloc[0].str.count('None').sum())
    except:
        no_of_nan = len(df.columns)
        no_of_none = 0
    
    empty_cols_count = no_of_nan + no_of_none

    return empty_cols_count



def insert_database(date, time, pdf_name,header_details,start, end, pdf_data, excel_name, excel_data, checksum,structure,emptycols,total_cols,filled_cols,str_list):
    
    cursor,conn = database_conn()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS log_table (log_id INTEGER PRIMARY KEY ,date TEXT , time TEXT, pdf_name TEXT,header_details TEXT, start TEXT , end TEXT ,pdf_data TEXT, excel_name TEXT, excel_data TEXT , checksum TEXT, structure TEXT, emptycols TEXT,total_cols TEXT,filled_cols TEXT, str_list TEXT) """)
    cursor.execute(""" INSERT INTO log_table (date,time,pdf_name,header_details, start , end, pdf_data,excel_name,excel_data,checksum,structure,emptycols,total_cols,filled_cols,str_list) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """, (date,time,pdf_name,header_details,start,end,pdf_data,excel_name,excel_data,checksum,structure,emptycols,total_cols,filled_cols,str_list))
    conn.commit()
    cursor.close()
    conn.close()
    print("Data Inserted Successfully")


def clean_digit(raw_element):
    # get_digit = re.search(r'[+-]?\d*[\'.,]?\d+[.,]?\d+',raw_element)
    get_digit = re.search(r'[+-]?\d*[\'.,]?\d*[.,]?\d+',raw_element)
    try:
        raw_element = single_currency_calculate(get_digit.group())
    except:
        raw_element = '0.00'
    raw_element = raw_element.replace(',','')
    raw_element = raw_element.replace("'",'')
    raw_element = float(raw_element)

    return raw_element

def calculate_tax_rate_amount(df):

    for i in range(len(df)):

        if str(df['Tax Amount'][i]) == 'nan':


            if str(df['Tax %'][i]) != 'nan':
                tax_rate = clean_digit(df['Tax %'][i]) # returns float
                amount = clean_digit(df['Amount'][i])
                tax_amount = (tax_rate/100)*amount
                # print(f'the value of tax rate is {tax_rate}')
                # print(f'the value of amount is {amount}')
                print(f'the tax amount is {tax_amount}')
                df['Tax Amount'][i] = str(format(tax_amount , '.2f'))
            else:
                if(str(df['CGST %'][i]) != 'nan' and str(df['SGST %'][i]) != 'nan'):
                    print('1 st condition.................................')
                    amount = clean_digit(df['Amount'][i])
                    cgst = clean_digit(df['CGST %'][i])
                    sgst = clean_digit(df['SGST %'][i])
                    print(f'CGST..........................{cgst}')
                    print(f'SGST..........................{sgst}')


                    try:
                        tcs = clean_digit(df['TCS %'][i])
                    except:
                        tcs = 0.00

        

                    total_tax_rate = cgst + sgst + tcs
                    print(f'Total tax rate is {total_tax_rate}')
                        
                    df['Tax %'][i] = str(format(total_tax_rate , '.2f'))
                    if df['Roundoff'][0] == 'None':
                        df['Tax Amount'][i] = str(format(round((total_tax_rate/100) * amount) , '.2f'))
                        print('................................... Round off............................................. ')
                    
                    else:
                        df['Tax Amount'][i] = str(format((total_tax_rate/100) * amount , '.2f'))
                    df['Tax Description'][i] = 'CGST, SGST/UTGST'
                    
                elif(str(df['CGST %'][i]) != 'nan' and str(df['SGST %'][i]) == 'nan'):
                    print('2 nd condition.................................')
                    amount = clean_digit(df['Amount'][i])
                    cgst = clean_digit(df['CGST %'][i])
                    sgst = cgst

                    try:
                        tcs = clean_digit(df['TCS %'][i])
                    except:
                        tcs = 0.00

                    total_tax_rate = cgst + sgst + tcs
                    df['Tax %'][i] = str(format(total_tax_rate , '.2f'))
                    df['Tax Amount'][i] = str(format((total_tax_rate/100) * amount , '.2f'))
                    df['Tax Description'][i] = 'CGST, SGST/UTGST'
                    
                elif(str(df['CGST %'][i]) == 'nan' and str(df['SGST %'][i]) != 'nan'):
                    print('3rd condition.................................')
                    amount = clean_digit(df['Amount'][i])
                    sgst = clean_digit(df['SGST %'][i])
                    cgst = sgst

                    try:
                        tcs = clean_digit(df['TCS %'][i])
                    except:
                        tcs = 0.00

                    total_tax_rate = cgst + sgst + tcs
                    df['Tax %'][i] = str(format(total_tax_rate , '.2f'))
                    df['Tax Amount'][i] = str(format((total_tax_rate/100) * amount , '.2f'))
                    df['Tax Description'][i] = 'CGST, SGST/UTGST'    

                elif(str(df['CGST %'][i]) == 'nan' and str(df['SGST %'][i]) == 'nan'):
                    print('4th condition.................................')
                    amount = clean_digit(df['Amount'][i])
                    try:
                        tcs = clean_digit(df['TCS %'][i])
                    except:
                        tcs = 0.00

                    try : 
                        gst = clean_digit(df['GST %'][i])
                    except:
                        gst = 0.00


                    total_tax_rate = gst + tcs    
                    df['Tax %'][i] = str(format(total_tax_rate , '.2f'))
                    df['Tax Amount'][i] = str(format((total_tax_rate/100) * amount , '.2f'))
                    df['Tax Description'][i] = 'IGST'



                else:
                    print('No Tax Amount Found')
                    print(' No tax Rate Found')





        if str(df['Tax Amount'][i]) != 'nan':
            if str(df['Tax %'][i]) == 'nan':
                tax_value = clean_digit(df['Tax Amount'][i])
                amount = clean_digit(df['Amount'][i])
                try:
                    tax_rate_value = (tax_value/amount)*100
                except:
                    tax_rate_value = '0.00 %'
                df['Tax %'][i] = str(format(tax_rate_value,'.2f'))
                df['Tax Description'][i] = 'IGST'


        tr = df['Tax %'][i]
        print(f' Tax Rate of {i} is {tr}')


        

    return df


    

def send_all_to_template(pdf_file_name,req, no_of_tables,header_details,page_list,checksum,structure_type,language):

    # fill the pdf data
    pdf_data_json = json.dumps(req)

    # taking page list as an input and converting it into integer
    
    page_list_int = convert_stringlist_to_intlist(page_list)

   # get the page number
    start,end = get_start_end(page_list_int)
    
    # filter the data 
    req = filtering_requests(req)

    print(f'The language coming from dropdown is {language}')

    print(req)

    template_header,dict_of_val = get_database(req,language)

    no_of_cols = 0
    # Making ficticious header to insert into the final DF
    for i in range(no_of_tables):
        no_of_cols += len(req[i][0])

    ficticious_header = template_header
    tem_header = template_header
    for i in range(no_of_cols):        
        val = ''
        val += "No_header_"
        val += str(i)
        ficticious_header.append(val)
    
    cur_row = 0
    indices = []
    for i in range(no_of_tables):
        x = list(range(cur_row, cur_row+len(req[i])))
        indices += x
        cur_row += len(req[i])
    indices.append(len(indices))


    # Making a final dataframe to insert all the data
    df_final = pd.DataFrame(index=indices,columns = ficticious_header)

    def add_to_final():
        for m in range(0, len(col_to_be_transported)):
            df_updated_list = pd.DataFrame(l_of_l)
            l = df_updated_list[col_to_be_transported[m][0]].values.tolist()
            l = l[1:]

            for i in range(cur_index, cur_index+len(l_of_l)-1):
                df_final.at[i, ficticious_header[col_to_be_transported[m][1]]] = l[i-cur_index]
            

    # Sending list by list to fetch to get proper DF
    cur_index = 0
    no_header_count = 0
    for i in range(no_of_tables):
        cur_index, col_to_be_transported, l_of_l = fetch(df_final, cur_index, dict_of_val, req[i], no_header_count, indices, ficticious_header)
        add_to_final()
        cur_index = cur_index + len(req[i])


    df_temp = df_final.iloc[:,:len(dict_of_val.keys())]
    df_garbage = df_final.iloc[:,len(dict_of_val.keys()):]
    
    df_temp.to_excel('excel_files/final_template.xlsx')  # into the main template
    df_garbage.to_excel("excel_files/final_garbage.xlsx") # into the garbage where all the non matched columns are there
    df_final.to_excel("excel_files/final_all_out.xlsx")  # into the final where all the matched and non matched values are there

    df_i = df_temp.copy()

    df_i.dropna(axis=0,how="all",inplace=True)
    size = len(df_i)

    res = [ele for ele in header_details[1:] for i in range(size)]
    df_h = pd.DataFrame(res , columns=header_details[0])
    print('88888888888888888888888888888888888888888888888888888888 Before editing 888888888888888888888888888888888888888888888888888888888')
    
    # df = calculate_tax_rate_amount(df)
    print(df_i)



    # df_i = df_i[['Itemno','Item Description','HSN/SAC Code','Quantity','Unit','Rate','Amount','Currency','Discount %','Discount Amount','Tax %','Tax Amount','Tax Description']]
    
    try:
        df_h = df_h.rename(columns={'Sr.No':'Document Nature'})
    except:
        df_h = df_h
    
    df = combine_dataframe(df_h , df_i)
    print("***********************************************************************************************************************************")
    print(df_h)
  

    print(df_i) 


    # Calculating Currency
    currency = search_currency(req,language)

    # Perform Calculations of total amount and tax amount
    df = calculate_tax_rate_amount(df)
    df = calculating_df_parameters(df,size,currency)

    


    df = df[['Document Nature','External Invoice No','External Invoice Date','Original Invoice reference','Purchase Order no','Purchase Document Date','Total Invoice Amount','Total Tax Amount','Roundoff','Vendor Name','Vendor Address','Vendor GSTIN','Vendor PAN','BillTo Name','BillTo Address','Bill to GSTN','ShipTo Name','ShipTo Address','Ship to GSTN','Vehicle No','Payment Terms','Reference1','Reference2','Reference3','Itemno','Item Description','HSN/SAC Code','Quantity','Unit','Rate','Amount','Currency','Discount %','Discount Amount','Tax %','Tax Amount','Tax Description']]

    df_export_template = df
    df.to_excel('integrated_header_template.xlsx',index=False)

    print("Exporting to template...............................................................................100%")

    # get insights of the cont of data
    empty_cols = get_empty_cols(df)
    emptycols = str(empty_cols)

    # get total number of columns
    total_cols = str(len(df.columns))

    # get the filled columns
    filled_cols = str(len(df.columns)-empty_cols)

    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DF <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print(df)
    list_of_missing_columns = []
    for i in range(len(df.columns)):
        # print(df.iloc[0][i],type(df.iloc[0][i]))

        if df.iloc[0][i] == 'None':
            list_of_missing_columns.append(df.columns[i])

    for i in df.columns[df.isnull().any()].tolist():
        list_of_missing_columns.append(i)

    print(list_of_missing_columns)

    str_list = ', '.join(list_of_missing_columns) + ' not found. '

    print(str_list)

        
    





    
        







                # if df[i][j] == 'None' or df[i][j] == np.nan:
            #     print(df.columns[i])


    # ****************************** Database operation *************************

    # Date Time operation done
    dateStr,timeStr = get_date_time()


    # Getting pdf name
    pdf_file_name = pdf_file_name
    print("PDF FILE DATA : ", pdf_file_name)


    # Getting Header Details

    header_details_json = json.dumps(header_details)
    # print(header_details_json)


    # Getting PDF Data
    

    # Getting Excel name
    excel_file_name = pdf_file_name.rstrip('.pdf') + ".xlsx"
    print("Excel File Name", excel_file_name)


    # Getting Excel data
    df_export_json = df_export_template.to_json()
    
    # Getting CheckSum
    checksum = checksum

    # Insering the structure
    if structure_type == '1':
        structure = 'stream'
    else:
        structure = 'lattice'

    
    insert_database(date=dateStr , time = timeStr , pdf_name = pdf_file_name,header_details = header_details_json, start = start, end = end, pdf_data = pdf_data_json, excel_name = excel_file_name, excel_data = df_export_json, checksum=checksum,structure =structure,emptycols=emptycols,total_cols = total_cols,filled_cols=filled_cols,str_list = str_list)

         

   
    return "Done"

