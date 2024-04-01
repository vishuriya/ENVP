from datetime import datetime


def get_date_time():
    dateTimeObj = datetime.now()
    dateObj = dateTimeObj.date()
    timeObj = dateTimeObj.time()

    dateStr = dateObj.strftime("%b %d %Y ")
    timeStr = timeObj.strftime("%H:%M:%S")

    print("Date : ", dateStr)
    print("Time : ",timeStr)
    
    return dateStr, timeStr

