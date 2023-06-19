"""TCP server that listens for commands and switches monitor input."""

import socketserver

from absl import app
from absl import logging

import samsung_ddc


HOST = ""  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

class MyTCPHandler(socketserver.BaseRequestHandler):
  """
  The request handler class for our server.

  It is instantiated once per connection to the server, and must
  override the handle() method to implement communication to the
  client.
  """
  def handle(self):
    # self.request is the TCP socket connected to the client
    self.data = self.request.recv(8).strip()
    message = self.data.decode('utf8')
    logging.info('%s wrote: %s', self.client_address[0], message)
    samsung_ddc.switch_monitor_input(message)

def main(argv):
  """Main function that starts the TCP server."""
  del argv  # Unused.
  # Create the server, binding to localhost on port 9999
  logging.info('Server is accepting connections on port %s.', PORT)
  with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C.
    try:
      server.serve_forever()
    except KeyboardInterrupt:
      logging.info('Exiting.')


if __name__ == '__main__':
  app.run(main)