import re
from sqlite3.dbapi2 import Cursor
import struct
from flask import *
import os
import sys
import hashlib
import pandas as pd
import shutil
import base64
from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport


# To hide the tensorflow warnings

import time
start = time.time();

# All the imports
from pdf_extract_model.format_conversion.pdf_plumber_convert import get_actual_path
from pdf_extract_model.table_detection.table_extract import detect_all_pages, detect_single_page, detect_multiple_pages, merge_columns,optimize_rotation
from pdf_extract_model.pdf_utility_function.pdf_functions import get_file_ext,get_PDF_Pages
from pdf_extract_model.template_extraction.export_template import send_all_to_template
from pdf_extract_model.date_time.get_date_time_instance import get_date_time
from pdf_extract_model.header_details.header_details_extract import return_header_data
from pdf_extract_model.emails.email_import import save_pdf_attachments
from pdf_extract_model.language_currency.get_language_database import get_language_list
from pdf_extract_model.database_connection.database_connect import database_conn
import pandas as pd
import os
import sqlite3
import os





t_x  =  time.time()-start;



#Main Calling of the Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')




# Deleteing the Cache from the website
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r





#Routing for home
@app.route('/')
def home():
    return render_template('index.html', title='Home', time=t_x)



# Routing for exporting all to template
@app.route('/export_all_to_template', methods=['POST','GET'])
def export_all_to_template():
    req = request.get_json()
    val = send_all_to_template(req['pdf_file_name'],req['merge_list'], req['no_of_tables'],req['header_details'],req['page_list'], req['checksum'],req['structure_type'],req['language'])
    val = jsonify(val)
    return val


@app.route('/import_to_sap/<file_name>')
def import_to_sap(file_name):
    print(f'successfully send file {file_name}')

    # copy to tmp 
    path_of_pdf_source = 'C:\\flask_model\\uploads\\modify_file.pdf'
    path_of_excel_source = 'C:\\flask_model\\integrated_header_template.xlsx'

    file_name_pdf = file_name
    file_name = os.path.splitext(file_name)[0]

    file_name_excel = file_name + '.' +'xlsx'

    path_of_pdf_dest = 'C:\\temp\\' + file_name_pdf
    path_of_excel_dest = 'C:\\temp\\' + file_name_excel

    shutil.copy(path_of_pdf_source, path_of_pdf_dest)
    shutil.copy(path_of_excel_source, path_of_excel_dest)

    # pdf = file_name_pdf #Enter PDF file path
    # xl = file_name_excel #Enter excel file path


# ******************************SAOP WSDL PART*********************************************
    # data1 = open(pdf, 'rb').read()
    # base64_encoded_pdf = base64.b64encode(data1).decode('UTF-8')

    # data2 = open(xl, 'rb').read()
    # base64_encoded_xl = base64.b64encode(data2).decode('UTF-8')

    session = Session()
    session.verify = False
    # session.auth = HTTPBasicAuth("chintang", "Ey@123456789")
    session.auth = HTTPBasicAuth("EY_VIM", "Ey@123456789")
    # client = Client('http://euwdrh201fl01.SPRADV.SBP.LOCAL:8001/sap/bc/srt/wsdl/flv_10002A111AD1/bndg_url/sap/bc/srt/rfc/sap/zeyocr_upload_files_name/200/zeyocr_upload_files_name/zeyocr_upload_files_name?sap-client=200',
    #client = Client('http://SCLS4QAPP.MEHTAGROUP.COM:8000/sap/bc/srt/wsdl/flv_10002A111AD1/bndg_url/sap/bc/srt/rfc/sap/zeyocr_upload_files_name/500/zeyocr_upload_files_name/zeyocr_upload_files_name?sap-client=500',
    client = Client('http://SCLS4QAPP.MEHTAGROUP.COM:8000/sap/bc/srt/wsdl/flv_10002A111AD1/bndg_url/sap/bc/srt/rfc/sap/zeyocr_upload_files_name/500/default_service/new_binding?sap-client=500',
    transport=Transport(session=session) )
    # print(client.service.ZEYOCR_UPLOAD_FILES_NAME(base64_encoded_pdf,base64_encoded_xl))
    print(client.service.ZEYOCR_UPLOAD_FILES_NAME(file_name_pdf,file_name_excel))
    
    return render_template('sap_success.html',title='success')






# Importing files from outlook email
@app.route('/records')
def import_from_email():
    path = os.path.join(app.root_path, 'uploads')
    list_of_attachments,list_of_date,list_of_time = save_pdf_attachments("Indian Oil Test Invoice",path) #Function call from email.py
    save_path_old = 'uploads/' #Specifying path
    mypath = save_path_old
    dateStr,timeStr = get_date_time()
    list_of_md5 = []
    print("Creating Checksums this may take a while........................................100%")
    

    for i in range(len(list_of_attachments)):
        md5_retruned = ''
        with open('uploads/'+list_of_attachments[i],encoding="cp437") as file_to_check:
            data = file_to_check.read()
            md5_retruned = hashlib.md5(data.encode("cp437")).hexdigest()
            list_of_md5.append(md5_retruned)
        
        language = 'en'
        create_email_database(email_date=list_of_date[i],email_time=list_of_time[i],import_date=dateStr,import_time=timeStr,pdf_name=list_of_attachments[i],checksum=list_of_md5[i],language=language)
    

    conn = sqlite3.connect('LOGSQAS.db')
    cursor  = conn.cursor()
    cursor.execute(""" SELECT * from email_table ORDER BY pdf_id DESC """)
    email_row = cursor.fetchall() 
    language_list = get_language_list()
    return render_template('email_invoices.html',title='Email Invoices',rows = email_row , data=language_list)


@app.route('/email')
def import_direct_email():
    conn = sqlite3.connect('LOGSQAS.db')
    cursor  = conn.cursor()
    cursor.execute(""" SELECT * from email_table ORDER BY pdf_id DESC """)
    email_row = cursor.fetchall()
    language_list = get_language_list()
    return render_template('email_invoices.html',title='Email Invoices',rows = email_row ,data=language_list)

@app.route('/<int:id>/scan/', methods=['POST','GET'])
def scan(id):
    # print("===========================================================")
    # print(id)
    lang = request.form.get('comp_select')
    print(f'The language is {lang}')
    pdf_id = id
    cursor,conn = database_conn()
    sql_scan_pdf = """ SELECT pdf_name FROM email_table where pdf_id=? """
    cursor.execute(sql_scan_pdf,(pdf_id,))
    pdf_name_rows = cursor.fetchall()
    pdf_file_name = pdf_name_rows[0][0]
    print(f'The PDF File Name is {pdf_file_name}')
    language =  lang
    save_path = 'uploads//' + pdf_file_name
    structure = 'stream'
    structure_type = '1'
    option = '2'
    file_ext = get_file_ext(save_path)
    optimize_rotation(save_path)
    save_path = "uploads//" + "modify_file.pdf"
    d_file = pdf_file_name.rstrip('.pdf').rstrip('.jpeg').rstrip('.jpg')

    md5_returned = ''
    with open(save_path, encoding="cp437") as file_to_check:
        data = file_to_check.read()  
        # read contents of the file
        md5_returned = hashlib.md5(data.encode("cp437")).hexdigest()

    if option == '2':
        no_of_pages = get_PDF_Pages(save_path)
        pagelist = [int(i) for  i in range(1,int(no_of_pages) + 1)]
        start = pagelist[0]
        end = pagelist[-1]
        sqlite_null_query = """ SELECT * from log_table """
        cursor.execute(sqlite_null_query)
        result = cursor.fetchall()

        if(len(result) == 0):
            x = get_actual_path(save_path)
            df_header_cols , df_header_vals = return_header_data(x)
            list_of_df, length_of_df = detect_all_pages(x,structure_type)

            column_names = []
            for df_item in list_of_df:
                column_names.append(df_item.columns.values)

            row_data = []
            for df_data in list_of_df:
                row_data.append(list(df_data.values.tolist()))

        else:
            sqlite_checksum_query = """ SELECT pdf_data,header_details from log_table where checksum=(?) AND start<=(?) AND end>=(?) AND structure=(?) AND log_id IN ( SELECT max(log_id) FROM log_table GROUP BY checksum HAVING checksum=(?) )  """
            cursor.execute(sqlite_checksum_query,(md5_returned , start , end , structure, md5_returned,))
            result_row = cursor.fetchall()

            if(len(result_row) == 0):
                x = get_actual_path(save_path)
                df_header_cols , df_header_vals = return_header_data(x)
                list_of_df, length_of_df = detect_all_pages(x,structure_type)

                column_names = []
                for df_item in list_of_df:
                    column_names.append(df_item.columns.values)

                row_data = []
                for df_data in list_of_df:
                    row_data.append(list(df_data.values.tolist()))
            
            else:
                print(" **************************************** Table Already exists *******************************")
                header_details_json = json.loads(result_row[0][1])
                df_header_cols = header_details_json[0]
                df_header_vals = [header_details_json[1]]



                list_of_df = []
                for i in range(start-1,end):
                    result_row_json = json.loads(result_row[0][0])
                    print(" @@@@@@@@@@@ custom @@@@@@@@@@@@@")
                    df = pd.DataFrame.from_dict(result_row_json[i])
                    df = df.iloc[: , 1:]
                    print(df)
                    list_of_df.append(df)

                length_of_df = len(list_of_df)
                
                column_names = []
                for df_item in list_of_df:
                    column_names.append(df_item.columns.values)

                row_data = []
                for df_data in list_of_df:
                    row_data.append(list(df_data.values.tolist()))

        j = render_template("multiple_pages_success.html", column_names=column_names, state='multiple',
                            no_of_pages=no_of_pages, file_ext="PDF",
                            row_data=row_data, zip=zip, len=length_of_df, title='Records', selected_pages=no_of_pages,name=pdf_file_name, d_name = d_file , pdf_file_name = pdf_file_name,header_columns = df_header_cols , header_values = list(df_header_vals) ,pagelist = pagelist, checksum = md5_returned,structure_type = structure_type,language = language )

    return j

# display of records in df form function
@app.route('/display', methods=['POST','GET'])
def multiple_pages_success():
    global j
 
    if request.method == 'POST':
        option = request.form['options']
        f = request.files['file']
        # structure = request.form['myStructure']
        language = request.form['language']


        structure = 'stream'
        if structure == 'stream':
            structure_type = '1'
        else:
            structure_type = '2'
        

        save_path = 'uploads/' + f.filename
        f.save(save_path)
        file_ext = get_file_ext(save_path)   
        optimize_rotation(save_path)
        save_path = "uploads//" + "modify_file.pdf"
      #  optimize_rotation(save_path)
        d_file = f.filename.strip('.pdf').strip('.jpeg').strip('.jpg')
        pdf_file_name = f.filename
        md5_returned = ''
        with open(save_path, encoding="cp437") as file_to_check:
            data = file_to_check.read()  
            # read contents of the file
            md5_returned = hashlib.md5(data.encode("cp437")).hexdigest()        
        cursor,conn = database_conn()



        if option == '1':

            p = request.form['which-page']
            check_page = int(p)
            start = check_page
            end = check_page
            pagelist = [check_page]
            no_of_pages = get_PDF_Pages(save_path)


        

            # create_database()
            sqlite_null_query = """ SELECT * from log_table """
            cursor.execute(sqlite_null_query)
            result = cursor.fetchall()

            if len(result)==0:

                x = get_actual_path(save_path)
                no_of_pages = get_PDF_Pages(x)
                df_header_cols , df_header_vals = return_header_data(x)
                df = detect_single_page(x, p, structure_type)

            else:
                sqlite_checksum_query = """ SELECT pdf_data,header_details,start from log_table where checksum=(?) AND start<=(?) AND end>=(?) AND structure=(?) AND log_id IN ( SELECT max(log_id) FROM log_table GROUP BY checksum HAVING checksum=(?) ) """
                cursor.execute(sqlite_checksum_query,(md5_returned , start , end, structure, md5_returned,))
                result_row = cursor.fetchall()
               
                if(len(result_row) == 0):
                    x = get_actual_path(save_path)
                    no_of_pages = get_PDF_Pages(x)
                    df_header_cols , df_header_vals = return_header_data(x)
                 
                    df = detect_single_page(x, p,structure_type)


                else:
                    print("++++++++++++++++++++++++++++++++yes data exists+++++++++++++++++++++++++++++++++++++++++")

                    # pagelist = [check_page]
                    # print(result_row[0])
                    # df = detect_single_page(x, p)

                    header_details_json = json.loads(result_row[0][1])
                    database_start = json.loads(result_row[0][2])
                    print(" ############################################3 Database Start ############################################### ")
                    print("Type of database start ",type(database_start))
                    print(database_start)

                    df_header_cols = header_details_json[0]
                    df_header_vals = [header_details_json[1]]
                    print(df_header_vals)
                    

                    result_row_json = json.loads(result_row[0][0])
                    # print(result_row_json)
                    print(" ****RRJ *****")
                    diff = database_start-1
                    for i in range(start-1,end):
                        df = pd.DataFrame.from_dict(result_row_json[i-diff])
                        df = df.iloc[:, 1:]
                    
                    
         
                    print(df.values.tolist())




            

            
            j = render_template("multiple_pages_success.html", state='single', name=f.filename, column_names=df.columns.values,
                                no_of_pages=no_of_pages, file_ext=file_ext,
                                row_data=list(df.values.tolist()), len=1, zip=zip,
                                title='Records',selected_pages=1,page_number=p, d_name = d_file ,pdf_file_name = pdf_file_name, header_columns = df_header_cols , header_values = list(df_header_vals), pagelist = pagelist, checksum = md5_returned ,structure_type = structure_type,language = language)


        elif option == '2':
            no_of_pages = get_PDF_Pages(save_path)
            pagelist = [int(i) for  i in range(1,int(no_of_pages) + 1)]

            start = pagelist[0]
            end = pagelist[-1]

            # create_database()


            sqlite_null_query = """ SELECT * from log_table """
            cursor.execute(sqlite_null_query)
            result = cursor.fetchall()

            if(len(result) == 0):

                x = get_actual_path(save_path)
                
                df_header_cols , df_header_vals = return_header_data(x)



                list_of_df, length_of_df = detect_all_pages(x,structure_type)
                column_names = []


                for df_item in list_of_df:
                    column_names.append(df_item.columns.values)
                row_data = []
                for df_data in list_of_df:
                    row_data.append(list(df_data.values.tolist()))
              

            else:
                sqlite_checksum_query = """ SELECT pdf_data,header_details from log_table where checksum=(?) AND start<=(?) AND end>=(?) AND structure=(?) AND log_id IN ( SELECT max(log_id) FROM log_table GROUP BY checksum HAVING checksum=(?) )  """
                cursor.execute(sqlite_checksum_query,(md5_returned , start , end , structure, md5_returned,))
                result_row = cursor.fetchall()

                if(len(result_row) == 0):
                    x = get_actual_path(save_path)
                
                    df_header_cols , df_header_vals = return_header_data(x)



                    list_of_df, length_of_df = detect_all_pages(x,structure_type)
                    column_names = []


                    for df_item in list_of_df:
                        column_names.append(df_item.columns.values)
                    row_data = []
                    for df_data in list_of_df:
                        row_data.append(list(df_data.values.tolist()))

                else:
                    print(" **************************************** Table Already exists *******************************")

                    header_details_json = json.loads(result_row[0][1])

                    df_header_cols = header_details_json[0]
                    df_header_vals = [header_details_json[1]]



                    list_of_df = []
                    for i in range(start-1,end):
                        result_row_json = json.loads(result_row[0][0])
                        print(" @@@@@@@@@@@ custom @@@@@@@@@@@@@")
                        df = pd.DataFrame.from_dict(result_row_json[i])
                        df = df.iloc[: , 1:]
                        print(df)
                        list_of_df.append(df)

                    length_of_df = len(list_of_df)
                    column_names = []
                    for df_item in list_of_df:
                        column_names.append(df_item.columns.values)

                    row_data = []
                    for df_data in list_of_df:
                        row_data.append(list(df_data.values.tolist()))

            j = render_template("multiple_pages_success.html", column_names=column_names, state='multiple',
                                no_of_pages=no_of_pages, file_ext="PDF",
                                row_data=row_data, zip=zip, len=length_of_df, title='Records', selected_pages=no_of_pages,name=f.filename, d_name = d_file , pdf_file_name = pdf_file_name,header_columns = df_header_cols , header_values = list(df_header_vals) ,pagelist = pagelist, checksum = md5_returned,structure_type = structure_type,language = language )


        elif option == '3':
            s = request.form['start-page']
            e = request.form['end-page']

            no_of_pages = get_PDF_Pages(save_path)

  
            
            c_start = int(s)
            c_end = int(e)
            pagelist = [int(i) for i in range(c_start,c_end+1)]

            start = pagelist[0]
            end = pagelist[-1]

            

            sqlite_null_query = """ SELECT * from log_table """
            cursor.execute(sqlite_null_query)
            result = cursor.fetchall()

            if(len(result) == 0):
                x = get_actual_path(save_path)
                no_of_pages = get_PDF_Pages(x)
                df_header_cols , df_header_vals = return_header_data(x)



                list_of_df, length_of_df = detect_multiple_pages(x, s, e,structure_type)
                column_names = []
                for df_item in list_of_df:
                    column_names.append(df_item.columns.values)

                row_data = []
                for df_data in list_of_df:
                    row_data.append(list(df_data.values.tolist()))



            else:
                sqlite_checksum_query = """ SELECT pdf_data,header_details,start from log_table where checksum=(?) AND start<=(?) AND end>=(?) AND structure=(?) AND log_id IN ( SELECT max(log_id) FROM log_table GROUP BY checksum HAVING checksum=(?) )  """
                cursor.execute(sqlite_checksum_query,(md5_returned , start , end, structure, md5_returned,))
                result_row = cursor.fetchall()
               

                if(len(result_row) == 0):
                    x = get_actual_path(save_path)
                    no_of_pages = get_PDF_Pages(x)
                    df_header_cols , df_header_vals = return_header_data(x)

                    list_of_df, length_of_df = detect_multiple_pages(x, s, e, structure_type)
                    column_names = []
                    for df_item in list_of_df:
                        column_names.append(df_item.columns.values)

                    row_data = []
                    for df_data in list_of_df:
                        row_data.append(list(df_data.values.tolist()))

                else:
                    print("***********Table Exists ********")

                    header_details_json = json.loads(result_row[0][1])
                    database_start = json.loads(result_row[0][2])
                    print(" ############################################3 Database Start ############################################### ")
                    print("Type of database start ",type(database_start))
                    print(database_start)


                    diff = database_start-1

                    df_header_cols = header_details_json[0]
                    df_header_vals = [header_details_json[1]]

                    list_of_df = []
                    for i in range(start-1,end):
                        result_row_json = json.loads(result_row[0][0])
                        print(" @@@@@@@@@@@ custom @@@@@@@@@@@@@")
                        df = pd.DataFrame.from_dict(result_row_json[i-diff])
                        df = df.iloc[: , 1:]
                        print(df)
                        list_of_df.append(df)

                    length_of_df = len(list_of_df)
                    column_names = []
                    for df_item in list_of_df:
                        column_names.append(df_item.columns.values)

                    row_data = []
                    for df_data in list_of_df:
                        row_data.append(list(df_data.values.tolist()))

          







  


            j = render_template("multiple_pages_success.html", column_names=column_names, state='range',
                                        no_of_pages=no_of_pages, file_ext=file_ext,
                                        row_data=row_data, zip=zip, len=length_of_df,  title='Records',selected_pages=int(e)-int(s) + 1,start_p = c_start,name=f.filename, d_name = d_file, pdf_file_name = pdf_file_name, header_columns = df_header_cols , header_values = list(df_header_vals), pagelist=pagelist,checksum = md5_returned ,structure_type = structure_type,language = language)
        
        return j




# Downloading the final excel file as attachement
@app.route('/final_download/<file_name>')
def final_download(file_name):
    print(f'the file name is {file_name} and file type is {type(file_name)}')
    excel_file_name = file_name.rstrip('pdf') + '.xlsx'
    return send_file('integrated_header_template.xlsx',as_attachment=True , cache_timeout=0,attachment_filename=excel_file_name)




@app.route('/logs')
def view_logs():
    conn = sqlite3.connect('LOGSQAS.db')
    cursor  = conn.cursor()
    cursor.execute(""" SELECT log_id,date,time,pdf_name,start,end,excel_name,total_cols,filled_cols,str_list FROM log_table ORDER BY log_id DESC """)
    log_row = cursor.fetchall()
    return render_template('logs.html',title='Logs',rows = log_row)



@app.route('/results/<id>')
def results(id):
    log_id = id
    print("+++++++++++++++++++++++++++++++++++++++++LOG ID++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(type(log_id))

    conn = sqlite3.connect("LOGSQAS.db")
    cursor = conn.cursor()
    sql_data_query = """ SELECT excel_data , excel_name from log_table WHERE log_id=? """
    cursor.execute(sql_data_query, (log_id,))
    final_result_rows = cursor.fetchall()
    final_result_rows_json = json.loads(final_result_rows[0][0])
    result_dataframe = pd.DataFrame.from_dict(final_result_rows_json)

    result_file_name = final_result_rows[0][1]
    result_dataframe.to_excel('final_log_result.xlsx')

    return send_file('final_log_result.xlsx',as_attachment=True, cache_timeout=0,attachment_filename=result_file_name)


    
    # return render_template('logs.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

#Error handling page
@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return render_template('error.html'), 500

def create_database():
    conn = sqlite3.connect('LOGSQAS.db')
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS log_table (log_id INTEGER PRIMARY KEY ,date TEXT , time TEXT, pdf_name TEXT,header_details TEXT, start TEXT , end TEXT ,pdf_data TEXT, excel_name TEXT, excel_data TEXT , checksum TEXT ) """)
    # cursor.execute(""" INSERT INTO log_table (date,time,pdf_name,header_details, start , end, pdf_data,excel_name,excel_data,checksum) VALUES (?,?,?,?,?,?,?,?,?,?) """, (date,time,pdf_name,header_details,start,end,pdf_data,excel_name,excel_data,checksum))
    conn.commit()
    cursor.close()
    conn.close()
    print("Table Created Successfully")


def create_email_database(email_date,email_time,import_date,import_time,pdf_name,checksum,language):
    cursor,conn = database_conn()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS email_table (pdf_id INTEGER PRIMARY KEY, email_date TEXT,email_time TEXT,import_date TEXT, import_time TEXT, pdf_name TEXT, checksum TEXT UNIQUE,language TEXT) """)
    cursor.execute(""" INSERT OR IGNORE INTO email_table (email_date,email_time,import_date,import_time,pdf_name,checksum,language) VALUES (?,?,?,?,?,?,?) """, (email_date,email_time,import_date,import_time,pdf_name,checksum,language))
    conn.commit()
    cursor.close()
    conn.close()
    print("emaildata inserted successfully")


if __name__ == '__main__':
    app.run(debug=True,host='192.168.10.157', port=5000)
    app.jinja_env.cache = {}    # Deleting the template cache
    session.close()
