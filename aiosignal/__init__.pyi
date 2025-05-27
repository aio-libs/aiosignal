from typing import Any, Generic, TypeVar

from frozenlist import FrozenList
from .typedefs import P, AsyncFunc

__all__ = ("Signal",)

_T = TypeVar("_T")

class Signal(FrozenList[AsyncFunc[P, _T]], Generic[_T]):
    def __init__(self, owner: Any) -> None: ...
    def __repr__(self) -> str: ...
    async def send(self, *args: P.args, **kwargs: P.kwargs) -> None: ...
