#!/usr/bin/python
 
import spidev
import time
import os
import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(7,GPIO.FALLING,callback=somefunction,bouncetime=300)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000
 
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts
 
def ConvertTemp(data,places): 
  temp = ((data * 330)/float(1023))-50
  temp = round(temp,places)
  return temp
 
light_channel = 0
temp_channel  = 1
 
global delay
global count
global i

def isabove():
  if(i>3):
    i = 0

def somefunction():
  print("Button pressed, changing delay time")
  if(GPIO.input(7) == 1):
    i+=1
    if(i==1):
      delay = 10
    else if(i==2):
      delay = 5
    else:
      delay = 1
  isabove()
  
print("Runtime\t\tTemp Reading\t\tTemp\t\tLight Reading")

while True:
  light_level = ReadChannel(light_channel)
  light_volts = ConvertVolts(light_level,2)
  temp_level = ReadChannel(temp_channel)
  temp_volts = ConvertVolts(temp_level,2)
  temp       = ConvertTemp(temp_level,2)

  print(str(count)+"s"+"\t\t"+str(temp_level)+"t\t\t"+str(temp)+" C\t\t"+str(light_level))
  count = count + delay
  time.sleep(delay)
