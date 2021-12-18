#RED code

import board
import busio
import digitalio
import adafruit_rfm9x
import time
import supervisor

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO) #set up spi

cs = digitalio.DigitalInOut(board.D10) #chip select to pin 10
reset = digitalio.DigitalInOut(board.D11) #RST to pin 11

rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0) #set up connection to RFM95 radio
rfm9x.tx_power = 23

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

while True:
    #print('Listening:')
    packet = rfm9x.receive(timeout=5.0)
    if packet is not None:
        try:
            packet_text = str(packet, 'ascii')
            rssi = ',' + str(rfm9x.last_rssi) 
            print(packet_text,rssi)
            rfm9x.send('ok RED:' + str(rfm9x.last_rssi) )
        except:
            print('NaN,NaN,NaN,NaN,NaN')
    else: 
        print('NaN,NaN,NaN,NaN,NaN')

supervisor.reload() #resets board if it randomly stops running (not sure why this is needed)
