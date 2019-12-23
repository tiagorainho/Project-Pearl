from datetime import datetime

dateTimeObj = datetime.now()

def getTimeToString():
    return str(dateTimeObj.hour) + 'hours ' + str(dateTimeObj.minute) + ' minutes and ' + str(dateTimeObj.second) + " seconds"
    
def getTime():
    return str(dateTimeObj.hour) + ':' + str(dateTimeObj.minute) + ':' + str(dateTimeObj.second)

def getDate():
    dateObj = dateTimeObj.date()
    return dateObj.strftime("%b %d %Y")