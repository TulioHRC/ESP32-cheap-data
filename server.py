# Code for the server ESP32, the one who will get the info from the client

import machine
import network
import time


class ESP32:
	def __init__(self):
		self.FLASH = machine.Pin(4, machine.Pin.OUT)

		self.wifiName = ""
		self.wifiPassword = ""

		self.STATIC_IP = "192.168.1.100"
		self.PORT = 6677

		self.wifiConnection(self.wifiName, self.wifiPassword)

	# def restart, Server (use class already created, modes)

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


if __name__ == "__main__":
    print("\n\nStarting ESP32 server device...\n\n")
    main = ESP32()