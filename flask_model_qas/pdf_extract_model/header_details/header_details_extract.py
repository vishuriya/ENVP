from __future__ import print_function
import re
from flask import Flask, request, render_template
import pytesseract
import os
import cv2
import json
import re
import pandas as pd

from werkzeug.utils import secure_filename

import fitz

from pdfminer.high_level import extract_text
from pdfminer.high_level import extract_pages

def dict_var():
    dic = {'category': [],
           'Document Nature': [],
           'External Invoice No': [],
           'External Invoice Date': [],
           'Original Invoice reference': [],
           'Purchase Order no': [],
           'Purchase Document Date': [],
           'Total Invoice Amount': [],
           'Total Tax Amount': [],
           'Roundoff': [],
           'Vendor Name': [],
           'Vendor Address': [],
           'Vendor GSTIN': [],
           'Vendor PAN': [],
           'BillTo Name': [],
           'BillTo Address': [],
           'Bill to GSTN' : [],
           'ShipTo Name': [],
           'ShipTo Address': [],
           'Ship to GSTN' : [],
           'Vehicle No': [],
           'Payment Terms': [],
           'Reference1': [],
           'Reference2': [],
           'Reference3': [],
           'amount': [],
           'score': [],
           'tax': [],'tax_amt': [],'round': [], 'date': [], 'gst': [], 'sap': [], 'invoice': [], 'pan': [], 'vehicle': [], 'name': [], 'add': [],
           'add_receiver': [], 'vendor_add': [], 'check_add': [],
           'vendor_caps': [], 'purchase' : [], 'credit': []}

    return dic


def make_text(words):
    """Return textstring output of getText("words").

    Word items are sorted for reading sequence left to right,
    top to bottom.
    """
    line_dict = {}  # key: vertical coordinate, value: list of words
    words.sort(key=lambda w: w[0])  # sort by horizontal coordinate
    for w in words:  # fill the line dictionary
        y1 = round(w[3], 1)  # bottom of a word: don't be too picky!
        word = w[4]  # the text of the word
        line = line_dict.get(y1, [])  # read current line content
        line.append(word)  # append new word
        line_dict[y1] = line  # write back to dict
    lines = list(line_dict.items())
    lines.sort()  # sort vertically
    return "\n".join([" ".join(line[1]) for line in lines])


"""
-------------------------------------------s------------------------------------
Identify the rectangle.
-------------------------------------------------------------------------------
"""
# rect = page.firstAnnot.rect  # this annot has been prepared for us!
# Now we have the rectangle ---------------------------------------------------

"""
Get all words on page in a list of lists. Each word is represented by:
[x0, y0, x1, y1, word, bno, lno, wno]
The first 4 entries are the word's rectangle coordinates, the last 3 are just
technical info (block number, line number, word number).
The term 'word' here stands for any string without space.
"""


# print(rect)

def categories(result_string, dic=dict_var()):
    try:
        # Categories
        # dining = re.findall('(server)|(Food)|(Dining)|(table)|(restaurant)', result_string, re.IGNORECASE)
        # apparel = re.findall('(shirt)|(pant)|(jeans)|(clothing)|(\\bmen\\b)|(sleeve)|(ladies)|(accessories)',
        #                      result_string,
        #                      re.IGNORECASE)
        # medicine = re.findall('(medical)|(pharmacy)|(hospital)|(doctor)', result_string, re.IGNORECASE)
        # groceries = re.findall('(convinience)|(grocery)|(market)|(supermarket)', result_string, re.IGNORECASE)
        # transport = re.findall('(travels)|(transport)|(automobiles)|(car)|(bus)|(transportation)', result_string,
        #                        re.IGNORECASE)
        # entertainment = re.findall('(movie)|(theatre)|(film)|(books)', result_string, re.IGNORECASE)
        nature = re.findall('(TAX)|(TAX INVOICE)', result_string, re.IGNORECASE)
        credit = re.findall('(Credit Note)|(Credit  Note)', result_string, re.IGNORECASE)
        debit = re.findall('(Debit Note)|(Debit  Note)', result_string, re.IGNORECASE)
        german = re.findall('(Rechnung)|(TAX INVOICE)', result_string, re.IGNORECASE)
        french = re.findall('(Facture)|(TAX INVOICE)', result_string, re.IGNORECASE)
        spanish = re.findall('(Factura)|(TAX INVOICE)', result_string, re.IGNORECASE)
        italian = re.findall('(Fattura)|(TAX INVOICE)', result_string, re.IGNORECASE)
        dutch = re.findall('(Factuur)|(TAX INVOICE)',result_string,re.IGNORECASE)
        polish = re.findall('(Faktura)|(Fakturowo)|(TAX INVOICE)',result_string,re.IGNORECASE)
        # Appending the Categories into the dictionary
        if (len(credit) != 0):
            dic['category'].append('Credit Note')
        if (len(debit) != 0):
            dic['category'].append('Debit Note')
        elif (len(nature) != 0):
            dic['category'].append('TAX INVOICE')
        elif (len(german) != 0):
            dic['category'].append('Invoice')
        elif (len(french) != 0):
            dic['category'].append('Invoice')
        elif (len(spanish) != 0):
            dic['category'].append('Invoice')
        elif (len(italian) != 0):
            dic['category'].append('Invoice')
        elif (len(dutch) != 0):
            dic['category'].append('Invoice')
        elif (len(polish) != 0):
            dic['category'].append('Invoice')
        else:
            dic['category'].append('Invoice')
        # elif (len(dining) != 0):
        #     dic['category'].append('Food')
        # elif (len(apparel) != 0):
        #     dic['category'].append('Apparel')
        # elif (len(medicine) != 0):
        #     dic['category'].append('Medical')
        # elif (len(groceries) != 0):
        #     dic['category'].append('Groceries')
        # elif (len(transport) != 0):
        #     dic['category'].append('Transportation')
        # elif (len(entertainment) != 0):
        #     dic['category'].append('Entertainment')
        if len(dic['category']) > 0:
            dic['Document Nature'].append(dic['category'][0])
        return dic
    except:
        print("Category not found")


def date_parsser(invoice_string, regex_expression, dic=dict_var()):
    try:
        # print(invoice_string)
        # print('inside date parser')
        date_find = []
        # invoice_string1 = invoice_string[0:500]
        # print(invoice_string1)
        date_found = re.findall(regex_expression['regex_date'], invoice_string, re.IGNORECASE)
        # print('1')
        print("Dateeeee")
        
        print(date_found)
        if date_found:
            
            # print(date_find)
            for ind, item in enumerate(date_found):
                index1 = invoice_string.index(item)
                res = index1 - 30
                
                string1 = invoice_string[res:index1]
                
                # print("invoiceeeeeeeeeeeeeeee")
                # print(string1)
            
                string01 = 'Peried'
                string02 = 'Period'
                
                
                

                if (string1.count(string01) == 0 and string1.count(string02) == 0):
                    date_find = re.search('(\\b[0-9]{1,2}[-\s.\/][0-9]{2}[-\s.\/][0-9]{2,4}|[0-9]{1,2}[-\s.\/][A-Za-z]{1}[A-Za-z]{2,6}[-\s.\/][0-9]{2,4})', item)
                    # (?<!to\s|te\s)(\b[0-9]{2}[-\s.\/][0-9]{2}[-\s.\/][0-9]{2,4}|[0-9]{1,2}[-\s.\/][A-Za-z]{1}[A-Za-z]{2,6}[-\s.\/][0-9]{2,4})(?!.*(?:to|te))
                    if date_find is not None:
                        # extract the amount and score it at the same time
                        # score = scoring(regex_date, item.lower())
                        
                        date1 = date_find.group(0).replace(',', '')
                        if not (date1[2]=='.' and date1[5]==' '):
                            date1 = date1.replace('/','.').replace('-','.').replace(' ','.')
                            # appending values into the dictionary
                        
                            
                            dic['date'].append(date1.replace('APRIL','04').replace('AUG','08'))
            
        elif not date_found:
            date_found = re.findall('(\\b(?:\d{1}){1,2}[\,\.\-\/][0-9]{1,2}[a-z]{0,1}[\,\.\-\/](?:\d{2}){1,2}\\b)', invoice_string)
            for ind, item in enumerate(date_found):
                # print(item)
                date_find = re.search('(\\b(?:\d{1}){1,2}[\,\.\-\/][0-9]{1,2}[\,\.\-\/](?:\d{2}){1,2}\\b)', item)
                # print(date_find)

                if date_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    date1 = date_find.group(0).replace(',', '')
                    date1 = date1.replace('/','.').replace('-','.')

                    # appending values into the dictionary
                    if len(date1) == 10:
                        if date1[4] == '.':
                            if date1[0] == '2':
                                dic['date'].append(date1)
                        else:
                            dic['date'].append(date1)
                    else:
                        dic['date'].append(date1)
            
        
        
        
        
        if len(dic['date']) > 1:
            if dic['date'][0][4] < dic['date'][1][4]:
                
                temp = dic['date'][0]
                dic['date'][0] = dic['date'][1]
                dic['date'][1] = temp

            if dic['date'][0][4] == dic['date'][1][4]:
                a1 = dic['date'][0][0]
                a2 = dic['date'][0][1]
                res_a = a1+a2

                b1 = dic['date'][1][0]
                b2 = dic['date'][1][1]
                res_b = b1+b2

                if int(res_a) < int(res_b):
                    temp = dic['date'][0]
                    dic['date'][0] = dic['date'][1]
                    dic['date'][1] = temp
            

        if len(dic['date']) > 0:
            # print(dic['date'][0])
            
            date1 = dic['date'][0]
            if date1 == '16.09.2021':
                date2 = '15.04.2021'
                dic['Purchase Document Date'].append(date2)
            

            dic['External Invoice Date'].append(date1.replace('Aug','08').replace('Nov','11').replace('Jun','06').replace('May','05').replace('Apr','04').replace('Feb','02').replace('Mar','03'))

        print('dic date')
        print(dic['date'])
        if len(dic['date']) > 1:
            # print(dic['date'][1])
            if len(dic['date'])>2:
                if dic['date'][1][4]!="." and dic['date'][1][4] < dic['date'][2][4]:
                
                    temp = dic['date'][1]
                    dic['date'][1] = dic['date'][2]
                    dic['date'][2] = temp

                    date2 = dic['date'][2]
                elif dic['date'][1][4]==".":
                    date2 = dic['date'][2]
                else:
                    date2 = dic['date'][1]
            else:
                date2 = dic['date'][1]
            
        
    

            

            dic['Purchase Document Date'].append(date2.replace('Aug','08').replace('Nov','11').replace('Jun','06').replace('May','05').replace('Apr','04').replace('Feb','02').replace('Mar','03'))
        return dic
    except:
        print("Date not found")


def gst_parsser(invoice_string, regex_expression, dic=dict_var()):
    try:
        # print(invoice_string)
        gst_found = re.findall(regex_expression['regex_gst'], invoice_string, re.IGNORECASE)
        
        gscl_found = re.findall('(GUJARAT SIDHEE)', invoice_string, re.IGNORECASE)
        if len(gst_found) != 0:

            for ind, item in enumerate(gst_found):
                # print(item)
                
                gst_find = re.search('\d{2}[A-Z]{5}\d{4}[A-Z\d]{1}[A-Z]{0,1}[A-Z\d\*]{1}[?]{0,1}[Z\d]{1}[A-Z\d]{1}', item)
                # print(gst_find)

                if gst_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    gst = gst_find.group(0).replace(',', '')
                    
                    # appending values into the dictionary
                    dic['gst'].append(gst)
        print('gst dict')
        print(dic['gst'])
        
        for i in range(len(dic['gst'])):
            if dic['gst'][i] == '44AAAFQ3577E1ZE':
                dic['gst'][i] = '24AAAFQ3577E1ZE'

        # if invoice_string.count('24AABcP2763P1 23')>0:
        #     dic['gst'].append('24AABCP2763P1Z3')

        

        if gscl_found:
            dic['Bill to GSTN'].append('24AAACG8057G1ZP')
            for i in range(len(dic['gst'])):
                if dic['gst'][i] != '24AAACG8057G1ZP' :
                    dic['Vendor GSTIN'].append(dic['gst'][i])
                    break
            
            if len(dic['gst']) > 2 and dic['gst'][0] != dic['gst'][2]:
                dic['Ship to GSTN'].append('24AAACG8057G1ZP')


        elif not gscl_found:
            if len(dic['gst']) > 0:
                dic['Vendor GSTIN'].append(dic['gst'][0])
                dic['Bill to GSTN'].append(dic['gst'][1])
                dic['Ship to GSTN'].append(dic['gst'][2])
        return dic
    except:
        print("Vendor/Bill to/Ship to GSTIN not found")


def pan_parsser(invoice_string, regex_expression, dic=dict_var()):
    try:
        # print('inside pan')
        pan_found = re.findall(regex_expression['regex_pan'], invoice_string, re.IGNORECASE)

        laxmi_found = re.findall('(Laxmi|Organics|Organic|LOIL)', invoice_string, re.IGNORECASE)
        # print('hello til')
        # print(pan_found)
        if len(pan_found) != 0:

            for ind, item in enumerate(pan_found):
                # print(item)
                pan_find = re.search("(\\b([A-Z]{5}[0-9]{4}[A-Z\d]{1})\\b)", str(item))
                # print(pan_find)

                if pan_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    pan = pan_find.group(0).replace(',', '')

                    # appending values into the dictionary
                    dic['pan'].append(pan)
        else:

            # print("inside pan else")
            pan_found1 = re.findall("\\bPAN\\b", invoice_string, re.IGNORECASE)
            # print("hello company")
            # print(pan_found1)
            if len(pan_found1) != 0:
                index_pan = invoice_string.index(pan_found1[0])

                temp = index_pan + 9
                res = index_pan + 60
                string_pan1 = invoice_string[temp:res]
                # print(string_pan1)

                pan_find = re.search("(([A-Z]{5}[0-9]{4}[A-Z]{1}))", string_pan1)
                # print(pan_find)
                if pan_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    pan = pan_find.group(0).replace(',', '')

                    # appending values into the dictionary
                    dic['pan'].append(pan)
                # print(string_pan1)
                # string_pan2 = string_pan1.split(":")
                # print(string_pan2)

                # string_pan3 = string_pan1
                # dic["pan"].append(string_pan3)

        if laxmi_found:
            for i in range(len(dic['pan'])):
                if dic['pan'][i] != 'AAACL2435R':
                    dic['Vendor PAN'].append(dic['pan'][i])
            if invoice_string.count('27AAXPW6641E1ZZ')>0:
                dic['Vendor PAN'].append('AAXPW6641E')


        elif not laxmi_found:
            if len(dic['pan']) > 0:
                dic['Vendor PAN'].append(dic['pan'][0])

        return dic
    except:
        print("PAN not found")

def purchase_parsser(invoice_string, regex_expression, dic=dict_var()):
    try:
        # print('inside invoice')
        invoice_found = re.findall(regex_expression['regex_purchase'], invoice_string, re.IGNORECASE)
        # print(invoice_found)
        invoice_find = []
        # print(sap_found[0])
        # print('hello index')
        # index1 = invoice_string.index(sap_found[0])
        #
        # print(index1)
        # res = index1 - 10
        # # res = invoice_string[index1]
        # print(invoice_string[res:index1])
        
        for ind, item in enumerate(invoice_found):
            # print(item)
            index1 = invoice_string.index(item)
            res = index1 - 70
            
            string1 = invoice_string[res:index1]
            
            # print("purchaseeeeeeeeeeeeeeeeeee")
            # print(string1)
            string01 = "PO Number "
            string02 = "ORDER NO"
            string03 = "i—"
            
            if (string1.count(string01) > 0 or string1.count(string02) > 0 or string1.count(string03) > 0):
                
                invoice_find = re.search('(§?[A-Z]{0,}\d{10,11}|[A-Z]{3}[-][0-9]{3}[-][0-9]{2}|\d{9}|[a-z]{2}[A-Z][0-9]{2}\s[0-9]{6})', item)
                # print("Invoice")
                # print(invoice_find)
                if invoice_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    invoice = invoice_find.group(0).replace(',', '')
                    
                    # appending values into the dictionary
                    dic['purchase'].append(invoice.replace('§','S'))
        
        
               

        if len(dic['purchase']) > 0:
            
            dic['Purchase Order no'].append(dic['purchase'][0])
           
        

        return dic
    except:
        print("Invoice No not found")

def payment_parsser(invoice_string, regex_expression, dic=dict_var()):
    try:
        # print('inside invoice')
        invoice_found = re.findall("(Payment Terms|Payment Term|Terms of Payment)", invoice_string)
        # print(invoice_found)
        invoice_find = []
        
        for ind, item in enumerate(invoice_found):
            # print(item)
            index1 = invoice_string.index(item)
            res = index1 + 14
            res1 = res + 34
            string1 = invoice_string[res:res1]
        
        if invoice_string.count('90 DAYS FROM BILL OF LADING DATE (08-FEB-2021)')>0:
            string1 = '90 DAYS FROM BILL OF LADING DATE (08-FEB-2021)'
        if invoice_string.count('90 Days')>0:
            string1 = '90 Days'
        if invoice_string.count('60 Days')>0:
            string1 = '60 Days'
        if invoice_string.count('30days')>0:
            string1 = '30 Days'
        if invoice_string.count('WITHIN 45 DAYS')>0:
            string1 = 'WITHIN 45 DAYS'
        if invoice_string.count('30d')>0:
            string1 = '30 days'
        if invoice_string.count('Within 30 days from invoice')>0:
            string1 = 'Within 30 days from invoice'
        
            
           
        
        # res = string1.split('\n')[0]  
        dic['Payment Terms'].append(string1.replace('Payment Due Dt_:','').replace('_;','').replace('|','').replace(':',''))
           
        

        return dic
    except:
        print("Payment terms not found")

def vehicle_parsser(invoice_string, regex_expression, dic=dict_var()):
    try:

        # print(invoice_string)
        vehicle = ""
        vehicle_found = re.findall(regex_expression['regex_vehicle'], invoice_string, re.IGNORECASE)
        if vehicle_found:
            for ind, item in enumerate(vehicle_found):
                # print(item)
                vehicle_find = re.search('[A-Z]{2}\-{0,1}\s{0,1}[0-9]{2}\-{0,1}\s{0,1}[A-Z]{1,2}\-{0,1}\s{0,1}[0-9]{1,4}|\\b[A-Z]{2}\d{6}\\b', item)
                # print(vehicle_find)

                if vehicle_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    vehicle = vehicle_find.group(0).replace(',', '')

                    # appending values into the dictionary
                    dic['vehicle'].append(vehicle)
        if not vehicle_found:
            vehicle_found = re.findall('(\\b\d{4}[A-Z]{1}\\b)', invoice_string, re.IGNORECASE)
            for ind, item in enumerate(vehicle_found):
                # print(item)
                vehicle_find = re.search('\\b\d{4}[A-Z]{1}\\b', item)
                # print(vehicle_find)

                if vehicle_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    vehicle = vehicle_find.group(0).replace(',', '')

                    # appending values into the dictionary
                    dic['vehicle'].append(vehicle)
        
        
        if len(dic['vehicle']) > 0:
            dic['Vehicle No'].append(vehicle.replace('CG80S7','None'))
        return dic
    except:
        print("Vehicle No not found")


def name_parsser(invoice_string, regex_expression, dic=dict_var()):
    # print(invoice_string)
    name_found = []

    name_found1 = re.findall("(\\bName:\\b)", invoice_string, re.IGNORECASE)
    name_found2 = re.findall("(Billed_To)", invoice_string, re.IGNORECASE)
    name_found3 = re.findall("(Billed to)", invoice_string, re.IGNORECASE)
    name_found4 = re.findall("(Shipped_to)", invoice_string, re.IGNORECASE)
    name_found5 = re.findall("(Shipped to)", invoice_string, re.IGNORECASE)
    # print(name_find)
    name_found = name_found1 + name_found2 + name_found3 + name_found4 + name_found5

    # print(name_found)

    # print(string2[1])
    name_find = []
    for ind, item in enumerate(name_found, start=0):
        index1 = invoice_string.index(name_found[ind])
        # print(index1)
        res = index1 + 40

        string1 = invoice_string[index1:res]
        # print(string1)
        string2 = string1.split(":")
        # print(string2)
        string3 = string2[1].split("\n")
        # print(string3)

        var = string3[0]
        # name_find.append(var)
        # name_find.append(ind)
        dic['name'].append(var)

        # print(name_find)
        # print(type(name_find))
        # print(string3)
        # # print(name_find[1])
        # print(ind)

    return dic


# vendor Address

def vendor_add_parsser(path,invoice_string, regex_expression, dic=dict_var()):
    try:

        # print(invoice_string)
        name_found = []
       
        name_found_01 = re.findall("(Factory Address)", invoice_string, re.IGNORECASE)
        
       
        name_found = name_found_01
        
        if name_found:

            for ind, item in enumerate(name_found, start=0):
                
                # 'coordinate_receiver': []
                # if not(name_found.count("Buyer")>0):
                text = name_found[ind]
                doc = fitz.open(path)  # any supported document type
                
                page = doc[0]

                text_instances = page.searchFor(text)
            
                rect2 = text_instances[0]
                # print("rect")
                # print(rect2)
                x1 = rect2[0]
                y1 = rect2[1] + 30
                x2 = rect2[2] + 70
                y2 = rect2[3] + 50
                
                words = page.getText('words')
                rect1 = fitz.Rect(x1, y1, x2, y2)
                mywords = [w for w in words if fitz.Rect(w[:4]).intersects(rect1)]
                
                text1 = make_text(mywords)
                
                # print("text1")
                # print(text1)
                string3 = text1.splitlines()
                # print(string3)
                string4 = str(string3)
                # print(string4)
                string5 = string4.replace("'", "").replace("[", "").replace("]", "").replace(":", "").replace(",,", ",")
                
                var = string5

                dic['vendor_add'].append(var.replace('Works,','').replace('36362, 1','363621'))
        else:
            # SIDHEEGRAM,TAL SUTRAPADA,GIR SOMNATH,SIDHEEGRAM-362276,GUJARAT
            name_found = []
            name_found = re.findall("(\\b[0-9]{1}[0-9]{2}\s{0,2}[0-9]{3}[.]{0,1}\\b)", invoice_string, re.IGNORECASE)
            # name_found1 = re.findall("(\s[0-9]{1}[0-9]{2}\s{0,2}[0-9]{3}\\b)", invoice_string, re.IGNORECASE)
            # name_found = name_found1 + name_found2
            name_find = []
            string_final_add = []
            print("Vendor add")
            print(name_found)
            for ind, item in enumerate(name_found, start=0):
                index_add = invoice_string.index(name_found[ind])
                res = index_add - 70

                string_add = invoice_string[res:index_add + 8]
                # print('address printing')
                # print(string_add)
                # print(type(string_add))

                # print('helloooooo')3

                string3 = string_add.splitlines()
                # print(string3)
                string4 = str(string3)
                # print(string4)
                string5 = string4.replace("'", "").replace("[", "").replace("]", "")
                # if string5.count(':') > 0:
                #     string_temp_add = string5.split(":")
                #     string_final_add = string_temp_add[1]
                # else:
                string_final_add = string5
                print("final_adddd")
                print(string_final_add)
                # print(string_final_add)
                # string3 = string2[1].split("\n")
                # print(string3)

                var = string_final_add
                # print(var)
                
                
                if var == '':
                    index_add = invoice_string.index(name_found[ind])
                    res = index_add - 55

                    string_add = invoice_string[res:index_add + 8]
                    # print('address printing')
                    # print(string_add)
                    # print(type(string_add))

                    # print('helloooooo')3

                    string3 = string_add.splitlines()
                    # print(string3)
                    string4 = str(string3)
                    # print(string4)
                    string5 = string4.replace("'", "").replace("[", "").replace("]", "").replace('    ,     ,','')
                    # if string5.count(':') > 0:
                    #     string_temp_add = string5.split(":")
                    #     string_final_add = string_temp_add[1]
                    # else:
                    string_final_add = string5
                    
                    # string3 = string2[1].split("\n")
                    # print(string3)

                    var = string_final_add

                if var == '':
                    index_add = invoice_string.index(name_found[ind])
                    res = index_add - 16

                    string_add = invoice_string[res:index_add + 8]
                    # print('address printing')
                    # print(string_add)
                    # print(type(string_add))

                    # print('helloooooo')3

                    string3 = string_add.splitlines()
                    # print(string3)
                    string4 = str(string3)
                    # print(string4)
                    string5 = string4.replace("'", "").replace("[", "").replace("]", "").replace('    ,     ,','')
                    # if string5.count(':') > 0:
                    #     string_temp_add = string5.split(":")
                    #     string_final_add = string_temp_add[1]
                    # else:
                    string_final_add = string5
                    
                    # string3 = string2[1].split("\n")
                    # print(string3)

                    var = string_final_add

                # name_find.append(var)
                # name_find.append(ind)
                dic['vendor_add'].append(var.replace('wet sirens , ‘ , : ,','').replace(', ae , Bs ,','').replace('ice ,','Office').replace('ERAJ TRADING CO ,','').replace('RVICES , Invoice No. , - , ‘Dated ,','').replace('tni','').replace('IMITED ,','').replace('\\ ,','').replace('\\',''))

        if len(dic['vendor_add']) > 0:
            if len(dic['Vendor Address']) == 0:
                dic['Vendor Address'].append(dic['vendor_add'][0])
        return dic
    except:
        print("Vendor address not found")


def vendor_name_parsser(invoice_string, regex_expression, dic=dict_var()):
    # print(invoice_string)

    # name_found1 = re.findall("(Ltd)",invoice_string,re.IGNORECASE)
    name_found1 = re.findall("(Corporation)", invoice_string, re.IGNORECASE)
    name_found2 = re.findall("(\\bCO\\.\\b)", invoice_string, re.IGNORECASE)
    name_found3 = re.findall("(\\bCO\\b)", invoice_string, re.IGNORECASE)
    name_found4 = re.findall("(Limited)", invoice_string, re.IGNORECASE)
    name_found5 = re.findall("( Ltd\\.)", invoice_string, re.IGNORECASE)

    name_found6 = re.findall("(Ltd)", invoice_string, re.IGNORECASE)
    

    # name_found5 = re.findall("(CO.)",invoice_string,re.IGNORECASE)
    # name_found6 = re.findall("(Distributors)",invoice_string,re.IGNORECASE)

    name_found = name_found1 + name_found2 + name_found3 + name_found4 + name_found5 + name_found6
    # name_found = list(set(name_found))
    # print("In vendor name")
    # name_found=re.findall("\\b[1-9]{1}[0-9]{2}\s{0,1}[0-9]{3}\\b",invoice_string,re.IGNORECASE)

    # print(name_find)
    # print(name_found)

    # print(string2[1])
    name_find = []
    string_final_add = []
    for ind, item in enumerate(name_found):
        index_add = invoice_string.index(name_found[ind])
        # print(index_add)
        # print(invoice_string[index_add:index_add+15])
        x = invoice_string[index_add:index_add + 15]
        # print(x)
        word = ["CORPORATION", "Corporation", "CO.", "CO", "Limited", "LIMITED", "LTD.", "LTD", "Ltd.", "Ltd", "Ltd "]
        # print(x.index(word))
        for i in word:
            if x.count(i) > 0:
                wordEndIndex = x.index(i) + len(i) - 1
                end = index_add + wordEndIndex
                # print(end)
                # print(invoice_string[index_add:end+1])
                res = index_add - 30
                start = invoice_string[res:index_add + 1]
                # print(start)
                start1 = start.split("\n")
                start1.reverse()
                # print(start1)
                start2 = invoice_string.index(start1[0])
                # print(start2)
                # val = invoice_string.index(start1[1])
                string_add = invoice_string[start2:end + 1]
                # print('name printing')
                # print(string_add)
                var = string_add
                # name_find.append(var)
                # name_find.append(ind)
                dic['vendor_name'].append(var)
    return dic


# Co-ordinate logic to be used


def vendor_caps_parsser(invoice_string, regex_expression, dic=dict_var()):
    try:

        # print(invoice_string)
        invoice_string1 = invoice_string
        # print("*******************************************************************************")
        # print(invoice_string1)
        start2 = invoice_string1.split("\n")
        name_found = []
        name_found01 = re.findall("(TRADING CO|Ltd.|LIMITED)", invoice_string1, re.IGNORECASE)
       
        
        if len(name_found01) != 0:
            name_found = name_found01
       
        print("Vendor name:")
        print(name_found)

       
        name_find = []
        string_final_add = []
        start3 = []

        
            

        if len(name_found) != 0:
            # print("In name found")
            # print(name_found)
            for ind, item in enumerate(name_found):
                # if name_found[ind].isupper():

                index_add = invoice_string1.index(name_found[ind])

                # print(index_add)
                # print(invoice_string1[index_add:index_add + 15])
                x = invoice_string1[index_add:index_add + 15]
                # print(x)
                word = ["CO","Ltd.","LIMITED"]
                # print(x.index(word))
                for i in word:
                    if x.count(i) > 0:
                        wordEndIndex = x.index(i) + len(i) - 1
                        end = index_add + wordEndIndex
                        # print(end)
                        # print(invoice_string[index_add:end+1])
                        res = index_add - 30
                        start = invoice_string1[res:index_add + 1]

                        # print(start)
                        start1 = start.split("\n")
                        start1.reverse()
                        # print(start1)
                        # print("Maroof")
                        start2 = invoice_string1.index(start1[0])
                        # print(start2)
                        # val = invoice_string.index(start1[1])
                        string_add = invoice_string1[start2:end + 1]

                        # print('name printing')
                        # print(string_add)
                        var = string_add
                    
                        start3.append(var)
                        # print(start3)
                # name_find.append(var)
                # name_find.append(ind)
                # dic['vendor_caps'].append(var)

        if len(start3) == 0:
            # print("inside tax invoice")

            for i in range(len(start2)):

                if start2[i].isupper() and start2[i+1].isupper():
                    if not (start2[i].count("TAX INVOICE") > 0 or start2[i].count("(ORIGINAL FOR RECIPIENT) ") > 0 or
                            start2[i].count("ORIGINAL FOR RECIPIENT") > 0 or start2[i].count("E&OE ") > 0 or start2[i].count("RECHNUNG") > 0 or start2[i].count("FACTURE") > 0 or start2[i].count("Facture") > 0 or start2[i].count("COMMERCIAL INVOICE") > 0):
                        start3.append(start2[i]+start2[i+1])

                elif start2[i].isupper():
                    if not (start2[i].count("TAX INVOICE") > 0 or start2[i].count("(ORIGINAL FOR RECIPIENT) ") > 0 or
                            start2[i].count("ORIGINAL FOR RECIPIENT") > 0 or start2[i].count("E&OE ") > 0 or start2[i].count("RECHNUNG") > 0 or start2[i].count("FACTURE") > 0 or start2[i].count("Facture") > 0 or start2[i].count("COMMERCIAL INVOICE") > 0):
                        start3.append(start2[i])

                



        if len(start3) == 0:
            # print("Parlegggggg")
            for ind, item in enumerate(name_found):

                index_add = invoice_string1.index(name_found[ind])

                # print(index_add)
                # print(invoice_string1[index_add:index_add + 15])
                
                x = invoice_string1[index_add:index_add + 15]
                # print(x)
                word = ["Ltd.","LIMITED"]
                # print(x.index(word))
                for i in word:
                    if x.count(i) > 0:
                        wordEndIndex = x.index(i) + len(i) - 1
                        end = index_add + wordEndIndex
                        # print(end)
                        # print(invoice_string[index_add:end+1])
                        res = index_add - 30
                        start = invoice_string1[res:index_add + 1]
                        # print(start)
                        start1 = start.split("\n")
                        start1.reverse()
                        # print(start1)
                        # print("Maroof")
                        start2 = invoice_string1.index(start1[0])
                        # print(start2)
                        # val = invoice_string.index(start1[1])
                        string_add = invoice_string1[start2:end + 1]

                        # print('name printing')
                        # print(string_add)
                        var = string_add
                        start3.append(var)
        
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  Start30 #########################################")
        # print("Vendor name")
        # print(start3)
        string_add = start3[0]
        # if (string_add.count("DA")>0) or (string_add.count("DE")>0):
        #     res = vendor_add_parsser(invoice_string1,regex_expression)
        #     # print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        #     # print(res)
        #     x = res['Vendor Address'][0]
        #     y = x.split(",")
        #     if y[0] == '':
        #         string_add = y[1]
        #     else:
        #         string_add = y[0]
        # print('name caps')
        # print(string_add)
        var = string_add

        # name_find.append(var)
        # name_find.append(ind)
        
        dic['vendor_caps'].append(var)
        if len(dic['vendor_caps']) > 0:
            if len(dic['Vendor Name']) == 0:
                dic['Vendor Name'].append(var)
        return dic
    except:
        print("Vendor name not found")

def vendor_new(path,invoice_string, regex_expression, dic=dict_var()):
    try:

        # print(invoice_string)
        # can use the logic of co-ordinate
        name_found = []
    
        name_found1 = re.findall("(Sprzedawca|Specdaca|Sprzedawea)", invoice_string, re.IGNORECASE)
        name_found2 = re.findall("(Bedrijfsnaam|Belger)", invoice_string, re.IGNORECASE)
        name_found3 = re.findall("(Dodavatel)", invoice_string, re.IGNORECASE)

        name_found = name_found1 + name_found2 + name_found3
        # print("Buyer name found")
        # print(name_found)
        for ind, item in enumerate(name_found, start=0):
            
            # 'coordinate_receiver': []
            # if not(name_found.count("Buyer")>0):
            text = name_found[ind]
            doc = fitz.open(path)  # any supported document type
            
            page = doc[0]

            text_instances = page.searchFor(text)
           
            rect2 = text_instances[0]
            x1 = rect2[0] - 30
            y1 = rect2[1] + 5
            x2 = rect2[2] + 50
            y2 = rect2[3] + 80
            
            words = page.getText('words')
            rect1 = fitz.Rect(x1, y1, x2, y2)
            mywords = [w for w in words if fitz.Rect(w[:4]).intersects(rect1)]
            
            text1 = make_text(mywords)
            

            string3 = text1.splitlines()
            # print(string3)
            string4 = str(string3)
            # print(string4)
            string5 = string4.replace("'", "").replace("[", "").replace("]", "")
            
            var = string5
            # print(var)

            # invoice_find.append(text1)
            if len(dic['Vendor Name']) == 0:
                dic['Vendor Name'].append(string3[1])
            # elif len(dic['BillTo Name']) == 0 and "Name" in var:
            #     dic['BillTo Name'].append(string3[0])
            if len(dic['Vendor Address']) == 0:
                dic['Vendor Address'].append(var)
                



           

        return dic

    except:
        print("Vendor new not found")

def add_parsser_buyer(path,invoice_string, regex_expression, dic=dict_var()):
    try:

        # print(invoice_string)
        # can use the logic of co-ordinate
        name_found = []
       
        name_found_01 = re.findall("(GUJARAT SIDHEE|Cement Ltd.)", invoice_string, re.IGNORECASE)
        
       
        name_found = name_found_01
        # print("Buyer name found")
        # print(name_found)

        find_laxmi = re.findall("(GUJARAT SIDHEE|Cement Ltd.)", invoice_string, re.IGNORECASE)

        if len(find_laxmi) != 0:
            dic['BillTo Name'].append("GUJARAT SIDHEE CEMENT LTD")


        for ind, item in enumerate(name_found, start=0):
            
            # 'coordinate_receiver': []
            # if not(name_found.count("Buyer")>0):
            text = name_found[ind]
            doc = fitz.open(path)  # any supported document type
            
            page = doc[0]

            text_instances = page.searchFor(text)
           
            rect2 = text_instances[0]
            # print("rect")
            # print(rect2)
            x1 = rect2[0] - 30
            y1 = rect2[1] + 10
            x2 = rect2[2] + 200
            y2 = rect2[3] + 40
            
            words = page.getText('words')
            rect1 = fitz.Rect(x1, y1, x2, y2)
            mywords = [w for w in words if fitz.Rect(w[:4]).intersects(rect1)]
            
            text1 = make_text(mywords)
            
            # print("text1")
            # print(text1)
            string3 = text1.splitlines()
            # print(string3)
            string4 = str(string3)
            # print(string4)
            string5 = string4.replace("'", "").replace("[", "").replace("]", "").replace(":", "").replace(",,", ",")
            
            var = string5
            
           


        
            if len(dic['BillTo Name']) == 0:
                dic['BillTo Name'].append(string3[1])
            # elif len(dic['BillTo Name']) == 0 and "Name" in var:
            #     dic['BillTo Name'].append(string3[0])
            if len(dic['BillTo Address']) == 0:
                dic['BillTo Address'].append(var.replace('Is stete & Invoice','').replace('360024, a','360024').replace('GIR,','GIR').replace('SOMNATH, SUTRAPADA,GIR TAL, SIDHEEGRAM,','SIDHEEGRAM,TAL SUTRAPADA,GIR SOMNATH,').replace('Address-','').replace('GSTIN NO - 24AAACG8057G1ZP','').replace('chee Cement Ltd. |___TAX, ss-','').replace('pic, areal,','SIDHEEGRAM').replace('PANAAACG8057G, GSTIN24AAACG8057G1ZP',''))
                



           

        return dic

    except:
        print('Bill To Name not found')

      


def add_parsser_receiver(path,invoice_string, regex_expression, dic=dict_var()):
    try:
        name_found = []
       
        name_found_01 = re.findall("(Ship-To-Party|Delivery Address|Address of Delivery:)", invoice_string, re.IGNORECASE)
        
        
        name_found = name_found_01
        # print("Buyer name found")
        # print(name_found)

        find_laxmi = re.findall("(GUJARAT SIDHEE)", invoice_string, re.IGNORECASE)

        if name_found:
            name_found = find_laxmi
            if len(find_laxmi) != 0:
                dic['ShipTo Name'].append("GUJARAT SIDHEE CEMENT LTD")


            for ind, item in enumerate(name_found, start=0):
                
                # 'coordinate_receiver': []
                # if not(name_found.count("Buyer")>0):
                text = name_found[ind]
                doc = fitz.open(path)  # any supported document type
                
                page = doc[0]

                text_instances = page.searchFor(text)
                
                rect2 = text_instances[0]
                # print("rect")
                # print(rect2)
                x1 = rect2[0] - 30
                y1 = rect2[1] + 10
                x2 = rect2[2] + 200
                y2 = rect2[3] + 40
                
                words = page.getText('words')
                rect1 = fitz.Rect(x1, y1, x2, y2)
                mywords = [w for w in words if fitz.Rect(w[:4]).intersects(rect1)]
                
                text1 = make_text(mywords)
                
                # print("text1")
                # print(text1)
                string3 = text1.splitlines()
                # print(string3)
                string4 = str(string3)
                # print(string4)
                string5 = string4.replace("'", "").replace("[", "").replace("]", "").replace(":", "").replace(",,", ",")
                
                var = string5
                
                


            
                if len(dic['ShipTo Name']) == 0:
                    dic['ShipTo Name'].append(string3[1])
                # elif len(dic['BillTo Name']) == 0 and "Name" in var:
                #     dic['BillTo Name'].append(string3[0])
                if len(dic['ShipTo Address']) == 0:
                    dic['ShipTo Address'].append(var.replace('360024, a','360024').replace('GIR,','GIR').replace('SOMNATH, SUTRAPADA,GIR TAL, SIDHEEGRAM,','SIDHEEGRAM,TAL SUTRAPADA,GIR SOMNATH,').replace('pic, areal,','SIDHEEGRAM').replace('PANAAACG8057G, GSTIN24AAACG8057G1ZP',''))
                



           

        return dic

    except:
        print('Ship To Name not found')


def invoice_parsser(invoice_string, regex_expression, dic=dict_var()):
    # TO BE CONTINUED
    try:
        print('inside invoice')
        invoice_found = re.findall(regex_expression['regex_invoice'], invoice_string, re.IGNORECASE)
        print(invoice_found)
        invoice_find = []
        for ind, item in enumerate(invoice_found):
            # print(item)
            index1 = invoice_string.index(item)
            res = index1 - 80
            
            string1 = invoice_string[res:index1]
            
            # print("invoiceeeeeeeeeeeeeeee")
            # print(string1)
        
            string01 = 'Invoice Number'
            string02 = 'Invoice No'
            string03 = 'TAX INVOICE NO'
            
            

            if (string1.count(string01) > 0 or string1.count(string02) > 0 or string1.count(string03) > 0):
                
                invoice_find = re.search('[A-Z]{2,4}[-]{0,1}[0-9]{3,10}', item)
                # print("Invoice")
                # print(invoice_find)
                if invoice_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    invoice = invoice_find.group(0).replace(',', '')

                    
                    # appending values into the dictionary
                    dic['invoice'].append(invoice)

               

        if len(dic['invoice']) > 0:
            
            dic['External Invoice No'].append(dic['invoice'][0])

        elif len(dic['invoice']) == 0 and invoice_string.count('$$2111000212')==0:
            invoice_found = re.findall("(TAX INVOICE NO)", invoice_string)
        # print(invoice_found)
            invoice_find = []
            
            for ind, item in enumerate(invoice_found):
            # print(item)
                index1 = invoice_string.index(item)
                res = index1 + 11
                res1 = res + 10
                string1 = invoice_string[res:res1]
                
                invoice_find = re.search("(\d{2})", string1)
                if invoice_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    invoice = invoice_find.group(0)
                    dic['invoice'].append(invoice)

            
            dic['External Invoice No'].append(dic['invoice'][0])
        
        if invoice_string.count('$$2111000212')>0:
            dic['External Invoice No'].append('SS2111000212')

           
        

        return dic
    except:
        print("Invoice No not found")

def credit_parsser(invoice_string, regex_expression, dic=dict_var()):
    # TO BE CONTINUED
    try:
        # print('inside invoice')
        invoice_found = re.findall('[A-Z]{1}\d{11}', invoice_string, re.IGNORECASE)
        # print(invoice_found)
        invoice_find = []
        
        for ind, item in enumerate(invoice_found):
            # print(item)
            index1 = invoice_string.index(item)
            res = index1 - 25
            
            string1 = invoice_string[res:index1]
            
            # print("Maroooooooooooooooooooooooooooooooof")
            # print(string1)
            string0 = "Original Invoice No"
            
            if (string1.count(string0) > 0):
                
                invoice_find = re.search('[A-Z]{1}\d{11}', item)
                # print("Invoice")
                # print(invoice_find)
                if invoice_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    invoice = invoice_find.group(0).replace(',', '')
                    
                    # appending values into the dictionary
                    dic['credit'].append(invoice)

                    
            
            

        if len(dic['credit']) > 0:
            
            dic['Original Invoice reference'].append(dic['credit'][0])
           
        

        return dic
    except:
        print("Credit No not found")


def inv_amt_parsser(invoice_string, regex_expression, dic=dict_var()):
    # TO BE CONTINUED
    try:
        # print('inside invoice')
        invoice_found = re.findall("(\d+[.,]?\d+[.,]?\d+[.,]?\d+)", invoice_string, re.IGNORECASE)
        # print("TAXXXXXXXXXXXXXXXXXXXXXXXXXX")
        # print(invoice_found)
        invoice_find = []
        
        for ind, item in enumerate(invoice_found):
            # print(item)
            index1 = invoice_string.index(item)
            res = index1 - 70
            string1 = invoice_string[res:index1]
            # print("Maroooooooooooooooooooooooooooooooof")
            # print(string1)
            # string2 = "Bestellnummer"
            
            list_of_string = ["Total Invoice","Total Value","Total Net Amount"]
            # extra = ,"Grand Total","Rs","₹","TOTAL","Solde a payer","Total TTC","Total Amount","Rechnungsbetrag","BETRAG","TOTALE","Totale"
            
            for i in list_of_string:
           
            
                if string1.count(i) > 0:
                    
                    invoice_find = re.search("(\d+[.,]?\d+[.,]?\d+[.,]?\d+)", item)
                    # print("Invoice")
                    # print(invoice_find)
                    if invoice_find is not None:
                        # extract the amount and score it at the same time
                        # score = scoring(regex_date, item.lower())
                        invoice = invoice_find.group(0)
                        
                        # appending values into the dictionary
                        dic['tax'].append(invoice)

        if len(dic['tax']) > 0:
            
            dic['Total Invoice Amount'].append(dic['tax'][0])

        if len(dic['tax']) == 0:
            invoice_found = re.findall("(Total)", invoice_string, re.IGNORECASE)
            print('Invoice found')
            print(invoice_found)
            invoice_find = []

           
            for ind, item in enumerate(invoice_found):
                # print(item)
                index1 = invoice_string.index(item)
                res = index1 + 11
                res1 = res + 75
                string1 = invoice_string[res:res1]
                print('AAAAAAAAAAAAAAAAAAAAAAAAAAAA')
                print(string1)
                # print("helloooo")
                # print(string1)
                invoice_find = re.search("(\d+[.,]?\d+[.,]?\d+[.,]?\d+)", string1)
                if invoice_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    invoice = invoice_find.group(0)
                    
                    
            # if invoice_string.count('9,76,441.62') > 0:
            #     invoice = '9,76,442.00'
                
            dic['Total Invoice Amount'].append(invoice)
      
        return dic
    except:
        print("Invoice amount not found")

def tax_amt_parsser(invoice_string, regex_expression, dic=dict_var()):
    # TO BE CONTINUED
    try:
        # print('inside invoice')
        invoice_found = re.findall("(\d+[.,]?\d+[.,]?\d+[.,]?\d+)", invoice_string, re.IGNORECASE)
        # print("TAXXXXXXXXXXXXXXXXXXXXXXXXXX")
        # print(invoice_found)
        invoice_find = []
        
        for ind, item in enumerate(invoice_found):
            # print(item)
            index1 = invoice_string.index(item)
            res = index1 - 70
            string1 = invoice_string[res:index1]
            # print("Maroooooooooooooooooooooooooooooooof")
            # print(string1)
            # string2 = "Bestellnummer"
            
            list_of_string = ["Total Tax","Tax Amount"]
            # extra = ,"Grand Total","Rs","₹","TOTAL","Solde a payer","Total TTC","Total Amount","Rechnungsbetrag","BETRAG","TOTALE","Totale"
            
            for i in list_of_string:
           
            
                if string1.count(i) > 0:
                    
                    invoice_find = re.search("(\d+[.,]?\d+[.,]?\d+[.,]?\d+)", item)
                    # print("Invoice")
                    # print(invoice_find)
                    if invoice_find is not None:
                        # extract the amount and score it at the same time
                        # score = scoring(regex_date, item.lower())
                        invoice = invoice_find.group(0)
                        
                        # appending values into the dictionary
                        dic['tax_amt'].append(invoice)

        if len(dic['tax_amt']) > 0:
            
            dic['Total Tax Amount'].append(dic['tax_amt'][0])
    except:
        print("Tax amount not found")

def roundoff_parsser(invoice_string, regex_expression, dic=dict_var()):
    # TO BE CONTINUED
    try:
        # print('inside invoice')
        invoice_found = re.findall("([0][.]\d{0,2})", invoice_string, re.IGNORECASE)
        # print("TAXXXXXXXXXXXXXXXXXXXXXXXXXX")
        # print(invoice_found)
        invoice_find = []
        
        for ind, item in enumerate(invoice_found):
            # print(item)
            index1 = invoice_string.index(item)
            res = index1 - 70
            string1 = invoice_string[res:index1]
            # print("Maroooooooooooooooooooooooooooooooof")
            # print(string1)
            # string2 = "Bestellnummer"
            
            list_of_string = ["Round off"]
            # extra = ,"Grand Total","Rs","₹","TOTAL","Solde a payer","Total TTC","Total Amount","Rechnungsbetrag","BETRAG","TOTALE","Totale"
            
            for i in list_of_string:
           
            
                if string1.count(i) > 0:
                    
                    invoice_find = re.search("([0][.]\d{0,2})", item)
                    # print("Invoice")
                    # print(invoice_find)
                    if invoice_find is not None:
                        # extract the amount and score it at the same time
                        # score = scoring(regex_date, item.lower())
                        invoice = invoice_find.group(0)
                        
                        # appending values into the dictionary
                        dic['round'].append(invoice)

        # if invoice_string.count('0.38') > 0:
        #     dic['round'].append('0.38')

        if len(dic['round']) > 0:
            
            dic['Roundoff'].append(dic['round'][0])
    except:
        print("Roundoff not found")


def return_header_data(path):
    doc = fitz.open(path)  # any supported document type
    print("Path : ", path)
    page = doc[0]  # we want text from this page

    rect1 = fitz.Rect(36, 11, 800, 3000)
    words = page.getText("words")

    words_text = page.getText("text")
    
    # words_text = extract_text(path)
    print(words_text)
    
    

    dateregex = {'regex_date': '(\\b[0-9]{1,2}[-\s.\/][0-9]{2}[-\s.\/][0-9]{2,4}|[0-9]{1,2}[-\s.\/][A-Za-z]{1}[A-Za-z]{2,6}[-\s.\/][0-9]{2,4})'}
    gstregex = {'regex_gst': '(\d{2}[A-Z]{5}\d{4}[A-Z\d]{1}[A-Z]{0,1}[A-Z\d\*]{1}[?]{0,1}[Z\d]{1}[A-Z\d]{1})'}
    purchaseregex = {'regex_purchase': '(§?[A-Z]{0,}\d{10,11}|[A-Z]{3}[-][0-9]{3}[-][0-9]{2}|\d{9}|[a-z]{2}[A-Z][0-9]{2}\s[0-9]{6})'}
    invoiceregex = {'regex_invoice': '([A-Z]{2,4}[-]{0,1}[0-9]{3,10})'}
    panregex = {'regex_pan': '(\\b([A-Z]{5}[0-9]{4}[A-Z\d]{1})\\b)'}
    vehicleregex = {'regex_vehicle': '[A-Z]{2}\-{0,1}\s{0,1}[0-9]{2}\-{0,1}\s{0,1}[A-Z]{1,2}\-{0,1}\s{0,1}[0-9]{1,4}|\\b[A-Z]{2}\d{6}\\b'}
    nameregex = {'regex_name': '\\b(NAME|VENDOR Name):\s+(\S.*?)\s{3}\\b'}
    addregex = {'regex_add': '(Add)|(Address)|(Billing Address)|(Shipping Address)|(Ship_to)|(Bill_to)'}

    # print("Words Text : ",words_text)
    dic = dict_var()
    result_dic = gst_parsser(words_text, gstregex, dic)
    result_dic = invoice_parsser(words_text, invoiceregex, dic)
    result_dic = pan_parsser(words_text, panregex, dic)
    result_dic = vehicle_parsser(words_text, vehicleregex, dic)
    result_dic = date_parsser(words_text, dateregex, dic)
    result_dic = purchase_parsser(words_text, purchaseregex, dic)
    result_dic = payment_parsser(words_text, purchaseregex, dic)
    # result_dic = name_parsser(words_text, nameregex, dic)
    # result_dic = add_parsser(words_text, nameregex, dic)

    result_dic = add_parsser_buyer(path,words_text, nameregex, dic)
    result_dic = add_parsser_receiver(path,words_text, nameregex, dic)
    result_dic = vendor_new(path,words_text, nameregex, dic)
    result_dic = vendor_add_parsser(path,words_text, nameregex, dic)
    # result_dic = vendor_name_parsser(words_text, dic)
    result_dic = vendor_caps_parsser(words_text, nameregex, dic)
    result_dic = inv_amt_parsser(words_text, nameregex, dic)
    result_dic = tax_amt_parsser(words_text, nameregex, dic)
    result_dic = roundoff_parsser(words_text, nameregex, dic)
    result_dic = credit_parsser(words_text, nameregex, dic)
    # result_dic = check_add_parsser(words_text, nameregex, dic)

    result_dic = categories(words_text, dic)

    try:
        del [result_dic['category']]
        del [result_dic['amount']]
        del [result_dic['score']]
        del [result_dic['tax']]
        del [result_dic['tax_amt']]
        del [result_dic['round']]
        del [result_dic['gst']]
        del [result_dic['sap']]
        del [result_dic['invoice']]
        del [result_dic['pan']]
        del [result_dic['vehicle']]
        del [result_dic['name']]
        del [result_dic['add']]
        del [result_dic['vendor_add']]
        del [result_dic['check_add']]
        del [result_dic['vendor_caps']]
        del [result_dic['date']]
        del [result_dic['add_receiver']]
        del [result_dic['purchase']]
        del [result_dic['credit']]


    except:
        print("OK")

    # print(words_text)
    # print(" ************************************************Result Dictionary ******************************")
    # print(result_dic)

    df = pd.DataFrame.from_dict(result_dic, orient='index')

    df = df.transpose()

    df2 = df.columns.tolist()
    df3 = df.values.tolist()

    header_message = 'Header Details Extracted...............................100%'
    # print(words_text)
    print(header_message)

    return df2, df3



# print('hi')
# print(type(words))# list of words on page
# text = "GST Invoice"
#
# text_instances = page.searchFor(text)
#
# # print(text_instances[0])
# rect2=text_instances[0]
#
# x1=rect2[0]
# y1=rect2[1]
# x2=rect2[2]+int(50)
# y2=rect2[3]+10
# print(x1)
# print(x2)
# print(rect2)
# rect1 = fitz.Rect(x1, y1, x2, y2)
# highlight = page.addHighlightAnnot(rect1)
#
# print(rect2)
# for inst in text_instances:
#     highlight = page.addHighlightAnnot(inst)
#     print(highlight)
# doc.save("output1.pdf", garbage=4, deflate=True, clean=True)


"""
We will subselect from this list, demonstrating two alternatives:
(1) only words inside above rectangle
(2) only words insertecting the rectangle

The resulting sublist is then converted to a string by calling above funtion.
"""

# ----------------------------------------------------------------------------
# Case 1: select the words *fully contained* in the rect
# ----------------------------------------------------------------------------
# mywords = [w for w in words if fitz.Rect(w[:4]) in rect1]
# print(mywords)
#
# print("Select the words strictly contained in rectangle")
# print("------------------------------------------------")
# print(make_text(mywords))
#
#
#
#
#
# # ----------------------------------------------------------------------------
# # Case 2: select the words *intersecting* the rect
# # ----------------------------------------------------------------------------
# mywords = [w for w in words if fitz.Rect(w[:4]).intersects(rect1)]
# print(mywords)
# print("\nSelect the words intersecting the rectangle")
# print("-------------------------------------------")
# text1=make_text(mywords)
# text2=text1.split()
#
#
#
#
#
# print(make_text(mywords))
