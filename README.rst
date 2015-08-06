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

