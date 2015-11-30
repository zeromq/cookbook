Problem: I don't know zeromq and want to learn the simplest usage, show me some code
==============================================

The simplest example is client-server. Client sends "Hello" and server replies with "World".

Design
======

The recipe is divided to a client and server, client connects to the server and send a request, server binds and sending a reply.

Client uses a CLIENT socket type.
Server uses a SERVER socket type.

Clients steps:

1. Create a CLIENT socket
2. Connect to the server
3. Send "Hello" request message
4. Receive reply message

Server steps:

1. Create SERVER socket
2. Binds the socket
3. Receive request message
4. Send "World" reply message

Implementations:
===================
* [GOCZMQ](https://github.com/zeromq/cookbook/blob/master/goczmq/simple_helloworld_test.go)
* [NetMQ](https://github.com/zeromq/cookbook/blob/master/netmq/HelloWorld.cs)
* [PyZMQ](https://github.com/zeromq/cookbook/blob/master/pyzmq/helloword)

References:
==============
* [NetMQ](http://netmq.readthedocs.org/en/latest/)
* [goczmq](https://github.com/zeromq/goczmq)
* [PyZMQ](http://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/patterns/client_server.html)
* [PyZMQ Examples](https://github.com/zeromq/pyzmq/blob/master/examples/)