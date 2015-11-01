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


class Handler:

    def __init__(self, name, frontend_point, backend_point, context = None, loop = None):
        self._context = context or zmq.Context.instance()
        self._loop = loop or ioloop.IOLoop().instance()
        self._name = name
        self._frontend_point = frontend_point
        self._backend_point = backend_point

    @property
    def get_name(self):
        return self._name

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def _on_recv_frontend(self, stream, msg):
        pass

    @abstractmethod
    def _on_recv_backend(self, stream, msg):
        pass


class CommandHandler(Handler):

    def __init__(self, name, frontend_point, backend_point, context = None, loop = None):
        Handler.__init__(self,  name, frontend_point, backend_point, context, loop)

        self._frontend = self._context.socket(zmq.ROUTER)
        self._frontend.setsockopt(zmq.IDENTITY,'FRONTEND-{0}'.format( self._name))

        self._backend = self._context.socket(zmq.DEALER)
        self._backend.setsockopt(zmq.IDENTITY,'BACKEND-{0}'.format( self._name))

        self._stream_frontend = zmqstream.ZMQStream(self._frontend)
        self._stream_frontend.on_recv_stream(self._on_recv_frontend)

        self._stream_backend = zmqstream.ZMQStream(self._backend)
        self._stream_backend.on_recv_stream(self._on_recv_backend)

        self.log = logging.getLogger(__name__)

    def start(self):
        self._stream_backend.bind(self._backend_point)
        self.log.info('command handler backend started')
        self._stream_frontend.bind(self._frontend_point)
        self.log.info('command handler frontend started')
        self._loop.start()

    def stop(self):
        self._stream_frontend.stop_on_send()
        self._stream_frontend.stop_on_recv()
        self._stream_backend.stop_on_recv()
        self._stream_backend.stop_on_send()
        self._stream_frontend.close()
        self._stream_backend.close()
        self.log.info('command handler stopped')
