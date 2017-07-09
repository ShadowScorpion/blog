import socket
import time

target_host = 'localhost'
target_port = 88
message = "test message"

server_address = (target_host, target_port)
#socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#connect to client
client.bind(server_address)

print("Awaiting messages from hosts")

while True:
    data, addr = client.recvfrom(1024)
    print ("Received message:", data)
