import network
import socket
import machine
from machine import Pin
import time

flash = Pin(4, Pin.OUT)

wifiName = 'TESTE-PLC'
wifiPassword = 'hidropocos22'

print("Connecting to ethernet...")
flash.on()

time.sleep(2)

station = network.WLAN(network.STA_IF)
station.active(1)

while station.isconnected() == False: 
    print(".", end="")
    #station.connect(wifiName, wifiPassword)
    time.sleep(0.5)

print(f"Connected to {wifiName}. In IP {station.ifconfig()}.")
flash.off()

# Cria um socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket.sethostname(hostname)

# Define o endereço e porta do servidor
ip = '192.168.1.205'
station.ifconfig((ip,'255.255.255.0','192.168.100.2','8.8.8.8'))
port = 6677
server_address = (ip, port)


# Faz o bind do socket ao endereço e porta do servidor
server_socket.bind(server_address)

# Define o número máximo de conexões em fila
server_socket.listen(5)

print(f"Servidor escutando em {station.ifconfig()}:{port} e ip - {ip}")

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
