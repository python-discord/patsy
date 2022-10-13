from sqlalchemy.ext import asyncio

class _SessionClassMethods:
    @classmethod
    def close_all(cls) -> None: ...
    @classmethod
    def identity_key(cls, *args, **kwargs): ...
    @classmethod
    def object_session(cls, instance): ...

class _SessionManager:
    async def __aenter__(self) -> asyncio.AsyncSession:
        ...

class sessionmaker(_SessionClassMethods):
    """Simple stub to better type hint the type of session, and the method available."""
    class_: asyncio.AsyncSession

    def __init__(
        self,
        bind=None,
        class_=asyncio.AsyncSession,
        autoflush=True,
        autocommit=False,
        expire_on_commit=True,
        info=None,
        **kw
    ):
        ...

    def begin(self) -> _SessionManager:
        ...
    async def __aenter__(self) -> asyncio.AsyncSession:
        ...
