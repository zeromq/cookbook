local zthreads = require "lzmq.threads"

-- If we run as thread we get global context
-- If we run as process we create new context
local ctx = zthreads.context()

-- Create new REP socket and bind on interface
local skt, err = ctx:socket{"REP",
  bind = "tcp://*:5555"
}
if not skt then
  print("Can not create server socket:", err)
  os.exit(1)
end

-- Send message
local msg, err = skt:recv()
if not msg then
  print("Can not recv hello message:", err)
  os.exit(1)
end

print("Server recv message:", msg)

-- Recv server response
local ok, err = skt:send("World")
if not ok then
  print("Can not send server response:", err)
  os.exit(1)
end

