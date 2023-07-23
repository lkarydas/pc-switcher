"""TCP server that listens for commands and switches monitor input."""

import socketserver

from absl import app
from absl import logging

from ddc import ddc_control_tcp_handler

HOST = ""  # Standard loopback interface address (localhost).
PORT = 65432  # Port to listen on (non-privileged ports are > 1023).
TCPServer = socketserver.TCPServer

def main(argv):
  """Main function that starts the TCP server for DDC monitor control."""
  del argv  # Unused.
  logging.info('Server is accepting connections on port %s.', PORT)
  with TCPServer((HOST, PORT), ddc_control_tcp_handler.DDCHandler) as server:
    try:
      server.serve_forever()
    except KeyboardInterrupt:
      logging.info('Exiting.')


if __name__ == '__main__':
  app.run(main)
