import machine
from machine import Pin
import network
import socket
import time

STATIC_IP = "192.168.1.100"
PORT = 6677

FLASH = Pin(4, Pin.OUT)
BUTTON = Pin(2, Pin.IN)

# Network Connection

print("Starting network connection....")

wifiName = "TESTE-PLC"
wifiPassword = "hidropocos22"

station = network.WLAN(network.STA_IF)
station.active(1)
station.connect(wifiName, wifiPassword)

while station.isconnected == 0:
    print(".")
    time.sleep(0.2)

# IP config

station.ifconfig((STATIC_IP, '255.255.255.0', '192.168.100.2', '8.8.8.8'))

print(f"Connected to {wifiName} in {station.ifconfig}.")
FLASH.on()
time.sleep(0.5)
FLASH.off()

# Communication and read I/O

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((STATIC_IP, PORT))
server_socket.listen(1)

print(f"\nServer listening to {station.ifconfig()[0]}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()

    data = client_socket.recv(1024)
    if data: print(f"Mensagem recebida do cliente: {data.decode()}")

    client_socket.send(str(BUTTON.value()).encode())

    client_socket.close() 