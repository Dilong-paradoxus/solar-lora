# solar-lora
A LoRa implementation for monitoring various sensors on a solar panel setup. 

As of now, the setup monitors battery voltage, light level, temperature, and humidity. The code is 100% python. The BLUE side also outputs both signal strength values over usb serial and indicates connection status via the neopixel RGB LED. Data is communicated via the LoRa protocol at 915mhz.

#Hardware
Solar-lora uses two identical modules composed of an Adafruit Feather RP2040 and the LoRa featherwing with a helical antenna. The RED side is connected to a windows computer via usb. The BLUE side lives on a solderless breadboard with a voltage divider and DHT11 temperature/humidity sensor. A light sensor is connected to the Stemma QT port on the RP2040.

#Goals
* Make the hardware less sketchy to reduce fire risk
* Move RED side to a dedicated monitoring computer (such as raspberry pi)
* Add seismometer sensor if data rate is not too high
* Add support for multiple radios and bidirectional communication
