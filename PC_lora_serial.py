#Reads data from RED rp2040 lora module and saves it to a file

import os
import serial
from time import sleep
from datetime import datetime

#open serial port
def serialopen():
    if os.name == 'nt': #windows
        portname = 'COM5' # change this to the COM port of your microcontroller
    else: #linux or whatever
        portname = '/dev/ttyACM0' #or change this, if you use linux
        
    print('opening serial port at ' +  portname)
    portopen = [False,0] #initialize variable to hold number of failed tries
    while portopen[0] == False:
        portopen[1] = portopen[1] + 1
        print('try #' + str(portopen[1])) #print number of tries 
        try:    
            seropen = serial.Serial(portname,baudrate=115200,timeout=1) #open serial
            portopen[0] = True #probably unnecessary
            filename = set_filename()
            print('serial success')
            return seropen, filename #return the serial port to be used
        except (PermissionError): #not sure if this actually works
            print('PermissionError')
            sleep(2)
        except (OSError, serial.SerialException): 
            print('OSError or SerialException')
            sleep(2) #wait for the serial device to turn on or be plugged in

#set up filename to save data to
def set_filename():
    print(datetime.utcnow())
    file_path = r'C:\\LoRa\\LoRaData\\' #enter a good place to put the data here
    #os.chdir(file_path) #change directory to working directory
    timestring = datetime.utcnow().strftime('%Y%m%d_%H%M')
    filename = file_path + timestring + '_UTC_LoRa_therm.csv'
    print(filename)
    return filename

def read_serial(ser): #grabs latest line from serial port
    try:
        ser_bytes = ser.readline() #read one line from serial port
        decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")) #convert that line to a normal string
        return 1,decoded_bytes,0 #return bit saying data is good, the data, and a zero
    except (OSError, serial.SerialException,UnicodeDecodeError):
        ser.close() #end serial connection
        print('serial error, retrying')
        sleep(0.5)
        ser,filename = serialopen()
        return 0,ser,filename

def write_file(line,filename): #takes line to write and path of file
        with open(filename,"a") as f: #write serial to file
            #writer = csv.writer(f,delimiter=",") #set delimiter as ','
            #writer.writerow(line) #write row
            f.write(str(line) + "\r\n")
            return

starttime = datetime.utcnow() #set starttime to current time
ser, filename = serialopen() #open serial port
ser.reset_input_buffer() #clear buffer of any previous data

ignore_lines = [
    '',
    'NaN,NaN,NaN,NaN',
    'NaN,NaN,NaN,NaN,NaN',
] #ignores blank lines

while True:
    ser_bit, ser_data, fname = read_serial(ser) 
    if ser_bit == 1:
        if ser_data not in ignore_lines:
            #ser_data = ser_data.split(",")
            write_file(ser_data,filename)
            print(ser_data,datetime.now())
    if ser_bit == 0: #if read_serial returns error
        ser = ser_data #set ser to whatever read_serial returned
        filename = fname #set the filename to whatever read_serial returned
