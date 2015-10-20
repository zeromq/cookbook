Problem: I don't know zeromq and want to learn the simplest usage, show me some code
==============================================

The simplest example is client-server. Client sends "Hello" and server replies with "World".

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

* [GOCZMQ](https://github.com/zeromq/cookbook/blob/master/goczmq/simple_helloworld_test.go)
* [NetMQ](https://github.com/zeromq/cookbook/blob/master/netmq/HelloWorld.cs)
