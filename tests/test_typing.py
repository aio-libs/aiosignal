"""Static-typing regression tests for ``Signal``.

``Signal``'s headline feature is that callback parameters are type
checked: ``Signal[int, str]`` constrains both ``append()`` and
``send()``.  Nothing in the runtime test suite can observe that, so this
module asserts it against MyPy instead.  It is type checked by the
``mypy-py311``/``mypy-py313`` pre-commit hooks via ``.mypy.ini``'s
``files = aiosignal, tests``.

Two complementary mechanisms, both dependency-free:

* ``assert_type()`` pins an inferred type.  Widening it (e.g. to ``Any``)
  fails the check.  At runtime it is a no-op.
* ``# type: ignore[code]`` asserts that MyPy *does* report ``code``
  there.  ``.mypy.ini`` sets ``warn_unused_ignores = True``, so the
  assertion is bidirectional: if the error stops being reported the
  ignore becomes unused and MyPy fails.

Helpers are named ``_check_*`` rather than ``test_*`` on purpose -- MyPy
checks unexecuted function bodies, and the negative cases would raise at
runtime if pytest called them.
"""

import sys
from typing import Awaitable, Callable

from aiosignal import Signal

if sys.version_info >= (3, 11):
    from typing import Unpack, assert_type
else:
    from typing_extensions import Unpack, assert_type


class Owner:
    pass


async def _int_str(a: int, b: str) -> None:
    """A callback matching ``Signal[int, str]``."""


async def _str_only(a: str) -> None:
    """A callback that matches no signal used below."""


def _sync(a: int, b: str) -> None:
    """A non-coroutine callback."""


# --- accepted usage -------------------------------------------------


async def _check_parameterised_signal() -> None:
    signal = Signal[int, str](Owner())
    signal.append(_int_str)
    signal.freeze()
    await signal.send(42, "foo")


async def _check_bare_signal_takes_no_positional_args() -> None:
    """The ``_Ts`` default is an empty tuple, so ``send()`` takes none."""
    signal = Signal(Owner())
    signal.freeze()
    await signal.send()


async def _check_homogeneous_variadic_signal() -> None:
    signal = Signal[Unpack[tuple[str, ...]]](Owner())
    signal.freeze()
    await signal.send()
    await signal.send("a")
    await signal.send("a", "b", "c")


async def _check_kwargs_are_unconstrained() -> None:
    """``send()`` forwards arbitrary keyword arguments (``**kwargs: Any``)."""
    signal = Signal(Owner())
    signal.freeze()
    await signal.send(foo=1, bar="two")


# --- inferred types -------------------------------------------------


def _check_element_type() -> None:
    signal = Signal[int, str](Owner())
    assert_type(signal[0], Callable[[int, str], Awaitable[object]])
    assert_type(signal.frozen, bool)


async def _check_send_returns_none() -> None:
    """``send()`` discards each callback's return value."""
    signal = Signal[int](Owner())
    assert_type(await signal.send(1), None)


def _check_decorator_preserves_signature() -> None:
    """``__call__`` registers the callback and returns it unchanged."""
    signal = Signal[int, str](Owner())

    @signal
    async def callback(a: int, b: str) -> None:
        """Registered via the decorator form."""

    assert_type(callback, Callable[[int, str], Awaitable[None]])


def _check_decorator_preserves_return_type() -> None:
    """The callback's own return type survives; only ``send()`` drops it."""
    signal = Signal[int](Owner())

    @signal
    async def callback(a: int) -> str:
        return "result"

    assert_type(callback, Callable[[int], Awaitable[str]])


# --- rejected usage -------------------------------------------------
#
# Every ``type: ignore`` below asserts the error is still reported.


def _check_append_rejects_mismatched_callback() -> None:
    signal = Signal[int, str](Owner())
    signal.append(_str_only)  # type: ignore[arg-type]


def _check_append_rejects_sync_callback() -> None:
    signal = Signal[int, str](Owner())
    signal.append(_sync)  # type: ignore[arg-type]


def _check_decorator_rejects_mismatched_callback() -> None:
    signal = Signal[int, str](Owner())

    @signal  # type: ignore[arg-type]
    async def callback(a: str) -> None:
        """Wrong parameter type for this signal."""


def _check_decorator_rejects_sync_callback() -> None:
    signal = Signal[int, str](Owner())

    @signal  # type: ignore[arg-type]
    def callback(a: int, b: str) -> None:
        """Not a coroutine function."""


async def _check_send_rejects_wrong_type() -> None:
    signal = Signal[int, str](Owner())
    await signal.send("not an int", "foo")  # type: ignore[arg-type]


async def _check_send_rejects_too_few_args() -> None:
    signal = Signal[int, str](Owner())
    await signal.send(42)  # type: ignore[call-arg]


async def _check_send_rejects_too_many_args() -> None:
    signal = Signal[int, str](Owner())
    await signal.send(42, "foo", None)  # type: ignore[call-arg]


async def _check_bare_signal_send_rejects_args() -> None:
    """Guards the ``_Ts`` default -- without it this would be unchecked."""
    signal = Signal(Owner())
    await signal.send(42)  # type: ignore[call-arg]


async def _check_homogeneous_variadic_signal_rejects_wrong_type() -> None:
    signal = Signal[Unpack[tuple[str, ...]]](Owner())
    await signal.send("a", 2)  # type: ignore[arg-type]


def _check_signal_requires_an_owner() -> None:
    Signal()  # type: ignore[call-arg]


def test_typing_module_is_importable() -> None:
    """Keep pytest from reporting an empty module.

    The real assertions in this file are made by MyPy, not at runtime.
    """
    assert Signal[int, str](Owner()).frozen is False
