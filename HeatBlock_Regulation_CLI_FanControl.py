#!/usr/bin/env python3

import sys
import argparse
import time
from gpiozero import LED

# This imports the Adafruit DHT software installed via pip
import Adafruit_DHT

# Initialize the DHT22 sensor
SENSOR = Adafruit_DHT.DHT22

# GPIO4 on the Raspberry Pi
SENSOR_PIN = 4

# FAN Initialization
FAN_F_01 = LED(17)
FAN_F_02 = LED(19)

def FRONT_FAN_ON():
    FAN_F_01.on()
    FAN_F_02.on()

def FRONT_FAN_OFF():
    FAN_F_01.off()
    FAN_F_02.off()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fahrenheit", help="output temperature in Fahrenheit", action="store_true")

    return parser.parse_args()

def celsius_to_fahrenheit(degrees_celsius):
        return (degrees_celsius * 9/5) + 32

def main():
    args = parse_args()

    #Trigger Variables
    #TEMP_D = round(TEMP_UI_D,1)
    TEMP_D = round(float(input("Please enter desired temperature [rounded to one decimal place]: ")),1)
    TEMP_D_HIGH = TEMP_D + 0.5
    TEMP_D_LOW = TEMP_D - 0.5
    while True:
        try:
            # Gather the humidity and temperature
            # data from the sensor; GPIO Pin 4
            humidity, temperature = Adafruit_DHT.read_retry(SENSOR, SENSOR_PIN)
            TEMP_F = round(celsius_to_fahrenheit(temperature),1)
            TEMP_C = round(temperature,1)
        except RuntimeError as e:
            # GPIO access may require sudo permissions
            # Other RuntimeError exceptions may occur, but
            # are common.  Just try again.
            print(f"RuntimeError: {e}")
            print("GPIO Access may need sudo permissions.")

            time.sleep(2.0)
            continue

        if args.fahrenheit:
            print("Temp: {0:0.1f}*F, Humidity: {1:0.1f}%".format(celsius_to_fahrenheit(temperature), humidity))

            if TEMP_F > TEMP_D_HIGH:

                FRONT_FAN_ON()
                #FAN ON
                print("Temperature too High")
            elif TEMP_F < TEMP_D_LOW:
                FRONT_FAN_OFF()
                #FAN OFF
                print("Temperature too Low")
            elif TEMP_F >= TEMP_D_LOW and TEMP_F <= TEMP_D_HIGH:
                FRONT_FAN_OFF()
                #FAN OFF
                print("Temperature in Correct Range")
        else:
            print("Temp:{0:0.1f}*C, Humidity: {1:0.1f}%".format(temperature, humidity))

            if TEMP_C > TEMP_D_HIGH:
                FRONT_FAN_ON()
                #FAN ON
                print("Temperature too High")

            elif TEMP_C < TEMP_D_LOW:
                FRONT_FAN_OFF()
                #FAN OFF
                print("Temperature too Low")

            elif TEMP_C >= TEMP_D_LOW and TEMP_C <= TEMP_D_HIGH:
                FRONT_FAN_OFF()
                #FAN OFF
                print("Temperature in Correct Range")
        time.sleep(1.0)

if __name__ == "__main__":
    main()