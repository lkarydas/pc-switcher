"""TCP client for sending messages."""

import socket

HOST = "192.168.1.153"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def send_message(message):
  """Send a TCP message."""
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect((HOST, PORT))
  client_socket.send(message.encode())
