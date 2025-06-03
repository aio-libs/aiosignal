import sys
from typing import Awaitable, Callable, TypeVar
from frozenlist import FrozenList

if sys.version_info >= (3, 10):
    from typing import ParamSpec, Concatenate
else:
    from typing_extensions import ParamSpec, Concatenate

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

_P = ParamSpec("_P")
_T = TypeVar("_T", contravariant=True)
_AsyncFunc = Callable[_P, Awaitable[_T]]

__version__ = "1.3.2"

__all__ = ("Signal", "signal_func", "signal_method")


class Signal(FrozenList[_AsyncFunc[_P, _T]]):
    """Coroutine-based signal implementation.

    To connect a callback to a signal, use any list method.

    Signals are fired using the send() coroutine, which takes named
    arguments.
    """

    __slots__ = ("_owner",)

    def __init__(self, owner: object):
        super().__init__()
        self._owner = owner

    def __repr__(self) -> str:
        return "<Signal owner={}, frozen={}, {!r}>".format(
            self._owner, self.frozen, list(self)
        )

    async def send(self, *args: _P.args, **kwargs: _P.kwargs) -> None:
        """
        Sends data to all registered receivers.
        """
        if not self.frozen:
            raise RuntimeError("Cannot send non-frozen signal.")

        for receiver in self:
            await receiver(*args, **kwargs)

    def __call__(self, func: _AsyncFunc[_P, _T]) -> _AsyncFunc[_P, _T]:
        """Decorator to add a function to this Signal."""
        self.append(func)
        return func


def signal_func(_: _AsyncFunc[_P, None]) -> type[Signal[_P, None]]:
    """overrides a function to define a function as a
    signal that can be defined with typehinted parameters::

        from aiosignal import signal_func

        @signal_func
        async def my_signal(a:int, b:int) -> None:...

        # my_signal has been transformed to a Signal
        # and it should now be typehinted as:
        # (owner: object) -> Signal[(a: int, b: int), None]

        event = my_signal(None)

        # Now we can create helpuful callbacks with
        # helpful parameters to help us if were stuck...

        @event
        async def on_my_event(a:int, b:int):
            ...

    """
    return Signal


def signal_method(_: _AsyncFunc[Concatenate[Self, _P], None]) -> type[Signal[_P, None]]:
    """Helper that typehints a class method as a signal
    This could help assist in creating Protocol Types that can
    define the creation of an object

    ::

        from typing import TypeVar, Protocol

        A = TypeVar("A")
        B = TypeVar("B")

        class MySignalProtocol(Protocol[A, B]):
            @signal_method
            def __call__(self, a: A, b: B) -> None:...

        MySignal: MySignalProtocol[dict, int] = Signal

        # Signal is now been typehinted via protocol
        # pyright or other ides should be able to
        # identify it as:
        #   (owner:object) -> Signal[(a: dict, b: int), None]

        signal = MySignal()

    """
    return Signal
