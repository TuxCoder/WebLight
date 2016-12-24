# Run server.

from __future__ import print_function

from weblight.app import create_app

application = create_app('production')
if __name__ == '__main__':
    application.run()
