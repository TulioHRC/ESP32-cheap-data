# Code for the server ESP32, the one who will get the info from the client

import machine
import network
import time
import socket
import ssl


CERT_FILE = "certServer.crt"
KEY_FILE = "privateServer.key"
CLIENT_CERT_FILE = "certClient.crt"


class Server:
    def __init__(self, serverAddress):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(serverAddress)
        self.serverSocket.listen(5)
        print(f"Server on {serverAddress[0]}:{serverAddress[1]}")

    def communication(self):
        clientSocket, clientAddress = self.serverSocket.accept()
        print("\nConnection estabilished...\n")

        #self.sslAuthenticatedSocket = self.authentication(clientSocket)

        return self.requestHandler(clientSocket) # For initial tests

        if self.sslAuthenticatedSocket: return self.requestHandler()
        else: clientSocket.close()
        
        return "NULL"
        
    def authentication(self, clientSocket):
        try:
            sslContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            sslContext.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
            sslContext.load_verify_locations(cafile=CLIENT_CERT_FILE)
            sslContext.verify_mode = ssl.CERT_REQUIRED

            sslSocket = sslContext.wrap_socket(clientSocket, server_side=True)


            clientCerts = sslSocket.getpeercert()
            if clientCerts:
                print(f"Authentication Passed.\n{clientCerts['subject']}\n")
                return sslSocket

            print("Authentication Failed!!!")

        except Exception as e:
            print(f"Authentication ERROR: {e}\n")

    def requestHandler(self, clientSocket=""):
        if clientSocket: data = self.clientSocket.recv(1024)
        else: self.sslAuthenticatedSocket.recv(1024)

        if data: 
            if clientSocket: clientSocket.sendall(f"Message received...".encode())
            else: self.sslAuthenticatedSocket.sendall(f"Message received...".encode())
            
            return data.decode()
        
        return "NULL"


class ESP32:
    def __init__(self):
        self.FLASH = machine.Pin(4, machine.Pin.OUT)

        self.wifiName = ""
        self.wifiPassword = ""

        self.STATIC_IP = "192.168.1.100"
        self.PORT = 6677

        try:
            self.wifiConnection(self.wifiName, self.wifiPassword)
            self.espServer = Server((self.STATIC_IP, self.PORT))
            self.mainLoop()
        except Exception as e:
            print(f"\n\nError {e}\n\n")
            machine.reset()


    def wifiConnection(self, name, password):
        print("Starting WiFi connection...\n")

        self.FLASH.on()

        self.station = network.WLAN(network.STA_IF)
        self.station.active(1)
        self.station.connect(name, password)

        while self.station.isconnected() == 0:
            print(".")
            time.sleep(0.2)

        self.station.ifconfig((self.STATIC_IP, '255.255.255.0', '192.168.100.2', '8.8.8.8'))

        print(f"Connected to {name}, in IP {self.STATIC_IP}.")

        time.sleep(0.5)
        self.FLASH.off()
    
    def mainLoop(self):
        while True:
            response = self.espServer.communication()
            if response != "NULL":
                # Test only with flash
                if response == "1" or response == 1: self.FLASH.on()
                else: self.FLASH.off()
        


if __name__ == "__main__":
    print("\n\nStarting ESP32 server device...\n\n")
    main = ESP32()