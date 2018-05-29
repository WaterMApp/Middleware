import serial
import time

 # id of the fountain associated with this data
id="qiej2xxi7j"

url_req="http://srv1.gabrio.ovh:9998/fountain_data/"+id

def send_measurements(ph,turb):
    r = requests.post(
        url_req,
        json={ 'ph':ph, 'turb':turb, 'temp': 23})
    return (r.status_code,r.text)


print '[***] Trying to open serial'
ser=serial.Serial(port='COM5',timeout=3,baudrate=115200*2)
print '[   ] ok.'

print '[***] Start Reading from serial'
c=100
while(1):
    readed = ser.readline().strip("\r\n")
    print '[   ] Readed: '+readed

    readed_split = readed.split(" ")


    if len(readed)<=0 or readed[0]!="ALGG":
        print '[ ! ] Wrong message received'
        continue

    ph = float(readed[1].split(":")[1])
    turb = float(readed[2].split(":")[1])

    print "[***] Sending to "+path+" ph:"+ph+" turb:"+turb 
    status,txt = send_measurements(ph,turb)
    print "[   ] Response("+status+"): "+txt
    
    c=c-1
    if c<0:
        ser.close()
        break


