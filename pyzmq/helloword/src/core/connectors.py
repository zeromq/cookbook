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

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


class Connector:

    def __init__(self, name, end_point, context=None):
        self._context = context or zmq.Context.instance()
        self._name = name
        self._end_point = end_point

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def _on_recv(self, stream, msg):
        pass

    @abstractmethod
    def send(self, data):
        pass


class CommandConnector(Connector):

    def __init__(self,  name, end_point, context=None):
        Connector.__init__(self,  name, end_point, context)
        self._sockt = self._context.socket(zmq.REQ)
        self._sockt.setsockopt(zmq.IDENTITY, self._name)
        self._stream = zmqstream.ZMQStream(self._sockt)
        self.log = logger.getChild('command-connector')

    def connect(self):
        self.log.info(' try connect to {0} '.format(self._end_point))
        self._sockt.connect(str(self._end_point))
        self.log.info('connected to {0} '.format(self._end_point))

    def send(self, data):
        self._sockt.send(data, copy=False)


class QueryHandlerConnector(Connector):

    def __init__(self,  name, end_point, context=None):
        Connector.__init__(self,  name, end_point, context)
