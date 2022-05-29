import serial
from serial.tools import list_ports
import sys


#list serial devices 
list_ports.comports()

device = input("Select your device: ")

#attempts to create a connection and read data
try:
    ser = serial.Serial(device,9600)
except:
    sys.stderr.write("Error: Connection Failed / Device not found \n")
else:
    while True: 
        print(ser.readLine())
