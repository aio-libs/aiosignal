=========
Changelog
=========

..
    You should *NOT* be adding new change log entries to this file, this
    file is managed by towncrier. You *may* edit previous change logs to
    fix problems like typo corrections or such.
    To add a new change log entry, please see
    https://pip.pypa.io/en/latest/development/contributing/#news-entries
    we named the news folder "changes".

    WARNING: Don't drop the next directive!

.. towncrier release notes start

1.4 (2025-06-26)
================

Features
--------

- Added decorator functionality to ``Signal`` as a convenient way to add a callback -- by ``@Vizonex``.
  `#699 <https://github.com/aio-libs/aiosignal/pulls/699>`_

- Improved type safety by allowing callback parameters to be type checked (typing-extensions is now required for Python <3.13).
  Parameters for a ``Signal`` callback should now be defined like ``Signal[int, str]`` -- by @Vizonex and @Dreamsorcerer.
  `#699 <https://github.com/aio-libs/aiosignal/pulls/699>`_, `#710 <https://github.com/aio-libs/aiosignal/pulls/710>`_


Misc
----

- Removed the sphinxcontrib-asyncio documentation dependency.
  `#528 <https://github.com/aio-libs/aiosignal/pull/528>`_


----

1.3.2 (2024-12-13)
==================

Deprecations and Removals
-------------------------

- Dropped Python 3.7 support.
  `#413 <https://github.com/aio-libs/aiosignal/issues/413>`_

- Dropped Python 3.8 support.
  `#645 <https://github.com/aio-libs/aiosignal/issues/645>`_


Misc
----

- `#362 <https://github.com/aio-libs/aiosignal/issues/362>`_


----

1.3.1 (2022-11-08)
==================

Bugfixes
--------

- Removed stray quote and comma from setup.cfg preventing PyPI from accepting a
  release.
  `#361 <https://github.com/aio-libs/aiosignal/issues/361>`_


----


1.3.0 (2022-11-08)
==================

Features
--------

- Switched to declarative package setup.
  `#267 <https://github.com/aio-libs/aiosignal/issues/267>`_
- Added support for Python 3.11.
  `#360 <https://github.com/aio-libs/aiosignal/issues/360>`_


Deprecations and Removals
-------------------------

- Dropped Python 3.6 support.
  `#267 <https://github.com/aio-libs/aiosignal/issues/267>`_


----


1.2.0 (2021-10-16)
==================

Features
--------

- Added support for Python 3.10.
  `#328 <https://github.com/aio-libs/aiosignal/issues/328>`_


Bugfixes
--------

- Mark aiosignal as Python3-only package
  `#165 <https://github.com/aio-libs/aiosignal/issues/165>`_


----


1.1.2 (2020-11-27)
==================

Features
--------

- Fix MANIFEST.in to include ``aiosignal/py.typed`` marker


1.1.1 (2020-11-27)
==================

Features
--------

- Support type hints

1.1.0 (2020-10-13)
==================

Features
--------

- Added support of Python 3.8 and 3.9


1.0.0 (2019-11-11)
==================

Deprecations and Removals
-------------------------

- Dropped support for Python 3.5; only 3.6, 3.7 and 3.8 are supported going forward.
  `#23 <https://github.com/aio-libs/aiosignal/issues/23>`_
