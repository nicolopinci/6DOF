import serial
import time
import random

print("hey")

arduino = serial.Serial('/dev/cu.usbserial-DN01DCM1', 921600)
time.sleep(2)
print("hey")

#print(arduino.readline())
print("Enter '1' to turn 'on' the LED and '0' to turn LED 'off'")

while 1:

    var = random.randrange(0,10)
    print("You Entered :" + str(var))
    
    arduino.write(str.encode(str(var)))
    
    time.sleep(1)

#    if(var == '1'):
#        arduino.write(b'1')
#        print("LED turned on")
#        time.sleep(1)
#
#    if(var == '0'):
#        arduino.write(b'0')
#        print("LED turned off")
