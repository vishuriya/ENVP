import os
from pdf2image import convert_from_path
path = 'C:\\Users\\UC321QW\\OneDrive - EY\Desktop\\training imges\\'
for filename in os.listdir(path):
    
    images = convert_from_path(path + filename)
    for i in range(len(images)):
   
      # Save pages as images in the pdf
        images[i].save(filename + '_' + 'page_'+ str(i) +'.jpg', 'JPEG')
        print(f'{filename}..................100%')
