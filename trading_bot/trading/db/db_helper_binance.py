import typing
from contextlib import contextmanager

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from trading.core.settings import settings


class DBHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        max_overflow: int = 10,
        pool_size: int = 10,
    ):
        self.engine: Engine = create_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )

        self.Session: sessionmaker[Session] = sessionmaker(
            bind=self.engine,
            autocommit=False,
            # autoflush=False,
            # expire_on_commit=False,
        )

    @contextmanager
    def session(self, **kwargs) -> typing.ContextManager[Session]:
        """Provide a transactional scope around a series of operations."""
        new_session = self.Session(**kwargs)
        try:
            yield new_session
            new_session.commit()
        except Exception:
            new_session.rollback()
            raise
        finally:
            new_session.close()

    # async def dispose(self) -> None:
    #     await self.engine.dispose()


db_helper_binance = DBHelper(
    url=str(settings.db_binance.url),
    echo=settings.db_binance.echo,
    echo_pool=settings.db_binance.echo_pool,
    max_overflow=settings.db_binance.max_overflow,
    pool_size=settings.db_binance.pool_size,
)
