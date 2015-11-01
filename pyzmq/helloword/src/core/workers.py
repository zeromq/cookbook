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
from zmq.eventloop import zmqstream


class CommandWorker:

    def __init__(self, name, end_point, context = None):
        self._context = context or zmq.Context.instance()
        self._name = name
        self._end_point = end_point
        self._sockt = self._context.socket(zmq.REP)
        self.log = logging.getLogger(__name__)

    @property
    def get_name(self):
        return self._name

    def connect(self):
        self._sockt.connect(self._end_point)
        self.log.info('command worker connected to {0}'.format(self._end_point))

        while True:
            msg = self._sockt.recv(copy=False)
            self.log.info('work requested {0}'.format(msg))
            self._on_recv(msg)

    @abstractmethod
    def _on_recv(self, msg):
        pass
