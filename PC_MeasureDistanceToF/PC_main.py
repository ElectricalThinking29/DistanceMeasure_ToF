
'''
The program for the PC connect to ESP32 to measure distance using ToF method
You can watch this project's video at: ...
...

How to get this program work:
    1. Open this project on Visual Studio Code
    2. Create the Enviroment file by:
        2.1. Open New Terminal
        2.2. In the Terminal, type: python -m venv .venv
        2.3. Next, type: .venv\Scripts\activate
    3. Install the neccesary library: pip install keyboard   
'''
import keyboard
import socket
import time
import math

ESP32_IP = '192.168.4.1'
ESP32_PORT = 1234

tof_sum = 0

# Create a TCP socket and connect to the ESP32
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ESP32_IP, ESP32_PORT))
print('Connected to ESP32')

# Start the calibration
print('Start the calibration !')
print('Place your board (ESP32) close to this PC (less than 29 cm), then press the "space" key to continue.')
keyboard.wait('space')

print("Calibration process")
print("0                   100 %")

for i in range(10):
    # Send the message and get the ToF
    message = 'Hello, ESP32!'              
    start_time = time.perf_counter_ns() 
    s.sendall(message.encode()) 
    response = s.recv(20).decode()     
    end_time = time.perf_counter_ns()   
    tof_sum = tof_sum + (end_time - start_time) # nanoseconds     
    print("#",end='#', flush=True)          
    time.sleep(2)

print("Tof_sum: %d"%tof_sum)  
sys_time = tof_sum / 10 # nanoseconds  
tof_sum = 0
print('\nCalibration completed !') 
print("System time: %d nanoseconds"%(sys_time))
 
# Measure the ToF and calculate the distance
while True:
    print('Try move your board to a different location and press the "space" key to get the estimated distance.')
    keyboard.wait('space')
    print("Calculating process")
    print("0                   100 %")
    for i in range(10):
        message = 'Hello, ESP32!'
        start_time = time.perf_counter_ns()  
        s.sendall(message.encode())
        response = s.recv(20).decode() 
        end_time = time.perf_counter_ns()        
        tof_sum = tof_sum + end_time - start_time  # nanoseconds 
        print("#",end='#', flush=True)  
        time.sleep(2)
    tof = (tof_sum / 10) - sys_time / 1000
    print("\nToF raw: %.5f"%(end_time-start_time))
    print("ToF: %.5f"%tof)
    distance = 299792458 * (tof - 348277)* 1e-9 # meter                  
    print("Estimated present distance : %.5f meters" %(distance))
    print()        
# + 14645280 + 100704840 