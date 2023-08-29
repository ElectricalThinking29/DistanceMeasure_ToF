/*
>>> The program for the ESP32 creates UDP Server to measure distance using ToF method <<<

If you can, please support me on my Youtube's channel: @ElectricalThinking29
by hitting like, share and subscribe's buttons to my videos.

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
*/

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>

// Set up the Wi-Fi network
const char* ssid = "ESP32-Access-Point";
const char* password = "password";
IPAddress local_IP(192, 168, 4, 1);
IPAddress gateway(192, 168, 4, 1);
IPAddress subnet(255, 255, 255, 0);

// Set up the UDP server
WiFiUDP udp;
const int udp_port = 12345;

void setup() {
  Serial.begin(115200);
  setCpuFrequencyMhz(160);
  
  // Set up the Wi-Fi access point
  WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid, password);
  delay(100);

  // Configure the access point IP address
  if (!WiFi.softAPConfig(local_IP, gateway, subnet)) {
    Serial.println("Failed to configure access point");
  }

  // Start the UDP server
  if (!udp.begin(udp_port)) {
    Serial.println("Failed to start UDP server");
  }
  else {
    Serial.println("UDP server is up");
  }
  
}

void loop() {
  // Wait for a message from the PC
  int packet_size = udp.parsePacket();
  if (packet_size) {
    // Read the message into a buffer
    char buffer[packet_size];
    udp.read(buffer, packet_size);

    // Check if the message is "A"
    if (strcmp(buffer, "A") == 0) {
      // Send the same message back to the PC
      udp.beginPacket(udp.remoteIP(), udp.remotePort());
      udp.write(reinterpret_cast<uint8_t*>(buffer), packet_size);
      udp.endPacket();
    }
  }
}