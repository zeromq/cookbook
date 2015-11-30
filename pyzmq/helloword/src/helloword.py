"""Example using zmq with asyncio coroutines"""
# Copyright (c) PyZMQ Developers.
# This example is in the public domain (CC-0)
import asyncio
import zmq
import zmq.asyncio
from zmq.error import ZMQError


context = zmq.Context()
endpoint = 'tcp://127.0.0.1:5555'

srv = context.socket(zmq.REP)
clt = context.socket(zmq.REQ)

srv.bind(endpoint)
print('server online')

print("Connecting to server...")
clt.connect(endpoint)

while True:
    clt.send_string("Hello")

    message = srv.recv_string()
    print("server: {0} client".format(message))
    srv.send_string('World')

    msg = clt.recv_string()
    print('Thank you: Hello {0}'.format(msg))

