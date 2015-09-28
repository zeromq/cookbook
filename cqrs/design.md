CQRS Style Architecture with 0MQ
================================

Features
-----------

 ** Message protocol** 
 ** Error handling for validation and execution problems**
 ** Read model** (QueryHandlers)
	 - De-normalization
	 -  Aggregation
 ** Writing model** (CommandHandlers)
	 - Command definition
	 - Command execution error handling
	 - Reliable change notification to read model
 ** Persistence** (EventStore)
	 - Append-only
	 - Read-model database

Components involved
---------------------------

** Connector** - client that send a Command or QueryRequest message to a CommandHandler or a QueryHandler

** CommandHandler** - server that receive Command message to processes from a client. The CommandHandler must garantee that each Event must be delivered and persisted by EventStore.

** EventStore** - server that receive Event to persist on specific event store, each event store are identified by there respective event name. EventStore must notify every 

** ProjectionsStore** - pipeline that receive change notifications from EventStore and update and specific data view. 

** QueryHandler** - server that receive a QueryRequest and run queries in one ProjectionStore.

Message Protocol
----------------------

Command - It is going to be the arguments to CommandHandler, every Command has a unique identifier.

QueryRequest - It is going to be the arguments to QueryHandler, by default it has page size and page num attributes

QueryResult - Wrap data return by QueryHandler and has two fields: count with query rows count of filter and data that is a collection with 0 or mode rows.

Event - list of Command attributes to be store on EventStore

CommandError - All command processing errors are return back to 

Error Handling
------------------


Write model
---------------


Read model
---------------


Further Readings
----------------

 [1]:http://udidahan.com/2009/12/09/clarified-cqrs/  Clarified CQRS 