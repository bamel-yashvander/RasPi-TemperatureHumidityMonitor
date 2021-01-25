#!usr/bin/python3

import Adafruit_DHT as DHT
import RPi.GPIO as GPIO
from threading import Thread

class SENSOR:
    def __init__(self,name, pin, temp_pin, humd_pin):
        self.name = name
        self.pin = pin
        self.temp_pin = temp_pin
        self.humd_pin = humd_pin
        print('sensor@{self.name}')
        while True:
            try:
                self.min_temp = float(input('Enter the min. temperature(C): '))
                self.max_temp = float(input('Enter the max. temperature(C): '))
                self.min_humd = float(input('Enter the min. humidity(%): '))
                self.max_humd = float(input('Enter the max. humidity(%): '))
                if self.min_temp and self.max_temp and self.min_temp and self.max_temp:
                    break

            except ValueError:
                print('Enter a value greater than ZERO.')

    
    def monitor(self):
    
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.temp_pin, GPIO.OUT)
            GPIO.setup(self.humd_pin, GPIO.OUT)
            
            while True:
                self.humd, self.temp = DHT.read_retry(11, self.pin)
                print(f'sensor@{self.name}\nTemperature {self.temp} C, Humidity {self.humd} %\n')

                if self.temp < self.min_temp:
                    GPIO.output(self.temp_pin, True)
                    print(self.pin, 'temp on')
                elif self.temp > self.max_temp:
                    GPIO.output(self.temp_pin, False)
                    print(self.pin, 'temp off')

                if self.humd < self.min_humd:
                    GPIO.output(self.humd_pin, True)
                    print(self.pin, 'humd on')
                elif self.humd > self.max_humd:
                    GPIO.output(self.humd_pin, False)
                    print(self.pin, 'humd off')
            
        finally:
            GPIO.cleanup()
            

sensor_4 = SENSOR('pin 4', 4, 11, 12)
sensor_13 = SENSOR('pin 13', 13, 15, 16)
sensor_16 = SENSOR('pin 16', 16, 21, 22)

while True:
    sensor_4_thread = Thread(target=sensor_4.monitor)
    sensor_13_thread = Thread(target=sensor_13.monitor)
    sensor_16_thread = Thread(target=sensor_16.monitor)
    
    sensor_4_thread.run