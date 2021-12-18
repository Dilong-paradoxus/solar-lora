#BLUE code

import board
import busio
import digitalio
import adafruit_rfm9x
import adafruit_tsl2591
import neopixel
import adafruit_dht
import analogio
import time
import math

i2c = board.I2C() #set up i2c
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO) #set up spi

cs = digitalio.DigitalInOut(board.D10) #chip select to pin 10
reset = digitalio.DigitalInOut(board.D11) #RST to pin 11

rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0) #set up connection to RFM95 radio
rfm9x.tx_power = 23
sensor = adafruit_tsl2591.TSL2591(i2c) #set up connection to light sensor
dht = adafruit_dht.DHT11(board.D24) #set up connection to DHT11 temp sensor
pin = analogio.AnalogIn(board.A0)

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1) #set connection to neopixel 
pixel.fill((0, 0, 0))

def calc_bat(vbat_raw): #takes raw pin value and calculates actual voltage
    res_1 = 467000 #resistor 1 value in ohms
    res_2 = 97000 #resistor 2 value in ohms

    vbat_measured = (vbat_raw / 65535) * 3.3 #calculates voltage on analog pin from raw value
    vbat_cal = vbat_measured / (res_2 / (res_1 + res_2)) #calculates input voltage using voltage div eq

    vbat_cal = round(vbat_cal,1)

    return vbat_cal #return calibrated voltage

while True:
    try:
        tmp = dht.temperature #temperature sensor
        hum = dht.humidity #humidity sensor
        light = sensor.visible #light sensor
        vbat = calc_bat(pin.value) #calculate voltage

        sense_string = str(tmp) + ',' + str(hum) + ',' + str(light) + ',' + str(vbat) #concatenate values
        rfm9x.send(sense_string) #transmit data
        print(sense_string) #print what was sent
    except RuntimeError:
        print('Read failure, trying again') #in case temp/hum sensor deosn't give data

    packet = rfm9x.receive(timeout=5.0) #listen for 'ok'
    if packet is not None: #If something was received
        packet_text = str(packet, 'ascii') #change encoding
        rssi = rfm9x.last_rssi #get signal strength
        print(packet_text,'BLUE:',str(rfm9x.last_rssi)) #print received message and rssi
        
        pixel.fill((0,10,0)) #blink green
        time.sleep(0.1)
        pixel.fill((0,0,0)) #turn off neopixel
    else: 
        print('no ok')
        pixel.fill((10,0,0)) #blink red
        time.sleep(0.1)
        pixel.fill((0,0,0)) #turn off neopixel
    time.sleep(14.9)
