"""Binary to send messages to server. By default, it sends an echo message."""
import sys

from absl import flags
from absl import app
from absl import logging

import tcp_client

FLAGS = flags.FLAGS

flags.DEFINE_string('message', 'echo', 'Message to send.')

def main(argv):
    """Main function."""
    del argv  # Unused.
    message = FLAGS.message
    print(f'Sending message: {message}')
    tcp_client.send_message(message)


if __name__ == '__main__':
    try:
        app.run(main)
    except KeyboardInterrupt:
        print('')
        logging.info('Bye!')
        sys.exit(0)
