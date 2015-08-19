routingService
==============

Some POCs of data routing service implementing on MSA.

::

  +-----------+  +-----------+
  |           |  |           |
  | ServiceA <----> Router  <-----> Controller
  |           |  |     ^     |        ^ 
  +-----------+  +-----|-----+        |
                       |              |
                       |        +-----|-----+  +-----------+
                       |        |     v     |  |           |
                       +---------> Router  <----> ServiceB |
                                |           |  |           |
                                +-----------+  +-----------+

Run in Docker Container
-------------------------

#. Build a base image use the ``Dockerfile`` provided::

    docker build -t pyzmq:latest .

#. Set containers up with ``docker-compose`` ::

    docker-compose up -d

Container logs are redirected to syslog, instead of ``docker-compose logs`` use ``tail -f /var/log/syslog`` .

References
-----------

* agent.py - mainly purpose of this component is to redirect directives to Portal Service.
    
    listening port:6002
    
    //TODO: And it will build data pipelines between MicroServices and also support LoadBalance/Service discovery.

* portal.py - a gateway which provides accessability to MicroService for agent.py.

    listening port:6003

    An EntryPoint will be generated according to directives which sent from agent.py.

    With the help of different plugins of input/output/exchange, portal.py will adapt various kinds of MicroServices.

    If it couldn't support your MicroService, write plugins for it!

