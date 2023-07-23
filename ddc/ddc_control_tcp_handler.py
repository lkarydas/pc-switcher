"""Request handler for DDC monitor control."""

import socketserver

from absl import logging
from ddc import samsung_ddc

class DDCHandler(socketserver.BaseRequestHandler):
  """
  The request handler class for DDC monitor control.

  It is instantiated once per connection to the server, and must
  override the handle() method to implement communication to the
  client.
  """
  def handle(self):
    # self.request is the TCP socket connected to the client
    self.data = self.request.recv(8).strip()
    message = self.data.decode('utf8')
    if message == '':
      logging.debug('Heartbeat from Uptime Kuma.')
      return
    logging.info('%s wrote: %s', self.client_address[0], message)
    samsung_ddc.switch_monitor_input(message)
