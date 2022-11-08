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
