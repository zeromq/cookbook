/*
Problem: We want to send a message and receive a reply

Solution: Let's write a simple "Hello World" client and server.
We'll write them as go tests, so that we can verify that they
work.  To run this test, you can run "go test -run SimpleHelloWorld"
in the same directory as this file.
*/

package main

import (
	"log"

	"github.com/zeromq/goczmq"
)

// SimpleHelloWorldClient does the following:
// * Creates a ZMQ_REQ socket
// * Sends a "Hello" message
// * Waits for a "World" reply
func SimpleHelloWorldClient() {
	log.Printf("client starting...")

	// Create a ZMQ_REQ client using a "smart constructor".
	// See: https://godoc.org/github.com/zeromq/goczmq#NewReq

	client, err := goczmq.NewReq("tcp://localhost:5555")
	if err != nil {
		log.Fatalf("client.NewReq error: %s", err)
	}

	// Here, we make sure the socket is destroyed
	// when this function exits. While Go is a garbage
	// collected language, we're binding a C library,
	// so we need to make sure to clean up.

	defer client.Destroy()

	// Let's create a request message. GoCZMQ uses slices
	// of byte slices for messages, because they map
	// very simply to ZeroMQ "frames".

	request := [][]byte{[]byte("Hello")}

	// Send the message and check for any errors.

	err = client.SendMessage(request)
	if err != nil {
		log.Fatalf("client.SendMessage error: %s", err)
	}

	log.Printf("client.SendMessage '%s'", request)

	// Receive the reply message from the server. Note that
	// this RecvMessage() call will block forever waiting
	// for a message.

	reply, err := client.RecvMessage()
	if err != nil {
		log.Fatalf("client.RecvMessage error: %s", err)
	}

	log.Printf("client.RecvMessage: '%s'", reply)
}

// SimpleHelloWorldServer does the following:
// * Creates a ZMQ_REP socket
// * Waits for a "Hello" request
// * Sends a "World" reply
func SimpleHelloWorldServer() {
	log.Printf("server starting...")

	// Create a ZMQ_REP server using a "smart constructor".
	// See: https://godoc.org/github.com/zeromq/goczmq#NewRep

	server, err := goczmq.NewRep("tcp://*:5555")
	if err != nil {
		log.Fatalf("server.NewRep error: %s", err)
	}

	// Here, we make sure the socket is destroyed
	// when this function exits. While Go is a garbage
	// collected language, we're binding a C library,
	// so we need to make sure to clean up.

	defer server.Destroy()

	// Let's wait for a message from a client. Note that
	// this RecvMessage call will block forever waiting.

	request, err := server.RecvMessage()
	if err != nil {
		log.Fatalf("server.RecvMessage error: %s", err)
	}

	log.Printf("server.RecvMessage: '%s'", request)

	// Here we create a reply message. GoCZMQ uses slices
	// of byte slices for messages, because they map
	// very simply to ZeroMQ "frames".

	reply := [][]byte{[]byte("World")}

	// Send the message and check for any errors.

	err = server.SendMessage(reply)
	if err != nil {
		log.Fatalf("server.SendMessage error: %s", err)
	}

	log.Printf("server.SendMessage: '%s'", reply)
}

// TestSimpleHelloWorld starts SimpleHelloWorldServer in
// a goroutine, then starts a SimpleHelloWorldClient
func main() {
	go SimpleHelloWorldServer()
	SimpleHelloWorldClient()
}
