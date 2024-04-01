import os

count = 165
for i in os.listdir('C:\\Users\\UC321QW\OneDrive - EY\\flask_model\\training'):
    print(i)
    os.rename(i,str(count)+ '.'+ i.split('.')[-1])
    count+=1