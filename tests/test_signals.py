import re
from unittest import mock
from typing import Protocol, cast, Awaitable

import pytest

from aiosignal import Signal, signal_func, signal_method


class Owner:
    def __repr__(self) -> str:
        return "<Owner 0xdeadbeef>"


@pytest.fixture
def owner() -> Owner:
    return Owner()


async def test_add_signal_handler_not_a_callable(owner: Owner) -> None:
    callback = True
    signal = Signal(owner)
    signal.append(callback)
    signal.freeze()
    with pytest.raises(TypeError):
        await signal.send()


async def test_function_signal_dispatch_kwargs(owner: Owner) -> None:
    signal = Signal(owner)
    kwargs = {"foo": 1, "bar": 2}

    callback_mock = mock.Mock()

    async def callback(**kwargs):
        callback_mock(**kwargs)

    signal.append(callback)
    signal.freeze()

    await signal.send(**kwargs)
    callback_mock.assert_called_once_with(**kwargs)


async def test_function_signal_dispatch_args_kwargs(owner: Owner) -> None:
    signal = Signal(owner)
    args = {"a", "b"}
    kwargs = {"foo": 1, "bar": 2}

    callback_mock = mock.Mock()

    async def callback(*args, **kwargs):
        callback_mock(*args, **kwargs)

    signal.append(callback)
    signal.freeze()

    await signal.send(*args, **kwargs)
    callback_mock.assert_called_once_with(*args, **kwargs)


async def test_non_coroutine(owner: Owner) -> None:
    signal = Signal(owner)
    kwargs = {"foo": 1, "bar": 2}

    callback = mock.Mock()

    signal.append(callback)
    signal.freeze()

    with pytest.raises(TypeError):
        await signal.send(**kwargs)


def test_setitem(owner: Owner) -> None:
    signal = Signal(owner)
    m1 = mock.Mock()
    signal.append(m1)
    assert signal[0] is m1
    m2 = mock.Mock()
    signal[0] = m2
    assert signal[0] is m2


def test_delitem(owner: Owner) -> None:
    signal = Signal(owner)
    m1 = mock.Mock()
    signal.append(m1)
    assert len(signal) == 1
    del signal[0]
    assert len(signal) == 0


def test_cannot_append_to_frozen_signal(owner: Owner) -> None:
    signal = Signal(owner)
    m1 = mock.Mock()
    m2 = mock.Mock()
    signal.append(m1)
    signal.freeze()
    with pytest.raises(RuntimeError):
        signal.append(m2)

    assert list(signal) == [m1]


def test_cannot_setitem_in_frozen_signal(owner: Owner) -> None:
    signal = Signal(owner)
    m1 = mock.Mock()
    m2 = mock.Mock()
    signal.append(m1)
    signal.freeze()
    with pytest.raises(RuntimeError):
        signal[0] = m2

    assert list(signal) == [m1]


def test_cannot_delitem_in_frozen_signal(owner: Owner) -> None:
    signal = Signal(owner)
    m1 = mock.Mock()
    signal.append(m1)
    signal.freeze()
    with pytest.raises(RuntimeError):
        del signal[0]

    assert list(signal) == [m1]


async def test_cannot_send_non_frozen_signal(owner: Owner) -> None:
    signal = Signal(owner)

    callback_mock = mock.Mock()

    async def callback(**kwargs):
        callback_mock(**kwargs)  # pragma: no cover  # mustn't be called

    signal.append(callback)

    with pytest.raises(RuntimeError):
        await signal.send()

    assert not callback_mock.called


def test_repr(owner: Owner) -> None:
    signal = Signal(owner)

    signal.append(mock.Mock(__repr__=lambda *a: "<callback>"))

    assert (
        re.match(
            r"<Signal owner=<Owner 0xdeadbeef>, frozen=False, " r"\[<callback>\]>",
            repr(signal),
        )
        is not None
    )

async def test_decorator_callback_dispatch_args_kwargs(owner: Owner) -> None:
    signal = Signal(owner)
    args = {"a", "b"}
    kwargs = {"foo": 1, "bar": 2}

    callback_mock = mock.Mock()

    @signal
    async def callback(*args: object, **kwargs: object) -> None:
        callback_mock(*args, **kwargs)

    signal.freeze()
    await signal.send(*args, **kwargs)


async def test_paramspec_argument_passing_from_function(owner: Owner):

    @signal_func
    async def defined_signal(foo: int, bar: int):
        return

    assert defined_signal == Signal, "Signal did not pass"

    signal = defined_signal(owner)
    args = {"a", "b"}
    kwargs = {"foo": 1, "bar": 2}

    callback_mock = mock.Mock()

    @signal
    async def callback(*args: object, **kwargs: object) -> None:
        callback_mock(*args, **kwargs)

    signal.freeze()
    await signal.send(*args, **kwargs)


async def test_paramspec_argument_passing_from_protocol(owner: Owner):

    class MySignalProtocol(Protocol):
        @signal_method
        def __call__(self, foo: int, bar: int) -> Awaitable[None]:
            return

    # Casting Signals from protocol is one of the methods of type-casting
    # What the signal is...
    signal = cast(MySignalProtocol, Signal)(owner)
    args = {"a", "b"}
    kwargs = {"foo": 1, "bar": 2}

    callback_mock = mock.Mock()

    @signal
    async def callback(*args: object, **kwargs: object) -> None:
        callback_mock(*args, **kwargs)

    signal.freeze()
    await signal.send(*args, **kwargs)
