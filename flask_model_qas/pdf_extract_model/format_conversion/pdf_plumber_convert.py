import ocrmypdf
import os
import img2pdf

try:
    from PIL import Image
except ImportError:
    print("Import error")
    import Image




# Checking the input is it png jpeg or jpeg or is it a pdf, if it is a pdf then it should identify if it is texy based or scan based
def check_input(path):
    

    if path.lower().endswith(('.png','.jpg','.jpeg')):
        file_type  = '2'
    elif path.lower().endswith(('.pdf')):
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
            # print(text)
            if text == None:
                file_type = '0'  # scanned
            else:
                file_type = '1'  # text-based
    else:
        print("Improper file type")
    return file_type



# Once we identify what kind of file it is we will return the actual path
# The main aim is to convert everythung into textbased and then we will send for extracttion
def get_actual_path(input_path):

  

    actual_path = ''
    if check_input(input_path) == '0':
        # print("Scanned")
        head, tail = os.path.split(input_path)
        # print(head,tail)
        x = tail
        output_path = input_path

        ocrmypdf.ocr(input_path, output_path,progress_bar=False)
        print(f" The output path is  {output_path} ")
        actual_path = output_path
        status = 1

    if check_input(input_path) == '1':
        actual_path = input_path



    if check_input(input_path) == '2':
        head, tail = os.path.split(input_path)
        tail = tail.strip('.jpg')  + '.pdf'
        output_path = actual_path + tail

        pdf_path = tail
        image = Image.open(input_path)
        pdf_bytes = img2pdf.convert(image.filename)
        file = open(pdf_path, "wb")
        file.write(pdf_bytes)
        image.close()
        file.close()
        output_path = input_path
        ocrmypdf.ocr(pdf_path, output_path)
        actual_path = output_path



    return actual_path



#
# if __name__ == '__main__':
#     input_path = 'C:\\Users\\UC321QW\\OneDrive - EY\\PycharmProjects\\trial3\\local\\keras-retinanet\\pdfs\\image60771.pdf'
#     print(get_actual_path(input_path))
