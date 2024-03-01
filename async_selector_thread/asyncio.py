from __future__ import annotations

import asyncio

import typing
from typing import Any, Callable, Union

if typing.TYPE_CHECKING:
    from typing import Set  # noqa: F401
    from typing_extensions import Protocol

    class _HasFileno(Protocol):
        def fileno(self) -> int:
            pass

    _FileDescriptorLike = Union[int, _HasFileno]

from .selector_thread import SelectorThread

# AddThreadSelectorEventLoop: unmodified from tornado 6.4.0
class AddThreadSelectorEventLoop(asyncio.AbstractEventLoop):
    """Wrap an event loop to add implementations of the ``add_reader`` method family.

    Instances of this class start a second thread to run a selector.
    This thread is completely hidden from the user; all callbacks are
    run on the wrapped event loop's thread.

    This class is used automatically by Tornado; applications should not need
    to refer to it directly.

    It is safe to wrap any event loop with this class, although it only makes sense
    for event loops that do not implement the ``add_reader`` family of methods
    themselves (i.e. ``WindowsProactorEventLoop``)

    Closing the ``AddThreadSelectorEventLoop`` also closes the wrapped event loop.

    """

    # This class is a __getattribute__-based proxy. All attributes other than those
    # in this set are proxied through to the underlying loop.
    MY_ATTRIBUTES = {
        "_real_loop",
        "_selector",
        "add_reader",
        "add_writer",
        "close",
        "remove_reader",
        "remove_writer",
    }

    def __getattribute__(self, name: str) -> Any:
        if name in AddThreadSelectorEventLoop.MY_ATTRIBUTES:
            return super().__getattribute__(name)
        return getattr(self._real_loop, name)

    def __init__(self, real_loop: asyncio.AbstractEventLoop) -> None:
        self._real_loop = real_loop
        self._selector = SelectorThread(real_loop)

    def close(self) -> None:
        self._selector.close()
        self._real_loop.close()

    def add_reader(
        self, fd: "_FileDescriptorLike", callback: Callable[..., None], *args: Any
    ) -> None:
        return self._selector.add_reader(fd, callback, *args)

    def add_writer(
        self, fd: "_FileDescriptorLike", callback: Callable[..., None], *args: Any
    ) -> None:
        return self._selector.add_writer(fd, callback, *args)

    def remove_reader(self, fd: "_FileDescriptorLike") -> bool:
        return self._selector.remove_reader(fd)

    def remove_writer(self, fd: "_FileDescriptorLike") -> bool:
        return self._selector.remove_writer(fd)
