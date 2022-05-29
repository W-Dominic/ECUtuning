import obd 
from obd import OBDStatus
import serial
import sys
import os

action = int(input( ''' Which feature would you like to use:

                    1) Serial Sensor Connection 
                    2) Obd-II connection 
                    3) Serial Sensor log & Obd-II connection
                    '''))


if action == 1:
    #scans device and attempts to connect to serial sensor 
    isConnected = False
    connectedPort = ""
    for i in range(9):
        try:
            print(f"Attempting to connect to : /dev/ttyUSB{i}")
            ser = serial.Serial(f"/dev/ttyUSB{i}")
        except:
            pass
        else:
            isConnected = True
            connectedPort = f"/dev/ttyUSB{i}"
            break

    #checks for successful connection
    if (isConnected):
        print(f"Connected Successfully to {connectedPort}") 
        
        #reads and log data to a text file
        willLog = input("Would you like to log data to a file? (yes/no): ")
        if willLog == "yes":            
            #clears the file, then opens it
            os.system("cat /dev/null > log.txt")
            file = open("log.txt", "w")
            while True:
                try:
                    data = ser.readline()
                    dataParsed = data.decode("utf-8").replace("\r\n", "")
                    file.write(dataParsed)
                    file.write("\n")
                    print(dataParsed)
                except KeyboardInterrupt:
                    file.close()
                    break
        else:
            while True:
                data = ser.readline()
                dataParsed = data.decode("utf-8").replace("\r\n", "")
                print(dataParsed)

    else:
        sys.stderr.write("Connection failed : device not found\n")


elif action == 2:
    #connects to a bluetooth OBD-II adapter
    sys.stderr.write("Error: Action not currently supported\n")
    '''
    connection = obd.OBD("/dev/rfcomm0")
    if connection.status() == "Not Connected":
        pass
    else:
        while True:
            print(connection.query(obd.commands["RPM"]))
    '''
elif action == 3:
    sys.stderr.write("Error: Action not currently supported\n")
else: 
    sys.stderr.write("Useage : Select actions 1,2, or 3\n")


