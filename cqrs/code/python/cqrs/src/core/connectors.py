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

import logging
import zmq
from zmq.eventloop import zmqstream

logger = logging.getLogger('cqrs-core')


class Connector:

    def __init__(self, name, end_point, context=None):
        self._context = context or zmq.Context.instance()
        self._name = name
        self._end_point = end_point

        logger.info('command handler initialized')

    def _on_recv(self, stream, msg):
        logger.info('data received')


class CommandHandlerConnector(Connector):

    def __init__(self, name, end_point, context=None):
        super(CommandHandlerConnector, self).__init__(name, end_point, context)
        self._sockt = self._context.socket(zmq.REQ)
        self._stream = zmqstream.ZMQStream(self._sockt)
        self._stream.on_recv_stream(self._on_recv)

    def connect(self):
        self._sockt.connect(self._end_point)

    def send(self, data):
        self._sockt.send_pyobj(data)


class QueryHandlerConnector(Connector):

    def __init__(self, name, end_point, context=None):
        super(QueryHandlerConnector, self).__init__(name, end_point, context)
