import win32com.client #pip install pypiwin32 to work with windows operating sysytm
import datetime
import os
import pythoncom
import hashlib

dateToday=datetime.datetime.today()
FormatedDate=('{:02d}'.format(dateToday.day)+'-'+'{:02d}'.format(dateToday.month)+'-'+'{:04d}'.format(dateToday.year))

def save_pdf_attachments(subject,path):
    pythoncom.CoInitialize()
    # Creating an object for the outlook application.
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    print("Connected to Outlook............................................................100%")
    # Creating an object to access Inbox of the outlook.
    inbox=outlook.GetDefaultFolder(6)
    print("Checking Inbox ................................................................100%")
    # Creating an object to access items inside the inbox of outlook.
    messages=inbox.Items

    # path = "C:\\Users\\ZA165BL\\OneDrive - EY\\Desktop\\yolo1\\flask_model\\uploads\\"
    
    s1 = ".pdf"
    list_of_date = []
    list_of_time = []
    list_of_count_attachment = []
    list_of_attachments = []
    # To iterate through inbox emails using inbox.Items object.
    print("Searching For Invoices........................................................100%")
    for idx,message in enumerate(messages):

        if (message.Subject == subject):

            date = message.SentOn.strftime("%b %d %Y")
            time = message.SentOn.strftime("%H:%M:%S")


  


            
            # body_content = message.body
            # Creating an object for the message.Attachments.
            attachments = message.Attachments
            # len_of_attachments = len(attachments)
            # list_of_count_attachment.append(len_of_attachments)
            # print(attachment)
            # To check which item is selected among the attacments.
            # print (message.Attachments.Item(which_item))
            # To iterate through email items using message.Attachments object.
            # for attachment in message.Attachments:
            #     # To save the perticular attachment at the desired location in your hard disk.
            #     attachment.SaveAsFile(path + '\\' + file_name)
            #     break
            num_attach = len([x for x in attachments])
            for x in range(1, num_attach+1):
                attachment = attachments.Item(x)

                

                if(attachment.FileName.count(s1)>0):
                    file_name = attachment.FileName.strip('.pdf') + "-" + str(idx) + "-" + str(x) + '.pdf'
                    attachment.SaveASFile(os.path.join(path,file_name))

                    list_of_date.append(date)
                    list_of_time.append(time)
                    list_of_attachments.append(file_name)
                    

                    
    print("Email Extraction Completed...........................................................100%")
    # print(list_of_attachments,list_of_date,list_of_time)

    return list_of_attachments,list_of_date,list_of_time

