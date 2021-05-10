# asyncio-selector-thread

Provide asyncio selector methods (add/remove_reader/writer)
when asyncio itself doesn't (i.e. ProactorEventLoop).

This is initially extracted from tornado 6.1, which defined the AddThreadSelectorLoop.
