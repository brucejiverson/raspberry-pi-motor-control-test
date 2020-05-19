import time
from datetime import datetime, timedelta
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import piplates.MOTORplate as MOTOR          #import the MOTORplate module
import numpy as np
import pickle as pkl

addr = 0                                    #Address of the motor plate board on SPI bus
motor_n = 2
accel_time = 0.5
#configure dc motor 2 on the MOTORplate at address 0 being configured for clockwise
MOTOR.dcCONFIG(addr, motor_n, 'ccw', 50.0, accel_time) #motion at a 50% duty cycle and accel_time seconds of acceleration

def move(secs):
    global t
    global sensor_vals
    #implicit global start
    while t > timedelta(seconds = secs):
        t = datetime.now() - start              #time since start of the experiment

        pot = AnalogIn(mcp, MCP.P0)
        print('Raw ADC Value: ', pot.value)
        print('ADC Voltage: ' + str(pot.voltage) + 'V')
        sensor_vals[t] = pot.value

# create an analog input channel on pin 0
sensor_vals = {}
start = datetime.now()
MOTOR.dcSTART(addr, motor_n)                 #Start DC motor
t = timedelta(seconds = 0)              #time since start of the experiment

# MOTOR.dcSPEED(0,2,100.0)
move(10)
MOTOR.dcCONFIG(addr, motor_n, 'cw', 50.0, accel_time) #motion at a 50% duty cycle and accel_time seconds of acceleration
move(10)



MOTOR.dcSTOP(addr, motor_n)                  #stop the motor
time.sleep(accel_time)                              #wait for deceleration
print("DC Motor demo completed")              #print notice
with open('sensor_vals.pkl', 'wb') as f:
    pkl.dump(sensor_vals, f)


# 192.168.86.40



def remap_range(value, left_min, left_max, right_min, right_max):
    # this remaps a value from original (left) range to new (right) range
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (int)
    valueScaled = int(value - left_min) / int(left_span)

    # Convert the 0-1 range into a value in the right range.
    return int(right_min + (valueScaled * right_span))
