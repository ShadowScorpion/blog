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
client.settimeout(1)

while True:
    sent = client.sendto(message.encode(), server_address)
    time.sleep(1)
