import socket

target_host = '127.0.0.1'
target_port = 9999

#socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connect to client
client.connect((target_host, target_port))
#send data
client.send("GET / HTTP/1.1\r\nHost: localhost\r\n\r\n".encode())
#receive response
response = client.recv(4096).decode()
print(response)
