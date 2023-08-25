# Runned by my PC

import socket

# Define o endereço e porta do servidor
dhcp_hostname = 'esp32-cam' + '.local'
server_ip = socket.gethostbyname(dhcp_hostname) 
port = 6677
server_address = (server_ip, port)

# Cria um socket TCP para o cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta o cliente ao servidor
client_socket.connect(server_address)

# Mensagem que será enviada para o servidor
mensagem = "Olá, servidor!"

# Envia a mensagem para o servidor
client_socket.send(mensagem.encode())

# Recebe a resposta do servidor
resposta = client_socket.recv(1024)

print(f"Resposta do servidor: {resposta.decode()}")

# Fecha a conexão com o servidor
client_socket.close()