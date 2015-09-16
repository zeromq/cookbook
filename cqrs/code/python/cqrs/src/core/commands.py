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

class CommandRequest:

    def __init__(self, end_point, server, sockt):
        self._end_point = None
        self._server = server
        logger.info('c ommand request initialized')

    def start(self):
        self._sockt.setsockopt(zmq.IDENTITY, self._end_point)
        self._sockt.connect(self._server)
        logger.info('command request started')


class CommandHandler:

    def __init__(self, registry, end_point, sockt):
        self._end_point = end_point
        self._stream = zmqstream.ZMQStream(sockt)
        self._registry = registry
        logger.info('command handler initialized')

    def start(self):
        self._stream.on_recv_stream(self._on_recv)
        self._stream.on_send_stream(self._on_send)
        self._stream.bind(self._end_point)
        logger.info('command request started')

    def stop(self):
        self._stream.stop_on_send()
        self._stream.stop_on_recv()
        logger.info('command request stopped')

    def _on_recv(self, stream, msg):
        logger.info('data received')

    def _on_send(self, stream, msg, status):
        pass

    def on_validation(self):
        return False

    def on_execution(self):
        pass

    def command_handler(self, arguments):

        if self.on_validation(arguments):
            self.on_execution()


class CommandRegistry:

    def __init__(self):
        self._commands = {}
        self._context = zmq.Context()

    def _create_command(self, ep):

        if not self._commands.get(ep):
            s = self._context.socket(zmq.ROUTER)
            self._commands[ep] = CommandHandler(ep, s)

    def add_command(self, end_point):
        pass


