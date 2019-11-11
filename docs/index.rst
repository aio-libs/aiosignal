aiosignal
=========

A project to manage callbacks in `asyncio` projects.

``Signal`` is a list of registered asynchronous callbacks.

The signal's life-cycle has two stages: after creation its content
could be filled by using standard list operations: ``sig.append()``
etc.

After you call ``sig.freeze()`` the signal is *frozen*: adding, removing
and dropping callbacks is forbidden.

The only available operation is calling the previously registered
callbacks by using ``await sig.send(data)``.

For concrete usage examples see the :ref:`aiohttp:aiohttp-web-signals` section of the :doc:`aiohttp:web_advanced` chapter of the :doc:`aiohttp documentation <aiohttp:index>`.

API
---

.. class:: aiosignal.Signal(owner)

   The signal, implements the :class:`collections.abc.MutableSequence`
   interface. The *owner* object is shown in the signal representation,
   and is there to make debugging easier.

   .. method:: send(*args, **kwargs)
      :async:

      Call all registered callbacks one by one starting from the beginning
      of the list.

   .. attribute:: frozen

      ``True`` if :meth:`freeze` was called, read-only property.

   .. method:: freeze()

      Freeze the list. After calling, any content modification is forbidden.

Installation
------------

.. code-block:: bash

   $ pip install aiosignal

The library requires Python 3.6 or newer.

Dependencies
------------

aiosignal depends on the frozenlist_ library.

Documentation
=============

https://aiosignal.readthedocs.io/

Communication channels
======================

*aio-libs discourse group*: https://aio-libs.discourse.group

Feel free to post your questions and ideas here.

*gitter chat* https://gitter.im/aio-libs/Lobby

Requirements
============

- Python >= 3.6
- frozenlist >= 1.0.0

License
=======

``aiosignal`` is offered under the Apache 2 license.

Source code
===========

The project is hosted on GitHub_

Please file an issue in the `bug tracker
<https://github.com/aio-libs/aiosignal/issues>`_ if you have found a bug
or have some suggestions to improve the library.

Authors and License
===================

The ``aiosignal`` package was originally part of the
:doc:`aiohttp project <aiohttp:index>`, written by Nikolay Kim and Andrew Svetlov.
It is now being maintained by Martijn Pieters.

It's *Apache 2* licensed and freely available.

Feel free to improve this package and send a pull request to GitHub_.


.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`


.. _GitHub: https://github.com/aio-libs/aiosignal
.. _frozenlist: https://github.com/aio-libs/frozenlist
