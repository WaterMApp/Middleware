import serial
import time
import signal
import os
import requests

if os.name =="nt":
    port = "COM4"
else:
    port = "/dev/ttyACM0"
    
id="0gc2v3w039"
path="http://srv1.gabrio.ovh:9998/fountain_data/"+id

        
def send_measurements(ph,turb):
    r = requests.post(
        path,
        json={ 'ph':ph, 'turb':turb, 'temp': 23})
    return (r.status_code,r.text)


print '[***] Trying to open serial'
ser=serial.Serial(port=port,timeout=3,baudrate=115200*2)
print '[   ] ok.'

print '[***] Start Reading from serial'

def main():
    
    readed = ser.readline().strip("\r\n")
    print '[   ] Readed: '+readed

    readed_split = readed.split(" ")

    readed=readed_split
    
    if len(readed)<=0 or readed[0]!="ALGG":
        print '[ ! ] Wrong message received'
        print ""
        return

    ph = float(readed[1].split(":")[1])
    turb = float(readed[2].split(":")[1])


    print "[***] Measured ph:"+ str(ph)+ ", turb:"+str(turb)

    
    print "[***] Sending to "+path
    status,txt = send_measurements(ph,turb)
    print "[   ] Response("+str(status)+"): "+txt

    print ""



while(1):
    try:
        main()
    except KeyboardInterrupt:
        print "[ ! ] CTRL-C handled, exit gracefully."
        ser.close()
        break;
