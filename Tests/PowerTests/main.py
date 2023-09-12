import machine
import time
""" Frequency test

# Test 1 (biggest, 240MHz) - 43mA

machine.freq(240000000)

FLASH = machine.Pin(4, machine.Pin.OUT)

time.sleep(5)
FLASH.on()
time.sleep(1)
FLASH.off()

# Test 2 (160MHz)

machine.freq(160000000)
time.sleep(5)
FLASH.on()
time.sleep(1)
FLASH.off()

# Test 3 (80MHz) -> 23mA

machine.freq(80000000)
time.sleep(5)
FLASH.on()
time.sleep(1)
FLASH.off()

# Test 4 (2MHz) - Doesn't work

machine.freq(2000000)
time.sleep(5)
FLASH.on()
time.sleep(1)
FLASH.off()
"""

# Sleep test
import esp32
from machine import Pin
from machine import deepsleep
from time import sleep

wake1 = Pin(2, mode = Pin.IN)

#level parameter can be: esp32.WAKEUP_ANY_HIGH or esp32.WAKEUP_ALL_LOW
esp32.wake_on_ext0(pin = wake1, level = esp32.WAKEUP_ANY_HIGH)
FLASH = Pin(4, Pin.OUT)

#your main code goes here to perform a task

FLASH.on()
print('Im awake. Going to sleep in 10 seconds')
sleep(2)
FLASH.off() 
print('Going to sleep now')
deepsleep(3000) # It resets after, and restarts the main.py