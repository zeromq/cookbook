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
from abc import abstractmethod

import logging
import zmq
from zmq.eventloop import ioloop, zmqstream

loop = ioloop.IOLoop().instance()

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


class CommandHandler:

    def __init__(self, name, end_point):
        self._context = zmq.Context.instance()
        self._name = name
        self._end_point = end_point
        self._sockt = self._context.socket(zmq.REP)
        self._stream = zmqstream.ZMQStream(self._sockt)
        self._stream.on_recv_stream(self._on_recv)
        self.log = logger

    @property
    def get_name(self):
        return self._name

    def start(self):
        self._stream.bind(self._end_point)
        self.log.info('command handler started')

    def stop(self):
        self._stream.stop_on_send()
        self._stream.stop_on_recv()
        self._stream.close()
        self.log.info('command handler stopped')

    @abstractmethod
    def _on_recv(self, stream, msg):
        pass

    @abstractmethod
    def _on_send(self, stream, msg, status):
        pass
