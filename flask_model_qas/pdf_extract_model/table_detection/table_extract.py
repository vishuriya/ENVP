# pdf2image libraries for deep learning
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader
from pdf_extract_model.cleaning.dataframe_cleaning import cleaning_data
from pdf_extract_model.cleaning.dfc2 import cleaning_data2
from pdf_extract_model.table_detection.detect_table_model import detect_table_coords
from pdf_extract_model.pdf_utility_function.pdf_functions import bboxes_pdf,norm_pdf_page,pdf_page2img
import pytesseract
import PyPDF2
import numpy as np
import pandas as pd
import camelot
import regex as re
import os

# for reading images error free
try:
    from PIL import Image
except ImportError:
    print("Import error")
    import Image


# Imports pyTesseract, need to give proper path according to system
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
import os




# -----------------------------------------------------------------Detects table cordinates--------------------------------------------------------

def optimize_rotation(path):
    pdf_path = open(path, 'rb')
    pdf_reader = PdfFileReader(pdf_path,strict=False)
    pdf_writer = PyPDF2.PdfFileWriter()
    for pagenum in range(pdf_reader.numPages):
        deg = pdf_reader.getPage(pagenum).get('/Rotate')
        print("Page Number : ",pagenum+1)
        print("Degree of PageNumber" , deg)
        if deg == None: 
            print("PDF Orientation Checked No Rotation required of :" , pagenum+1)
            print(pagenum)
            page = pdf_reader.getPage(pagenum)    
        else:
            page = pdf_reader.getPage(pagenum)
            if deg == 180:
                print("Rotating page by 180 degree of ",pagenum+1)
                page.rotateClockwise(180)
            elif deg == 90:
                print("Rotating page by 90 degree in Anticlockwise of " , pagenum+1)
                page.rotateCounterClockwise(90)
            elif deg == 270:
                print("Rotating page by 90 in clockwise direction of ", pagenum+1)
                page.rotateClockwise(90)
            else:
                print("Rotating page by 0 degree CounterClockwise of ", pagenum+1)
                page.rotateCounterClockwise(0)
        print("--------------------------------------------------------------------")    
        pdf_writer.addPage(page)
    head,tail = os.path.split(path)
    print(f"The head is {head}")
    print(f"The tail is {tail}")
    out_path = tail.rstrip('.pdf') + '.pdf'
    out_path_dir = "uploads//" + "modify_file.pdf"
    pdf_out = open(out_path_dir, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_path.close()
    print("PDF Orientation Checked......................100%")





# function to get the output layer names 

# in the architecture


   
    


# ---------------------------------------------------------------Uses camelot on the pdf page for OCR-------------------------------------------------------
def text_based_pdf_extraction(x1, y1, x2, y2, img, pdf_page, pdf_file, pg,structure_type):


    if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0:
        try :

            out = camelot.read_pdf(filepath = pdf_file, pages = str(pg))
            x = out[0].df
            print("Table Found Lattice.........................100%")
        except:
            try :
                out = camelot.read_pdf(filepath = pdf_file, flavor='stream', pages = str(pg))
                x = out[0].df
                print("Table Found Stream.........................100%")

            except :     

                print("Table Not Detected..........................")
                x = [['Table was no Detected',''],['','']]
                x = pd.DataFrame(x)

    else:
        interesting_areas = []
     
        output = [[x1, y1, x2, y2]]
    
        for x in output:
            
            [m1, n1, m2, n2] = bboxes_pdf(img, pdf_page, x)
            
            bbox_camelot = [
                ",".join([str(m1), str(n1), str(m2), str(n2)])
            ][0]  # x1,y1,x2,y2 where (x1, y1) -> left-top and (x2, y2) -> right-bottom in PDF coordinate space
 
            interesting_areas.append(bbox_camelot)
      
        
        try:
            if structure_type == '1':
                output_camelot = camelot.read_pdf(filepath=pdf_file,  flavor='stream', table_areas=interesting_areas,pages=str(pg))
                
                
            else:
                
                output_camelot = camelot.read_pdf(filepath=pdf_file,  flavor='lattice', table_regions=interesting_areas,pages=str(pg))
            # print(output_camelot[0].df)
            print(f'Length of camelot variable is {len(output_camelot)}')
            x = output_camelot[0].df
        except:
            print("PDF has image table")
            x = [['PDF has image table',''],['','']]
            x = pd.DataFrame(x)

 
   


    # print(x)

    # if len(x.columns == 1):
    #     output_camelot_z = camelot.read_pdf(pdf_file, flavor='stream',pages=str(pg))
    #     size = len(output_camelot_z)
    #     print(f'The size of the camelot is {size}')
    #     print('Going inside the alternate function.............................')
    #     z = output_camelot_z[0].df
    #     print('===============================Inside the function===============================')
     
    #     x = z.copy()
        


   
    
    # set the header row as the df header
    x = x.values
    x = x.tolist()
    print(pd.DataFrame(x))
    
    x = cleaning_dataframe(x)
    
    print('Before entering into the cleaning function...............')
    print(x)
    try :

        x = cleaning_data(x)
        x = pd.DataFrame(x)
        x = cleaning_data2(x)

    except:
        x = x.copy()

 
    y = pd.DataFrame(x)
    print(y)
    
    print("Text Extraction Done.................................100%")
    return x

# -------------------------------------------Functon for detecting all tables in multiple pages for a particular range of pages in a PDF---------------------------------------------------
def detect_multiple_pages(pdf_path, start_page, end_page,structure_type):
    l = []
    output_path = []

    images = convert_from_path(pdf_path)

    s = int(start_page)
    e = int(end_page)
    for i, image in enumerate(images[s - 1:e], start=s - 1):
        i = i + 1

        img = pdf_path[:-4] + "-" + str(i) + ".jpg"

        image.save(img, "JPEG")



        imagematrix, imgfname = pdf_page2img(pdf_path, i, save_image=True)
        pdf_page = norm_pdf_page(pdf_path, i)
        try:
            x1, y1, x2, y2 = detect_table_coords(imgfname)
            df1 = text_based_pdf_extraction(x1, y1, x2, y2, imagematrix, pdf_page, pdf_path, i,structure_type)

            df1 = pd.DataFrame(df1)


            l.append(df1)
            
            os.remove(imgfname)


        except TypeError as e:
            # print(e)
            print("There is no output")





    return l, len(l)

# -------------------------------------------------------Function for detecting single table in a single page in a pdf---------------------------------------------------
def detect_single_page(pdf_path, page_no,structure_type):
    pdf_file = pdf_path
    
    pg = int(page_no)
    img, imgfname = pdf_page2img(pdf_file, pg, save_image=True)
    pdf_page = norm_pdf_page(pdf_path, pg)
    try:
        x1, y1, x2, y2 = detect_table_coords(imgfname)

        df1 = text_based_pdf_extraction(x1, y1, x2, y2, img, pdf_page, pdf_file, pg,structure_type)
        df1 = pd.DataFrame(df1)
        os.remove(imgfname)
    except TypeError as e:
        
        df1 = "No Output 2"

    return df1

# -------------------------------------------------------------------Detect all pages in PDF------------------------------------------------------
def detect_all_pages(pdf_path,structure_type):
    images = convert_from_path(pdf_path)
    type(images)
    l = []
    output_path = []

    for i, image in enumerate(images, start=0):

        img = pdf_path[:-4] + "-" + str(i + 1) + ".jpg"
        image.save(img, "JPEG")
        head, tail = os.path.split(img)

     
        imagematrix, imgfname = pdf_page2img(pdf_path, i + 1, save_image=True)
        pdf_page = norm_pdf_page(pdf_path, i + 1)
        try:
            x1, y1, x2, y2 = detect_table_coords(imgfname)

            df1 = text_based_pdf_extraction(x1, y1, x2, y2, imagematrix, pdf_page, pdf_path, i + 1,structure_type)


            df1 = pd.DataFrame(df1)

            l.append(df1)
            
            os.remove(imgfname)




        except TypeError as e:

            # print(e)
            print("There is no output")




        # except ErrorType as e:
        #     # print(e)
        #     print("In Catch")

    return l, len(l)









def cleaning_dataframe(x):
    for outer in range(len(x)):

        for inner in range(len(x[outer])):

            a = x[outer][inner]

            b = re.sub('[^a-zA-ZÀ-ú0-9 \n\.\,\:\%\/\-\#\+\€]', '', a)

            x[outer][inner] = b
    return x

# --------------------------------------------------------Function to merge columns provided by the user-----------------------------------------
def merge_columns(list_of_list, merge_col_no):
    
    merge_col_no = int(merge_col_no)
    for i in range(0, len(list_of_list)):
        list_of_list[i][merge_col_no - 1] = list_of_list[i][merge_col_no - 1] + " " + list_of_list[i][merge_col_no]
        x = list_of_list[i].pop(merge_col_no)           
    return list_of_list



# ---------------------------------------------------------filtering the haeder with extra spaces and escape character so that it can map the values in excel

# ******************************************************************get currency value***********************************************************

# -------------------------------------------------get start and end page of the the pagelist passed from the fronend


# Pass the dataframe and column name and get sum of all values in the column with any fromat

# ---------------------------------------------------Function to get date and time---------------------------------------------------




# Calculating Total Tax amount Total Amount Index and filling curremcy column


# -------------------Converting String list to integer list------------------------------------------------------



#-------------------------------------Combining Dataframe---------------------------------------------------------------



# ------------------------------------------------------------------Function to fit all columns into template provided-------------------------------------------



    
def return_correct_row(list_of_list):
    list_expected = ['Description*','Sr.No*']
    final_list = []
    for i in list_of_list:
        for j in list_expected:
            for k in i:
                if re.match(j,k):
                    pos_of_col = list_of_list.index(i)
                    if pos_of_col > 0:
                        del list_of_list[0:pos_of_col]
                        final_list = list_of_list
                    else:
                        final_list = list_of_list
                else:
                    final_list = list_of_list

    for i in range(len(final_list[0])):
        final_list[0][i] = final_list[0][i].strip().replace('.','').replace('\n','').replace('  ',' ')
    
    return final_list





















    
# # Detect table in the image
# def detect_table(imgfname):
#     try:
#         image_path = imgfname

#         image = read_image_bgr(image_path)
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#         output = image.copy()
#         output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
#         # print(output.shape)  # row (height) x column (width) x color (3)

#         image = preprocess_image(image)
#         (image, scale) = resize_image(image)
#         image = np.expand_dims(image, axis=0)

#         # detect objects in the input image and correct for the image scale
#         (boxes, scores, labels) = model.predict_on_batch(image)
#         boxes /= scale

#         confidence = 0.2

#         import matplotlib.pyplot as plt

#         label_out = []

#         # loop over the detections
#         for (box, score, label) in zip(boxes[0], scores[0], labels[0]):
#             # filter out weak detections
#             if score < confidence:
#                 continue

#             # convert the bounding box coordinates from floats to integers
#             box = box.astype("int")

#             # build the label and draw the label + bounding box on the output
#             # image
#             labeli = label
#             label = "{}: {:.2f}".format(LABELS[label], score)
#             # print(label)

#             if LABELS[labeli] not in label_out:
#                 label_out.append(LABELS[labeli])
#                 cv2.rectangle(output, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 12)

#                 cv2.putText(output, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 4.5, (255, 1, 1), 12)
#     except ErrorType as e:
#         print(e)
#         print("In Catch")

# # Cleans the dataframe of redundant characters
# def cleaning(df1):
#     for outer in range(len(df1)):
#         # you need the length of the list in position 'outer', not of 'outer' itself

#         for inner in range(len(df1[outer])):
#             a = df1[outer][inner]

#             b = re.sub('[^a-zA-Z0-9 \n\.]', '', a)
#             print(b)
#             print('new string')
#             print(b)
#             df1[outer][inner] = b
#             return df1