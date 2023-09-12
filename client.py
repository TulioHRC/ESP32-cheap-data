# Code for the server ESP32, the one who will get the info from the client

import machine
import network
import esp32
import time
import socket
import ssl
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


CERT_FILE = "certClient.crt"
KEY_FILE = "privateClient.key"
SERVER_CERT_FILE = "certServer.crt"


class Client:
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def sendData(self, data, serverAddress):
        self.sslClientSocket = self.secureConnection(serverAddress)
        
        if self.sslClientSocket: self.requestHandler(data)
        else: self.clientSocket.close()

    def secureConnection(self, serverAddress):
        try:
            sslSocket = ssl.wrap_socket(self.clientSocket, certfile=CERT_FILE, keyfile=KEY_FILE, ca_certs=SERVER_CERT_FILE, cert_reqs=ssl.CERT_REQUIRED)
            
            sslSocket.connect(serverAddress)
            print("\nConnection estabilished...\n")

            return sslSocket

        except Exception as e:
            print(f"\nConnection / Authentication ERROR: {e}\n")

    def requestHandler(self, data):
        self.sslClientSocket.sendall(data.encode())

        serverResponse = self.sslClientSocket.recv(1024)
        print(f"\nServer answer \"{serverResponse.decode()}\"\n")



class ESP32:
	def __init__(self):
		self.FLASH = machine.Pin(4, machine.Pin.OUT)
        self.INPUT = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP) # Connection of GND, resistor, and the floater in series, NF
        
        self.wifiName = ""
		self.wifiPassword = ""

		self.STATIC_IP = "192.168.1.100"
		self.PORT = 6677

		try:
			self.wifiConnection(self.wifiName, self.wifiPassword)
			self.espClient = Client((self.STATIC_IP, self.PORT))
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
		data = self.INPUT.value()
		if data == '1': data = 0
		else: data = 1
  
		self.espClient.sendData(data)
		esp32.wake_on_ext0(pin = self.INPUT, level = esp32.WAKEUP_ALL_LOW)
  
		machine.deepsleep(5000)
		


if __name__ == "__main__":
    print("\n\nStarting ESP32 server device...\n\n")
    main = ESP32()
