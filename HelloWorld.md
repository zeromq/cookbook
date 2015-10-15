Problem: I don't know zeromq and want to learn the simplest usage, show me some code
==============================================

The simplest example is request-reply. You want to send a message and receive a reply.

The recipe is divided to a client and server, client connects to the server and send a request, server binds and sending a reply.

Client uses a REQ socket type, the REQ socket type must first send a message and then wait for reply message.
Server uses a REP socket type, the REP socket type must first wait for request message and then send a reply message.

Clients steps:

1. Create a REQ socket
2. Connect to the server
3. Send an "Hello" request messae
4. Receive a message

Server steps:

1. Create REP socket
2. Binds the socket
3. Receive a request message
4. Send a "World" reply message

Implementations:

* [GOCZMQ](https://github.com/zeromq/cookbook/blob/master/goczmq/simple_helloworld_test.go)
* [NetMQ](https://github.com/zeromq/cookbook/blob/master/netmq/HelloWorld.cs)
