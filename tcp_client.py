"""TCP client for sending messages."""

import socket
from absl import logging

HOST = "192.168.1.153"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
TIMEOUT_SEC = 1

def send_message(message):
  """Send a TCP message."""
  try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(TIMEOUT_SEC)
    client_socket.connect((HOST, PORT))
    client_socket.send(message.encode())
  except socket.timeout:
    logging.error('Could not connect to TCP server at %s:%s. Connection timed'
                  'out.', HOST, PORT)
