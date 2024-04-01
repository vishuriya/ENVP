from copy import copy
import PyPDF2
import numpy as np
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader
import os
import copy

# Gets pdf_page object from PDF file according to page number
def norm_pdf_page(pdf_file, pg):
    pdf_doc = PyPDF2.PdfFileReader(open(pdf_file, "rb"),strict=False)
    pdf_page = pdf_doc.getPage(pg - 1)
    pdf_page.cropBox.upperLeft = (0, list(pdf_page.mediaBox)[-1])
    pdf_page.cropBox.lowerRight = (list(pdf_page.mediaBox)[-2], 0)
    return pdf_page



# Gets pdf_page object from PDF file according to page number
def norm_pdf_page(pdf_file, pg):
    pdf_doc = PyPDF2.PdfFileReader(open(pdf_file, "rb"),strict=False)
    pdf_page = pdf_doc.getPage(pg - 1)
    pdf_page.cropBox.upperLeft = (0, list(pdf_page.mediaBox)[-1])
    pdf_page.cropBox.lowerRight = (list(pdf_page.mediaBox)[-2], 0)
    return pdf_page


# Converst PDF page to image
def pdf_page2img(pdf_file, pg, save_image=True):
    img_page = convert_from_path(pdf_file, first_page=pg, last_page=pg)[0]
    if save_image:
        img = pdf_file[:-4] + "-" + str(pg) + ".jpg"
        img_page.save(img)
    return np.array(img_page), img



# Gets image dimension
def img_dim(img, bbox):
    H_img, W_img, _ = img.shape
    x1_img, y1_img, x2_img, y2_img = bbox
    w_table, h_table = x2_img - x1_img, y2_img - y1_img
    return [[x1_img, y1_img, x2_img, y2_img], [w_table, h_table], [H_img, W_img]]

# Draws a Bounding box around the table detected
def norm_bbox(img, bbox, x_corr=0.05, y_corr=0.05):
    [[x1_img, y1_img, x2_img, y2_img], [w_table, h_table], [H_img, W_img]] = img_dim(img, bbox)
    x1_img_norm, y1_img_norm, x2_img_norm, y2_img_norm = x1_img / W_img, y1_img / H_img, x2_img / W_img, y2_img / H_img
    w_img_norm, h_img_norm = w_table / W_img, h_table / H_img
    w_corr = w_img_norm * x_corr
    h_corr = h_img_norm * x_corr

    return [x1_img_norm - w_corr, y1_img_norm - h_corr / 2, x2_img_norm + w_corr, y2_img_norm + 2 * h_corr]



# Gets BBox cordinates from PDF
def bboxes_pdf(img, pdf_page, bbox, save_cropped=False, pdf_file=None, pg=None):
    W_pdf = float(pdf_page.cropBox.getLowerRight()[0])
    H_pdf = float(pdf_page.cropBox.getUpperLeft()[1])
    # print(bbox)

    [x1_img_norm, y1_img_norm, x2_img_norm, y2_img_norm] = norm_bbox(img, bbox)
    x1, y1 = x1_img_norm * W_pdf, (1 - y1_img_norm) * H_pdf
    x2, y2 = x2_img_norm * W_pdf, (1 - y2_img_norm) * H_pdf

    if save_cropped:
        page = copy.copy(pdf_page)
        page.cropBox.upperLeft = (x1, y1)
        page.cropBox.lowerRight = (x2, y2)
        output = PyPDF2.PdfFileWriter()
        output.addPage(page)

        with open(pdf_file[:-4] + "-" + str(pg) + ".pdf", "wb") as out_f:
            output.write(out_f)

    return [x1, y1, x2, y2]


    # -------------------------------------------------------Function of getting number of pages--------------------------------------------
def get_PDF_Pages(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file,strict=False)
        return pdf_reader.numPages

def get_file_ext(pdf_path):
    file_prop = os.path.splitext(pdf_path)
    print(f'The value of file Prop is {file_prop}')
    extension = file_prop[1][1:].upper()
    print(f'The value of file extension is {extension}')
    return extension

