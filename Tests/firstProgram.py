from machine import Pin
import time

flash = Pin(4, Pin.OUT)

while True:
    time.sleep(1)
    flash.on()
    print("Flash ON")

    time.sleep(1)
    flash.off()
    print("Flash OFF")