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
import time

from core.workers import CommandWorker


class MyCommandWorker(CommandWorker):

    def __init__(self, name, end_point):
        CommandWorker.__init__(self, name, end_point)

    def _on_recv(self, msg):

        self._sockt.send(msg)
        time.sleep(1)
        self.log.info('work finished {0}'. format(msg))


if __name__ == "__main__":

    server = 'tcp://127.0.0.1:5556'

    try:
        for i in range(1,2):
            worker = MyCommandWorker('MyCommandWorker-{0}'.format(i), server)
            worker.connect()

            while True:
                pass
    except KeyboardInterrupt, error:
        pass



