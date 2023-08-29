'''
>>> The program for the PC connect to ESP32 to measure distance using ToF method <<<

If you can, please support me on my Youtube's channel: @ElectricalThinking29
by hitting like, share and subscribe's buttons to my videos.

How to get this program work:
    1. Open this project on Visual Studio Code
    2. Create the Enviroment file by:
        2.1. Open New Terminal
        2.2. In the Terminal, type: python -m venv .venv
        2.3. Next, type: .venv\Scripts\activate
    3. Install the neccesary library: pip install keyboard   

*** LICENSE ***

Copyright 2023 @ElectricalThinking29

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''
import socket
import time
import keyboard

# Set up the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 12345))  # Bind to a local port
print("UDP server up and listening.")

# Set up the ESP32 address and port 
esp32_addr = '192.168.4.1'
esp32_port = 12345

# Start the calibration
print('Start the calibration !')
print('Place your board (ESP32) close to this PC (less than 29 cm), then press the "space" key to continue.')
keyboard.wait('space')
print("Calibration process")
print("0                   100 %")
    
tof_sum = 0
for i in range(20):
    # Send a message to the ESP32
    message = b'A'
    sock.sendto(message, (esp32_addr, esp32_port))
    send_time = time.perf_counter_ns()

    # Receive the same message back from the ESP32
    data, addr = sock.recvfrom(1024)
    recv_time = time.perf_counter_ns()

    # Calculate the time-of-flight (ToF) of the message
    tof_sum = tof_sum + recv_time - send_time # nanoseconds

    print("#",end='', flush=True)          
    time.sleep(1)
sys_time = tof_sum / 20
print("\nsystem time : %.5f ns"%(sys_time))

print('\nPlace your board (ESP32) at 1 m away from this PC, then press the "space" key to continue.')
keyboard.wait('space')
print("Continue calibrating")
print("0                   100 %")   

tof_sum = 0
for i in range(20):
    # Send a message to the ESP32
    message = b'A'
    sock.sendto(message, (esp32_addr, esp32_port))
    send_time = time.perf_counter_ns()

    # Receive the same message back from the ESP32
    data, addr = sock.recvfrom(1024)
    recv_time = time.perf_counter_ns()

    # Calculate the time-of-flight (ToF) of the message
    tof_sum = tof_sum + (recv_time - send_time - sys_time)/2 # nanoseconds

    print("#",end='', flush=True)          
    time.sleep(1)
tof = tof_sum / 20

# Calculate transmition's speed
c = 1.0 / (tof * (1e-9)) # m/s

print("\nCalibration completed")
print(" Transmition's speed : %.5f m/s"%(c))

while True:
    print('\nPress the "space" key to get the estimated distance.')
    keyboard.wait('space')
    print("Calculating process")
    print("0                   100 %")
    distance_sum = 0.0
    for i in range(200):
        # Send a message to the ESP32
        message = b'A'
        sock.sendto(message, (esp32_addr, esp32_port))
        send_time = time.perf_counter_ns()

        # Receive the same message back from the ESP32
        data, addr = sock.recvfrom(1024)
        recv_time = time.perf_counter_ns()

        # Calculate the time-of-flight (ToF) of the message
        tof = (recv_time - send_time - sys_time)/2 # sys_time = 14274735.00000 ns

        # Calculate the distance
        distance_sum = distance_sum + c * (tof)* 1e-9 # meter   c = 35.20685 m/s
        if (i % 10 == 0):
            print("#",end='', flush=True)          
        time.sleep(1)

    distance = distance_sum / 200 
  
    print(f'\nMessage: {data.decode()}')
    #print('Time-of-flight: %.5f ns'%tof)
    print('Estimated distance: %.5f m\n'%distance)
