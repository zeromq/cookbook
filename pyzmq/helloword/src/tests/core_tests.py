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
import threading

import unittest
import nose
from zmq.eventloop import ioloop
from core.connectors import CommandConnector
from core.handlers import CommandHandler


class MyCommandConnector(CommandConnector):

    def __init__(self, name, end_point, handler):
        CommandConnector.__init__(self, name, end_point)
        self._stream.on_recv_stream(self._on_recv)
        self._handler = handler
        self._handler.start()

    def _on_recv(self, stream, msg):
        stream.close()

        print(msg[2])
        # self._handler.stop()
        nose.tools.ok_('hello word' == msg[2])


class CommunicationTest(unittest.TestCase):

    def connector_start(self):
        server = 'tcp://127.0.0.1:5555'
        handler = MyCommandHandler('MyCommandHandler', server)
        client = MyCommandConnector('MyCommandConnector', server, handler)
        client.connect()

        data = 'hello word'
        client.send(data)

        loop.start()

