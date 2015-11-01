# -*- coding: utf-8 -*-

# Copyright (c) the Contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from core.handlers import CommandHandler
from core.workers import CommandWorker

class MyCommandHandler(CommandHandler):

    def __init__(self, name, frontend, backend):
        CommandHandler.__init__(self, name, frontend, backend)

    def _on_recv_frontend(self, stream, msg):
        self.log.info('handling request from client {0}'. format(msg))
        self._backend.send_multipart(msg)

    def _on_err_frontend(self, stream, msg, status):
        self.log.info('error on client request {0}'. format(msg))

    def _on_recv_backend(self, stream, msg):
        self.log.info('handling answer from worker {0}'. format(msg))
        self._frontend.send_multipart(msg)

    def _on_err_backend(self, stream, msg):
        self.log.info('error on worker processing {0}'. format(msg))


if __name__ == "__main__":

    frontend = 'tcp://127.0.0.1:5555'
    backend = 'tcp://127.0.0.1:5556'
    handler = MyCommandHandler('MyCommandHandler', frontend, backend)

    try:
        handler.start()
    except KeyboardInterrupt, error:
        pass



