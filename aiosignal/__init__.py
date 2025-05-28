import sys
import typing

from frozenlist import FrozenList

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

P = ParamSpec("P")
T = typing.TypeVar("T")
AsyncFunc = typing.Callable[P, typing.Awaitable[T]]

__version__ = "1.3.2"

__all__ = ("Signal",)


class Signal(FrozenList[AsyncFunc[P, T]]):
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

    async def send(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """
        Sends data to all registered receivers.
        """
        if not self.frozen:
            raise RuntimeError("Cannot send non-frozen signal.")

        for receiver in self:
            await receiver(*args, **kwargs)

    def __call__(self, func: AsyncFunc[P, T]) -> AsyncFunc[P, T]:
        """wraps a callback function to the signal."""
        self.append(func)
        return func
