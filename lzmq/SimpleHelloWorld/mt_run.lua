-- Run HelloWorld example in multithreaded environment

local zthreads = require "lzmq.threads"

-- all threads use same global ZMQ context

-- run server in separate thread
local server = zthreads.xfork("@./server.lua"):start()

-- run client in separate thread
local client = zthreads.xfork("@./client.lua"):start()

-- wait server thread
server:join()

-- wait client thread
client:join()
