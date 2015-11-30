## Problem: We need a reference implementation of CQRS style architecture.
=================================================================

description here


## Design
![diagram missing](img/0.jpg)

## Features
###1. Basic communication
###2. Error handling
   - Reliability
###3. Communication messages
   - Business messages
   - Business errors
###4. Domain commands handling
###5. Domain events propagation
###6. Domain events persistence
###7. Domain events projections

## Implementations:

* [PyZMQ](https://github.com/zeromq/cookbook/blob/master/pyzmq/cqrs)

## References
- [CQRS](http://martinfowler.com/bliki/CQRS.html) - http://martinfowler.com/bliki/CQRS.html
 
- [Clarified CQRS](http://udidahan.com/2009/12/09/clarified-cqrs/) - http://udidahan.com/2009/12/09/clarified-cqrs/ 