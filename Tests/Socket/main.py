import network
from machine import Pin
import time

flash = Pin(4, Pin.OUT)

wifiName = 'teste'
wifiPassword = 'ipoq6796'

print("Connecting to ethernet...")
flash.on()

time.sleep(2)

station = network.WLAN(network.STA_IF)
station.active(True)

while station.isconnected() == False: 
    print(".", end="")
    time.sleep(1)
    host = f'esp32-cam-{machine.unique_id()}'
    station.config(dhcp_hostname = host)
    station.connect(wifiName, wifiPassword)

print(f"Connected to {wifiName}.")
flash.off()

#if station.isconnected(): print(f"Connected to {wifiName}.")
#else: print("Error to connect ethernet.")

import socket

# Cria um socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
hostname = station.config('dhcp_hostname')
ip = station.ifconfig()[0]
port = 6677
server_address = (ip, port)


# Faz o bind do socket ao endereço e porta do servidor
server_socket.bind(server_address)

# Define o número máximo de conexões em fila
server_socket.listen(5)

print(f"Servidor escutando em {hostname}:{port} e ip - {ip}")

while True:
    # Espera por uma conexão
    client_socket, client_address = server_socket.accept()

    # Recebe os dados enviados pelo cliente
    data = client_socket.recv(1024)

    # Processa os dados recebidos
    if data:
        print(f"Mensagem recebida do cliente: {data.decode()}")

    # Fecha a conexão com o cliente
    client_socket.close()
