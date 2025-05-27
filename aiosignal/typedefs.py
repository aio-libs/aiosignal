import sys 
import typing

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

P = ParamSpec("P")
T = typing.TypeVar("T")
AsyncFunc = typing.Callable[P, typing.Coroutine[T]]

