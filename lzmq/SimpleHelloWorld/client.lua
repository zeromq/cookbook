local zthreads = require "lzmq.threads"

-- If we run as thread we get global context
-- If we run as process we create new context
local ctx = zthreads.context()

-- Create new REQ socket and connect to the server
local skt, err = ctx:socket{"REQ",
  connect = "tcp://127.0.0.1:5555"
}
if not skt then
  print("Can not create client socket:", err)
  os.exit(1)
end

-- Send message
local ok, err = skt:send("Hello")
if not ok then
  print("Can not send hello message:", err)
  os.exit(1)
end

-- Recv server response
local msg, err = skt:recv()
if not msg then
  print("Can not recv server response:", err)
  os.exit(1)
end

print("Client recv message:", msg)

