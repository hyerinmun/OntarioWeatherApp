from datetime import datetime
from os import error
from urllib import request

now = str(datetime.utcnow())

print("Current time: ", now)

month = now[5:7]
print(month)

day = now[8:10]
print(day)

hour = now[11:13]
print(hour)


url = str('https://dd.weather.gc.ca/nowcasting/matrices/SCRIBE.NWCSTG.' + month + '.' + day + '.' + hour + 'Z.n.Z')
print(url)



local_file = url[45:]
print(local_file)

try:
    request.urlretrieve(url, local_file)

except error:
    if int(hour) > 1 and int(hour) <= 23:
        
        print(hour)
        hour = str("0" + str(int(hour) - 1))
        if len(hour) == 3:
            hour = hour[1:]
        url = str('https://dd.weather.gc.ca/nowcasting/matrices/SCRIBE.NWCSTG.' + month + '.' + day + '.' + hour + 'Z.n.Z')
        print(url)
        local_file = url[45:]
        print(local_file)
        request.urlretrieve(url, local_file)
        
            
    elif int(hour) == 0:
            print(hour)
            hour = "23"
            url = str('https://dd.weather.gc.ca/nowcasting/matrices/SCRIBE.NWCSTG.' + month + '.' + day + '.' + hour + 'Z.n.Z')
            print(url)
            local_file = url[45:]
            print(local_file)
            request.urlretrieve(url, local_file)