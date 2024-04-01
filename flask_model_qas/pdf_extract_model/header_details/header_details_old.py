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


def dict_var():
    dic = {'category': [],
        'Document Nature':[],
        'External Invoice No':[],
            'External Invoice Date':[],
        'Purchase Order no':[],
            'Purchase Document Date':[],
        'Total Invoice Amount':[],
        'Total Tax Amount':[],
        'Roundoff':[],
        'Vendor Name':[],
        'Vendor Address':[],
        'Vendor GSTIN':[],
        'Vendor PAN':[],
        'BillTo Name':[],
        'BillTo Address':[],
        'ShipTo Name':[],
        'ShipTo Address':[],
        'Vehicle No':[],
        'Payment Terms':[],
        'Reference1':[],
            'Reference2':[],
            'Reference3':[],
        'amount': [],
        'score': [],
        'tax': [],'date': [],'gst': [],'sap': [], 'invoice': [], 'pan': [],'vehicle': [], 'name':[],'add':[],'add_receiver':[],'vendor_add':[],'check_add':[],
        'vendor_caps':[], }

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
#rect = page.firstAnnot.rect  # this annot has been prepared for us!
# Now we have the rectangle ---------------------------------------------------

"""
Get all words on page in a list of lists. Each word is represented by:
[x0, y0, x1, y1, word, bno, lno, wno]
The first 4 entries are the word's rectangle coordinates, the last 3 are just
technical info (block number, line number, word number).
The term 'word' here stands for any string without space.
"""
#print(rect)

def categories(result_string, dic=dict_var()):
    try:
    # Categories
        dining = re.findall('(server)|(Food)|(Dining)|(table)|(restaurant)', result_string, re.IGNORECASE)
        apparel = re.findall('(shirt)|(pant)|(jeans)|(clothing)|(\\bmen\\b)|(sleeve)|(ladies)|(accessories)', result_string,
                            re.IGNORECASE)
        medicine = re.findall('(medical)|(pharmacy)|(hospital)|(doctor)', result_string, re.IGNORECASE)
        groceries = re.findall('(convinience)|(grocery)|(market)|(supermarket)', result_string, re.IGNORECASE)
        transport = re.findall('(travels)|(transport)|(automobiles)|(car)|(bus)|(transportation)', result_string,
                            re.IGNORECASE)
        entertainment = re.findall('(movie)|(theatre)|(film)|(books)', result_string, re.IGNORECASE)
        nature = re.findall('(TAX)|(TAX INVOICE)', result_string, re.IGNORECASE)


        # Appending the Categories into the dictionary
        if (len(nature) != 0):
            dic['category'].append('Tax Invoice')
        elif (len(dining) != 0):
            dic['category'].append('Food')
        elif (len(apparel) != 0):
            dic['category'].append('Apparel')
        elif (len(medicine) != 0):
            dic['category'].append('Medical')
        elif (len(groceries) != 0):
            dic['category'].append('Groceries')
        elif (len(transport) != 0):
            dic['category'].append('Transportation')
        elif (len(entertainment) != 0):
            dic['category'].append('Entertainment')
        if len(dic['category'])>0:
            dic['Document Nature'].append(dic['category'][0])
        return dic
    except:
        print("Category not found")


def date_parsser(invoice_string, regex_expression, dic=dict_var()):
    try:
        #print(invoice_string)
        # print('inside date parser')
        date_find=[]
        date_found1 = re.findall('([0-9]{2}\-[A-Z]{1}[a-z]{2}\-[0-9]{4})', invoice_string, re.IGNORECASE)
        for ind, item in enumerate(date_found1):
            # print(item)
            date_find = re.search('([0-9]{2}[-][A-Z]{1}[a-z]{2}[-][0-9]{4})', item)
            # print(date_find)

            if date_find is not None:
                # extract the amount and score it at the same time
                # score = scoring(regex_date, item.lower())
                date1 = date_find.group(0).replace(',', '')

                # appending values into the dictionary
                dic['date'].append(date1)
        date_found = re.findall(regex_expression['regex_date'],invoice_string,re.IGNORECASE)
        # print('1')
        if date_found is not None:
            if date_find is not None:
                for ind, item in enumerate(date_found):
                    # print(item)
                    date_find = re.search('([0-9]{2}\\.[0-9]{2}\\.[0-9]{4})', item)
                    # print(date_find)

                    if date_find is not None:
                        # extract the amount and score it at the same time
                        #score = scoring(regex_date, item.lower())
                        date1 = date_find.group(0).replace(',', '')

                        # appending values into the dictionary
                        dic['date'].append(date1)
        if date_find is None:
            # print('2')
            date_found = re.findall('([0-9]{2}\-[A-Z]{1}[a-z]{2}\-[0-9]{4})', invoice_string, re.IGNORECASE)
            for ind, item in enumerate(date_found):
                # print(item)
                date_find = re.search('([0-9]{2}[-][A-Z]{1}[a-z]{2}[-][0-9]{4})', item)
                # print(date_find)

                if date_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    date1 = date_find.group(0).replace(',', '')

                    # appending values into the dictionary
                    dic['date'].append(date1)

        if date_find is None:
            # print('3')
            date_found = re.findall('([0-9]{2}[-][0-9]{2}[-][0-9]{4})', invoice_string, re.IGNORECASE)
            for ind, item in enumerate(date_found):
                # print(item)
                date_find = re.search('([0-9]{2}[-][0-9]{2}[-][0-9]{4})', item)
                # print(date_find)

                if date_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    date1 = date_find.group(0).replace(',', '')

                    # appending values into the dictionary
                    dic['date'].append(date1)




        if len(dic['date'])>0:
            # print(dic['date'][0])
            date1 = dic['date'][0]
            dic['External Invoice Date'].append(date1)

        if len(dic['date'])>1:
            # print(dic['date'][1])
            date2 = dic['date'][1]

            dic['Purchase Document Date'].append(date2)
        return dic
    except:
        print("Date not found")

def gst_parsser(invoice_string, regex_expression, dic=dict_var()):
    try:
        #print(invoice_string)
        gst_found = re.findall(regex_expression['regex_gst'],invoice_string,re.IGNORECASE)
        if len(gst_found)!=0:

            for ind, item in enumerate(gst_found):
                # print(item)
                gst_find = re.search('\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}', item)
                # print(gst_find)

                if gst_find is not None:
                    # extract the amount and score it at the same time
                    #score = scoring(regex_date, item.lower())
                    gst = gst_find.group(0).replace(',', '')

                    # appending values into the dictionary
                    dic['gst'].append(gst)

        else:

        # print("inside pan else")
            gst_found1 = re.findall("\\bGSTIN\\b", invoice_string, re.IGNORECASE)
            # print("hello company")
            # print(gst_found1)
            if len(gst_found1) != 0:
                index_pan = invoice_string.index(gst_found1[0])

                temp = index_pan + 7
                res = index_pan + 25
                string_gst1 = invoice_string[temp:res]
                # print(string_pan1)

                #gst_find = re.search("(([A-Z]{5}[0-9]{4}[A-Z]{1}))", string_gst1)
                # print(pan_find)
                # if gst_find is not None:
                #     # extract the amount and score it at the same time
                #     # score = scoring(regex_date, item.lower())
                #     gst = gst_find.group(0).replace(',', '')

                    # appending values into the dictionary
                dic['gst'].append(string_gst1)
                # print(string_pan1)
                # string_pan2 = string_pan1.split(":")
                # print(string_pan2)

                # string_pan3 = string_pan1
                # dic["pan"].append(string_pan3)


        # print(dic['gst'])
        if len(dic['gst'])>0:
            dic['Vendor GSTIN'].append(dic['gst'][0])
        return dic
    except:
        print("Vendor GSTIN not found")



def pan_parsser(invoice_string, regex_expression, dic=dict_var()):
    try:
        # print('inside pan')
        pan_found = re.findall(regex_expression['regex_pan'],invoice_string,re.IGNORECASE)
        # print('hello til')
        # print(pan_found)
        if len(pan_found)!=0:

            for ind, item in enumerate(pan_found):
                # print(item)
                pan_find = re.search("(\\b([A-Z]{5}[0-9]{4}[A-Z]{1})\\b)", str(item))
                # print(pan_find)

                if pan_find is not None:
                    # extract the amount and score it at the same time
                    # score = scoring(regex_date, item.lower())
                    pan = pan_find.group(0).replace(',', '')

                    # appending values into the dictionary
                    dic['pan'].append(pan)
        else:

            # print("inside pan else")
            pan_found1 = re.findall("\\bPAN\\b",invoice_string,re.IGNORECASE)
            #print("hello company")
            # print(pan_found1)
            if len(pan_found1)!=0:
                index_pan = invoice_string.index(pan_found1[0])



                temp = index_pan+9
                res = index_pan + 60
                string_pan1 = invoice_string[temp:res]
                #print(string_pan1)

                pan_find = re.search("(([A-Z]{5}[0-9]{4}[A-Z]{1}))", string_pan1)
                #print(pan_find)
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
        if len(dic['pan'])>0:
            dic['Vendor PAN'].append(dic['pan'][0])

        return dic
    except:
        print("PAN not found")

def vehicle_parsser(invoice_string, regex_expression, dic=dict_var()):
    try:

        #print(invoice_string)
        vehicle = ""
        vehicle_found = re.findall(regex_expression['regex_vehicle'],invoice_string,re.IGNORECASE)
        for ind, item in enumerate(vehicle_found):
            # print(item)
            vehicle_find = re.search('[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}', item)
            # print(vehicle_find)

            if vehicle_find is not None:
                # extract the amount and score it at the same time
                #score = scoring(regex_date, item.lower())
                vehicle = vehicle_find.group(0).replace(',', '')

                # appending values into the dictionary
                dic['vehicle'].append(vehicle)

        if len(dic['vehicle']) > 0:
            dic['Vehicle No'].append(vehicle)
        return dic
    except:
        print("Vehicle No not found")

def name_parsser(invoice_string, regex_expression, dic=dict_var()):
    #print(invoice_string)
    name_found=[]

    name_found1 = re.findall("(\\bName:\\b)",invoice_string,re.IGNORECASE)
    name_found2 = re.findall("(Billed_To)",invoice_string,re.IGNORECASE)
    name_found3 = re.findall("(Billed to)", invoice_string, re.IGNORECASE)
    name_found4 = re.findall("(Shipped_to)", invoice_string, re.IGNORECASE)
    name_found5 = re.findall("(Shipped to)", invoice_string, re.IGNORECASE)
    # print(name_find)
    name_found=name_found1+name_found2+name_found3+name_found4+name_found5

    # print(name_found)

    # print(string2[1])
    name_find = []
    for ind, item in enumerate(name_found,start=0):
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

#vendor Address

def vendor_add_parsser(invoice_string, regex_expression, dic=dict_var()):
    try:

    # print(invoice_string)
        name_found=[]

        name_found=re.findall("\\b[1-9]{1}[0-9]{2}\s{0,1}[0-9]{3}\\b",invoice_string,re.IGNORECASE)

        name_find = []
        string_final_add=[]
        for ind, item in enumerate(name_found,start=0):
            index_add = invoice_string.index(name_found[ind])
            # print(index_add)
            res = index_add - 76

            string_add = invoice_string[res:index_add+7]
            # print('address printing')
            # print(string_add)
            # print(type(string_add))

            # print('helloooooo')

            string3 = string_add.splitlines()
            # print(string3)
            string4 = str(string3)
            # print(string4)
            string5 = string4.replace("'", "").replace("[", "").replace("]", "")
            # print(string5)
            if string5.count(':')>0:
                string_temp_add = string5.split(":")
                string_final_add=string_temp_add[1]
            else:
                string_final_add=string5
            # print(string_final_add)
            #string3 = string2[1].split("\n")
            #print(string3)

            var = string_final_add
            # name_find.append(var)
            # name_find.append(ind)
            dic['vendor_add'].append(var)

        if len(dic['vendor_add'])>0:
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

    name_found6 = re.findall("(Ltd)",invoice_string,re.IGNORECASE)


    # name_found5 = re.findall("(CO.)",invoice_string,re.IGNORECASE)
    # name_found6 = re.findall("(Distributors)",invoice_string,re.IGNORECASE)

    name_found= name_found1+name_found2+name_found3+name_found4+name_found5+name_found6
    # name_found = list(set(name_found))
    # print("In vendor name")
    # name_found=re.findall("\\b[1-9]{1}[0-9]{2}\s{0,1}[0-9]{3}\\b",invoice_string,re.IGNORECASE)

    # print(name_find)
    # print(name_found)

    # print(string2[1])
    name_find = []
    string_final_add=[]
    for ind, item in enumerate(name_found):
        index_add = invoice_string.index(name_found[ind])
        # print(index_add)
        # print(invoice_string[index_add:index_add+15])
        x= invoice_string[index_add:index_add+15]
        # print(x)
        word=["CORPORATION","Corporation","CO.","CO","Limited","LIMITED","LTD.","LTD","Ltd.","Ltd","Ltd "]
        # print(x.index(word))
        for i in word:
            if x.count(i)>0:
                wordEndIndex = x.index(i) + len(i) - 1
                end = index_add + wordEndIndex
                # print(end)
                # print(invoice_string[index_add:end+1])
                res = index_add - 30
                start = invoice_string[res:index_add+1]
                # print(start)
                start1 = start.split("\n")
                start1.reverse()
                # print(start1)
                start2 = invoice_string.index(start1[0])
                # print(start2)
                # val = invoice_string.index(start1[1])
                string_add = invoice_string[start2:end+1]
                # print('name printing')
                # print(string_add)
                var = string_add
                # name_find.append(var)
                # name_find.append(ind)
                dic['vendor_name'].append(var)
    return dic












#Co-ordinate logic to be used



def vendor_caps_parsser(invoice_string, regex_expression, dic=dict_var()):
    try:

        # print(invoice_string)
        invoice_string1 = invoice_string[0:400]
        # print(invoice_string1)
        start2 = invoice_string1.split("\n")
        name_found = []

        name_found1 = re.findall("(Corporation)", invoice_string1, re.IGNORECASE)
        name_found2 = re.findall("(\\bCO\\.\\b)", invoice_string1, re.IGNORECASE)
        name_found3 = re.findall("(\\bCO\\b)", invoice_string1, re.IGNORECASE)
        name_found4 = re.findall("(Limited)", invoice_string1, re.IGNORECASE)
        name_found5 = re.findall("( Ltd\\.)", invoice_string1, re.IGNORECASE)

        name_found6 = re.findall("(Ltd)", invoice_string1, re.IGNORECASE)

        # name_found5 = re.findall("(CO.)",invoice_string,re.IGNORECASE)
        # name_found6 = re.findall("(Distributors)",invoice_string,re.IGNORECASE)
        if len(name_found1)!=0:
            name_found = name_found1
        elif len(name_found2)!=0:
            name_found = name_found2
        elif len(name_found3)!=0:
            name_found = name_found3
        elif len(name_found4)!=0:
            name_found = name_found4
        elif len(name_found5)!=0:
            name_found = name_found5
        elif len(name_found6)!=0:
            name_found = name_found6

        # name_found = name_found1 + name_found2 + name_found3 + name_found4 + name_found5 + name_found6
        # print(name_found)
        # print("In vendor caps")
        # name_found=re.findall("\\b[1-9]{1}[0-9]{2}\s{0,1}[0-9]{3}\\b",invoice_string,re.IGNORECASE)

        # print(name_find)
        # print(name_found)

        # print(string2[1])
        name_find = []
        string_final_add=[]
        start3 = []
        # for ind, item in enumerate(name_found):
        #     index_add = invoice_string1.index(name_found[ind])
        #     print(index_add)
        #     start = (invoice_string1[index_add:index_add+60])
        #     print(start)
        #     start2 = start.split("\n")

        # print(name_found)
        if len(name_found)!=0:
            # print("In name found")
            # print(name_found)
            for ind, item in enumerate(name_found):
                # if name_found[ind].isupper():

                    index_add = invoice_string1.index(name_found[ind])

                    # print(index_add)
                    # print(invoice_string1[index_add:index_add + 15])
                    x = invoice_string1[index_add:index_add + 15]
                    # print(x)
                    word = ["CORPORATION", "Corporation", "CO.", "CO", "Limited", "LIMITED", "LTD.", "LTD", "Ltd.", "Ltd",
                            "Ltd "]
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

                if start2[i].isupper():
                    if not (start2[i].count("TAX INVOICE") > 0 or start2[i].count("(ORIGINAL FOR RECIPIENT) ") > 0 or
                            start2[i].count("ORIGINAL FOR RECIPIENT") > 0 or start2[i].count("E&OE ") > 0):
                        start3.append(start2[i])

        if len(start3) == 0:
            # print("Parlegggggg")
            for ind, item in enumerate(name_found):


                    index_add = invoice_string1.index(name_found[ind])

                    # print(index_add)
                    # print(invoice_string1[index_add:index_add + 15])
                    x = invoice_string1[index_add:index_add + 15]
                    # print(x)
                    word = ["CORPORATION", "Corporation", "CO.", "CO", "Limited", "LIMITED", "LTD.", "LTD", "Ltd.", "Ltd",
                            "Ltd "]
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
        # print('name caps')
        # print(string_add)
        var = string_add
        # name_find.append(var)
        # name_find.append(ind)
        dic['vendor_caps'].append(var)
        if len(dic['vendor_caps'])>0:

            dic['Vendor Name'].append(var)
        return dic
    except:
        print("Vendor name not found")







def add_parsser_buyer(invoice_string, regex_expression, dic=dict_var()):
    try:

        #print(invoice_string)
        #can use the logic of co-ordinate
        name_found=[]
        # print("inside buyer")
        # FUTURE purpose separate shipto and billto address
        name_found7 = re.findall("(\\bName\\b)", invoice_string, re.IGNORECASE)
        # Include co-ordinate logic where it is not returning anything
        name_found9 = re.findall("(\\bAdd\\b)",invoice_string,re.IGNORECASE)
        #name_found3 = re.findall("(Shipping_address)",invoice_string,re.IGNORECASE)
        name_found4 = re.findall("(Billing_address)",invoice_string,re.IGNORECASE)
        #name_found5 = re.findall("(Shipto_address)",invoice_string,re.IGNORECASE)
        name_found6 = re.findall("(Billto_address)",invoice_string,re.IGNORECASE)
        name_found1 = re.findall("(Billed to)", invoice_string, re.IGNORECASE)
        #name_found8 = re.findall("(Shipped to)", invoice_string, re.IGNORECASE)

        name_found2 = re.findall("(Receiver)", invoice_string, re.IGNORECASE)
        #name_found10 = re.findall("(\\bBuyer:\\b)", invoice_string, re.IGNORECASE)
        name_found11 = re.findall("(\\bBuyer \\()", invoice_string, re.IGNORECASE)

        name_found12 = re.findall("(Buyer)", invoice_string, re.IGNORECASE)
        name_found13 = re.findall("(\\bAddress\\b)", invoice_string, re.IGNORECASE)

        name_found= name_found1+name_found2+name_found4 +name_found6+name_found7+name_found13+name_found11+name_found12+name_found9

        # print(name_find)
        # print("Printing full text")
        # print(words_text)
        # print("In add buyer")
        # print(name_found)


        # print(string2[1])
        name_find = []
        string_final_add=[]
        # print("khuda bharose")
        for ind, item in enumerate(name_found,start=0):
            # print("Printing name_found moin")
            # print(name_found[ind])
            string_buyer=name_found[ind]
            index_buyer=invoice_string.index(string_buyer)
            string_final_buyer=invoice_string[index_buyer:index_buyer+25]
            # print(string_final_buyer)
            if name_found.count("Name")>0 and name_found.count("Billed to")==0:
                index_add = invoice_string.index("Name")
                temp = index_add + 150
                string_add = invoice_string[index_add + 7:temp]
                string_final_name = string_add.split("\n")
                pin_find = re.findall('\\b[1-9]{1}[0-9]{2}[0-9]{3}\\b', string_add, re.IGNORECASE)
                # print(invoice_string)
                # print(pin_find)
                if len(pin_find)>0:

                    if len(dic['name']) == 0:
                        dic['name'].append(string_final_name[0])


                    index_pin = invoice_string.index(pin_find[0])
                    # print(index_pin)
                    # print(string_add)

                    string2 = invoice_string[index_add:index_pin + 7]
                    # print('helloooooo maroof')
                    # print(string2)
                    # print(type(string2))
                    string3 = string2.splitlines()
                    # print(string3)
                    string4 = str(string3)
                    # print(string4)
                    string5 = string4.replace("'", "").replace("[", "").replace("]", "")
                    # print("Hiii String5555")
                    # print(string5)
                    if string5.count(":") > 0:

                        string_final_add = string5.split(":")
                        var = string_final_add[2]
                        # print(string_final_add)
                    # string3 = string2[1].split("\n")
                    # print(string3)
                    else:
                        var = string_final_add

                    # var = string_final_add[1]
                    # print('bangkok massage therapy')
                    # print("Printing variable")
                    # print(var)
                    # name_find.append(var)
                    # name_find.append(ind)
                    dic['add'].append(var)
            elif not(string_final_buyer.count("Buyer's Order No")>0):
                # print("In buyer order no")
                # print(name_found[ind])
                # print(invoice_string)
                index_add = invoice_string.index(name_found[ind])
                # print("Code chal jaa plzzzzz")
                # print(index_add)

                res = index_add + 160
                # print(string_name)
                temp = index_add + 60
                string_add = invoice_string[temp:res]
                # print('address printing')
                # print(string_add)
                # print("in add parser")
                # print(string_add)
                # print(type(string_add))
                pin_find = re.findall('\\b[1-9]{1}[0-9]{2}[0-9]{3}\\b', string_add,re.IGNORECASE)
                # if len(pin_find)<1:
                #     pin_find=pin_find = re.findall('\\b[1-9]{1}[0-9]{2}[0-9]{2}\\b', string_add,re.IGNORECASE)
                # print(pin_find)
                if len(pin_find)>0:


                    temp1 = index_add + 12
                    string_name = invoice_string[temp1:temp1 + 48]
                    # print('naam aarela hain')
                    # print(string_name)
                    string_clean_name = string_name.replace("'", "").replace("[", "").replace("]", "")
                    string_final_name = string_clean_name.split("\n")
                    # print("Name")
                    # print(string_final_name)
                    if len(dic['name'])==0:
                        dic['name'].append(string_final_name[1])


                    # print(dic['name'])
                    # print("Printing dict elem")
                    # print('bangkok massage therapy')
                    # print(dic['name'][2])

                    # print(pin_find[0])
                    index_pin=invoice_string.index(pin_find[0])
                    # print(index_add)
                    # print(index_pin)
                    # print(invoice_string[index_add])
                    # print(invoice_string[index_pin])
                    # print(index_pin)
                    # print(string_add)

                    string2 = invoice_string[index_add:index_pin+7]
                    # print('helloooooo maroof')
                    # print(string2)
                    # print(type(string2))
                    string3 = string2.splitlines()
                    # print(string3)
                    string4 = str(string3)
                    # print(string4)
                    string5 = string4.replace("'","").replace("[","").replace("]","")
                    # print("Hiii String5555")
                    # print(string5)
                    if string5.count(":")>0:

                        string_final_add=string5.split(":")
                        var = string_final_add[1]
                        # print(string_final_add)
                    #string3 = string2[1].split("\n")
                    #print(string3)
                    else:
                        var = string_final_add

                    # var = string_final_add[1]
                    # print('bangkok massage therapy')
                    # print("Printing variable")
                    # print(var)
                    # name_find.append(var)
                    # name_find.append(ind)
                    dic['add'].append(var)
                else:
                    temp1 = index_add + 12
                    string_name = invoice_string[temp1:temp1 + 48]
                    string_final_name=string_name.split('\n')
                    # print("alag alag line par")
                    # print(string_final_name)
                    # print('bangkok adventures')
                    # print(string_name)

                    if len(dic['name'])==0:
                        dic['name'].append(string_final_name[1])
                    # print("Name checkk")
                    # print(dic['name'])
                    res = index_add + 130
                    temp = index_add + 40

                    string_add = invoice_string[temp:res]
                    # print(string_add)
                    string3 = string_add.splitlines()
                    # print(string3)
                    string4 = str(string3)
                    # print(string4)
                    string5 = string4.replace("'", "").replace("[", "").replace("]", "")
                    # print('string 5 error')
                    var = string5
                    dic['add'].append(var)


            # print(len(dic['name']))
            new_list=[]
            if len(dic['name'])>2:
                for i in range(0,len(dic['name'])):
                    if dic['name'][i] != " ":
                        # print("hello")
                        new_list.append(dic['name'][i])      #flaw in logic

                        # print(new_list)
                    else:
                        print(dic['name'])
            for i  in range(len(new_list)):
                dic['name'][i] = new_list[i]
                dic['name'][i] = new_list[i]
        # print("Checkkk")
        # print(dic['name'])

        if len(dic['name'])==1:
            dic['BillTo Name'].append(dic['name'][0])
            # if len(dic['name']) > 1:
            #     dic['ShipTo Name'].append(dic['name'][1])

        if len(dic['add']) > 0:
            dic['BillTo Address'].append(dic['add'][0])

            # if len(dic['add']) >1:
            #     dic['ShipTo Address'].append(dic['add'][1])


        return dic
    except:
        print("Buyer address not found")

def add_parsser_receiver(invoice_string, regex_expression, dic=dict_var()):
    try:
        #print(invoice_string)
        # print("Inside receiver")
        name_found=[]
        # FUTURE purpose separate shipto and billto address
        # Include co-ordinate logic where it is not returning anything


        name_found3 = re.findall("(Delivery Details)", invoice_string, re.IGNORECASE)
        # name_found2 = re.findall("(\\bName\\b)", invoice_string, re.IGNORECASE)
        # Include co-ordinate logic where it is not returning anything
        name_found1 = re.findall("(\\bAdd\\b)", invoice_string, re.IGNORECASE)
        #name_found2 = re.findall("(\\bAdd\\b)",invoice_string,re.IGNORECASE)
        name_found4 = re.findall("(Shipping_address)",invoice_string,re.IGNORECASE)
        #name_found4 = re.findall("(Billing_address)",invoice_string,re.IGNORECASE)
        name_found5 = re.findall("(Shipto_address)",invoice_string,re.IGNORECASE)
        #name_found6 = re.findall("(Billto_address)",invoice_string,re.IGNORECASE)
        #name_found7 = re.findall("(Billed to)", invoice_string, re.IGNORECASE)
        #name_found8 = re.findall("(Shipped to)", invoice_string, re.IGNORECASE)

        #name_found9 = re.findall("(Receiver )", invoice_string, re.IGNORECASE)
        #name_found10 = re.findall("(\\bBuyer:\\b)", invoice_string, re.IGNORECASE)
        name_found11 = re.findall("(Consignee)", invoice_string, re.IGNORECASE)
        name_found12 = re.findall("(Consignes)", invoice_string, re.IGNORECASE)
        #name_found13 = re.findall("(\\bAddress\\b)", invoice_string, re.IGNORECASE)

        name_found= name_found1+name_found3+name_found4+ name_found5 +name_found11+name_found12

        # print(name_find)
        # print("Printing full text")
        # print(words_text)
        # print("In add receiver")
        # print(name_found)

        # print(string2[1])
        name_find = []
        string_final_add=[]
        for ind, item in enumerate(name_found,start=0):

            index_add = invoice_string.index(name_found[ind])
            # print("Code chal jaa plzzzzz")
            # print(index_add)
            res = index_add + 160
            # print(string_name)
            temp = index_add
            string_add = invoice_string[temp:res]
            # print('address printing')
            # print("in add parser")
            # print('moin final string')
            # print(string_add)
            # print(type(string_add))
            pin_find = re.findall('\\b[1-9]{1}[0-9]{2}[0-9]{3}\\b', string_add,re.IGNORECASE)
            # print("found pin code")
            # print(pin_find)
            if len(pin_find)>0:
                temp = index_add-40
                string_temp = invoice_string[temp:index_add]
                # print("Success")
                # print(string_temp)
                if string_temp.count("Name")>0:
                    # print("Success")
                    var = invoice_string.index("Name")
                    res = var + 6
                    string_final_name = invoice_string[res:index_add]
                    dic['name'].append(string_final_name)

                    index_pin = invoice_string.index(pin_find[0])
                    # print(index_pin)
                    # print(string_add)

                    string2 = invoice_string[index_add:index_pin + 7]
                    # print('helloooooo maroof')
                    # print(string2)
                    # print(type(string2))
                    string3 = string2.splitlines()
                    # print(string3)
                    string4 = str(string3)
                    # print(string4)
                    string5 = string4.replace("'", "").replace("[", "").replace("]", "")
                    # print("Hiii String5555")
                    # print(string5)
                    if string5.count(":") > 0:

                        string_final_add = string5.split(":")
                        var = string_final_add[1]
                        # print("Hiiiiiiii")
                        # print(var)
                    # string3 = string2[1].split("\n")
                    # print(string3)
                    else:
                        var = string5

                    # var = string_final_add[1]
                    # print("Printing variable")
                    # print(var)
                    # name_find.append(var)
                    # name_find.append(ind)
                    dic['add_receiver'].append(var)
                else:


                    temp1 = index_add + 12

                    # print("inside pin")
                    string_name = invoice_string[temp1:temp1 + 50]
                    # print(string_name)
                    string_clean_name = string_name.replace("'", "").replace("[", "").replace("]", "")
                    string_final_name=string_clean_name.split('\n')

                    dic['name'].append(string_final_name[1])
                    # print("Printing dict elem")
                    # print(dic['name'][2])


                    index_pin=invoice_string.index(pin_find[0])
                    # print(index_pin)
                    # print(string_add)

                    string2 = invoice_string[index_add:index_pin+7]
                    # print('helloooooo maroof')
                    # print(string2)
                    # print(type(string2))
                    string3 = string2.splitlines()
                    # print(string3)
                    string4 = str(string3)
                    # print(string4)
                    string5 = string4.replace("'","").replace("[","").replace("]","")
                    # print("Hiii String5555")
                    # print(string5)
                    if string5.count(":")>0:

                        string_final_add=string5.split(":")
                        var = string_final_add[1]
                        # print("Hiiiiiiii")
                        # print(var)
                    #string3 = string2[1].split("\n")
                    #print(string3)
                    else:
                        var = string5

                    # var = string_final_add[1]
                    # print("Printing variable")
                    # print(var)
                    # name_find.append(var)
                    # name_find.append(ind)
                    dic['add_receiver'].append(var)
            else:
                temp1 = index_add
                string_name = invoice_string[temp1:temp1 + 54]
                # print("semifinal name aarela hain")
                # print(string_name)
                string_final_name=string_name.split('\n')
                # print('final name aarela ain')
                # print(string_final_name)
                dic['name'].append(string_final_name[1])
                res = index_add + 130
                temp = index_add + 40

                string_add = invoice_string[temp:res]
                string3 = string_add.splitlines()
                # print(string3)
                string4 = str(string3)
                # print(string4)
                string5 = string4.replace("'", "").replace("[", "").replace("]", "")
                var = string5
                dic['add_receiver'].append(var)


        # print(len(dic['name']))
        new_list=[]
        if len(dic['name'])>2:
            for i in range(0,len(dic['name'])):
                if dic['name'][i] != " ":
                    # print("naam batao")
                    # print(dic['name'][i])
                    new_list.append(dic['name'][i])     #flaw in logic

                    # print(new_list)
                else:
                    # print('name coming')
                    print(dic['name'])
        for i  in range(len(new_list)):
            dic['name'][i] = new_list[i]
            dic['name'][i] = new_list[i]

        # if len(dic['name']) > 0:
        #     dic['BillTo Name'].append(dic['name'][0])
        if len(dic['name']) > 1:
            dic['ShipTo Name'].append(dic['name'][1])

        # if len(dic['add']) > 0:
        #     dic['BillTo Address'].append(dic['add'][0])

        if len(dic['add_receiver']) > 0:
            dic['ShipTo Address'].append(dic['add_receiver'][0])


        return dic
    except:
        print("Receiver address not found")


def invoice_parsser(invoice_string, regex_expression, dic=dict_var()):
    #TO BE CONTINUED
    try:
        # print('inside invoice')
        invoice_found = re.findall(regex_expression['regex_invoice'],invoice_string,re.IGNORECASE)
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
            res = index1 - 15
            string1 = invoice_string[res:index1]
            string2 = "Invoice No"
            if (string1.count(string2)>0):

                invoice_find = re.search('[A-Z]{0,5}\d{10}', item)
                # print(invoice_find)

                if invoice_find is not None:
                    # extract the amount and score it at the same time
                    #score = scoring(regex_date, item.lower())
                    invoice = invoice_find.group(0).replace(',', '')

                    # appending values into the dictionary
                    dic['invoice'].append(invoice)

        # text = "GSTIN No"

        # text_instances = page.searchFor(text)
        # # print(text_instances)
        # rect2 = text_instances[0]
        # x1 = rect2[0]
        # y1 = rect2[1]+10
        # x2 = rect2[2] + int(50)
        # y2 = rect2[3] + 10
        # # print(x1)
        # # print(x2)
        # # print(rect2)
        # words = page.getText('words')
        # rect1 = fitz.Rect(x1, y1, x2, y2)
        # mywords = [w for w in words if fitz.Rect(w[:4]).intersects(rect1)]
        # # print(mywords)
        # # text1 = make_text(mywords)
        # # text2 = text1.split()

        # text1 = make_text(mywords)
        # # print("IN invoice")
        # # print(type(text1))
        # invoice_find.append(text1)

        # dic['invoice'].append(text1)

                if len(dic['invoice'])>0:
                    dic['External Invoice No'].append(invoice)


        return dic
    except:
        print("Invoice No not found")



def return_header_data(path):
    doc = fitz.open(path)  # any supported document type
    print("Path : " , path)
    page = doc[0]  # we want text from this page

    rect1 = fitz.Rect(36, 11, 800, 3000)
    words = page.getText("words")

    words_text = page.getText("text")



    dateregex = {'regex_date': '([0-9]{2}.[0-9]{2}.[0-9]{4})'}
    gstregex = {'regex_gst': '(\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1})'}
    sapregex = {'regex_sap': '(\d{10})'}
    invoiceregex = {'regex_invoice': '([A-Z]{0,5}\d{10})'}
    panregex = {'regex_pan': '(\\b([A-Z]{5}[0-9]{4}[A-Z]{1})\\b)'}
    vehicleregex = {'regex_vehicle': '[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}'}
    nameregex = {'regex_name': '\\b(NAME|VENDOR Name):\s+(\S.*?)\s{3}\\b'}
    addregex={'regex_add':'(Add)|(Address)|(Billing Address)|(Shipping Address)|(Ship_to)|(Bill_to)'}

    # print("Words Text : ",words_text)
    dic = dict_var()
    result_dic = gst_parsser(words_text, gstregex, dic)
    result_dic = invoice_parsser(words_text, invoiceregex, dic)
    result_dic = pan_parsser(words_text, panregex, dic)
    result_dic = vehicle_parsser(words_text, vehicleregex, dic)
    result_dic = date_parsser(words_text, dateregex, dic)
    # result_dic = name_parsser(words_text, nameregex, dic)
    #result_dic = add_parsser(words_text, nameregex, dic)

    result_dic = add_parsser_buyer(words_text, nameregex, dic)
    result_dic=add_parsser_receiver(words_text,nameregex,dic)
    result_dic = vendor_add_parsser(words_text, nameregex, dic)
    # result_dic = vendor_name_parsser(words_text, dic)
    result_dic = vendor_caps_parsser(words_text,nameregex, dic)


    #result_dic = check_add_parsser(words_text, nameregex, dic)

    result_dic = categories(words_text, dic)



    try:
        del[result_dic['category']]
        del[result_dic['amount']]
        del[result_dic['score']]
        del[result_dic['tax']]
        del[result_dic['gst']]
        del[result_dic['sap']]
        del[result_dic['invoice']]
        del[result_dic['pan']]
        del[result_dic['vehicle']]
        del[result_dic['name']]
        del[result_dic['add']]
        del[result_dic['vendor_add']]
        del[result_dic['check_add']]
        del[result_dic['vendor_caps']]
        del[result_dic['date']]
        del[result_dic['add_receiver']]


    except:
        print("OK")

    # print(words_text)
    # print(" ************************************************Result Dictionary ******************************")
    # print(result_dic)


    df = pd.DataFrame.from_dict(result_dic, orient = 'index')

    df = df.transpose()

    df2 = df.columns.tolist()
    df3 = df.values.tolist()

    


    header_message = 'Header Details Extracted...............................100%'

    
    print(header_message)
   

    return df2, df3

# dff1,dff2 = return_header_data("IB20.pdf")
# print(dff1)
# print("Details........................................")
# print(dff2)

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
