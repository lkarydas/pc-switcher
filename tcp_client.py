import socket

HOST = "192.168.1.153"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def send_message(message):
  clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  clientSocket.connect((HOST, PORT))
  clientSocket.send(message.encode())
