import win32api
import requests
import datetime
import json
import time

timeHasBeenSet = False

def get_internet_data():
    ip = requests.get("http://ipecho.net/plain").text
    timeapi = f"https://timeapi.io/api/Time/current/ip?ipAddress={ip}"
    data = requests.get(timeapi).json()
    year = data['year']
    month = data['month']
    day = data['day']
    hour = data['hour']
    minute = data['minute'] - 1
    second = data['seconds']
    milliSeconds = data['milliSeconds']
    time = (year,month,day,hour,minute,second,milliSeconds)
    return time

def has_internet():
    try:
        requests.get("https://www.google.com",timeout=5)
        print("Connection is active")
        return True
    except (requests.ConnectionError,requests.Timeout) as e:
        print("No internet Connection")
        return False

def setTime(time):
    global timeHasBeenSet
    t = datetime.datetime(*time)
    dayOfWeek = t.isocalendar()[2]
    tt = time[:2] + (dayOfWeek,)+time[2:]
    win32api.SetSystemTime(*tt)
    print("set time successful")
    timeHasBeenSet = True


while not timeHasBeenSet:
    if has_internet():
        setTime(get_internet_data())
    else:
        time.sleep(3)

