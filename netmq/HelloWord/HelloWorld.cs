using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NetMQ;
using NUnit.Framework;

namespace netmq
{
    /// <summary>
    /// Problem: We want to send a message and receive a reply
    /// Solution: Let's write a simple "Hello World" client and server.
    /// </summary>
    [TestFixture]
    public class HelloWorld
    {
        [Test]
        public void HelloWorldTest()
        {
            // context must be created to create sockets, one context per application
            using (NetMQContext context = NetMQContext.Create())
            {
                Task.Factory.StartNew(() => Server(context));
                Client(context);
            }                
        }

        /// <summary>
        /// Client does the following:
        /// * Creates a Request socket
        /// * Sends a "Hello" message
        /// * Waits for a "World" reply
        /// </summary>
        /// <param name="context"></param>
        private void Client(NetMQContext context)
        {
            // creating the request socket inside using to automatically dispose the socket
            using (var request = context.CreateRequestSocket())
            {
                // connecting to the response socket
                request.Connect("tcp://localhost:5555");

                // sending a request message, SendFrame has multiple overload you can use"
                request.SendFrame("Hello");

                // Receive the reply message from the server. Note that
                // this ReceiveFrameString() call will block forever waiting
                // for a message. 
                var reply = request.ReceiveFrameString();

                Assert.That(reply == "World");
            }
        }

        /// <summary>
        /// SimpleHelloWorldServer does the following:
        /// * Creates a Response socket
        /// * Waits for a "Hello" request
        /// * Sends a "World" reply
        /// </summary>
        /// <param name="context"></param>
        private void Server(NetMQContext context)
        {
            // create the response socket
            using (var response = context.CreateResponseSocket())
            {
                // bind the response socket, binds make the socket the "server"
                // * can be used to bind to all IP addresses
                response.Bind("tcp://*:5555");

                // response socket must first receive a message and only then reply
                string request = response.ReceiveFrameString();

                Assert.That(request == "Hello");

                response.SendFrame("World");
            }
        }
    }
}
