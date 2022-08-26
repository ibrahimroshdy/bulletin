import datetime

from uptime import uptime

while True:
    print(str(datetime.timedelta(seconds=uptime())))
