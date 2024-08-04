from contextlib import asynccontextmanager
from unittest.mock import MagicMock

from asynccontextstack import AsyncContextMixin


async def test_async_context_mixin_no_contexts():
    class MockAsyncContextClass(AsyncContextMixin):
        pass

    my_cm = MockAsyncContextClass()
    async with my_cm as ctx:
        assert my_cm is ctx
        assert ctx.async_entered_contexts == []


async def test_async_context_mixin_with_contexts():
    pre_mock = MagicMock()
    post_mock = MagicMock()
    mock_1 = MagicMock()

    @asynccontextmanager
    async def mock_manager():
        pre_mock()
        yield mock_1
        post_mock()

    class MockAsyncContextClass(AsyncContextMixin):
        @property
        def async_contexts(self):
            return [mock_manager()]

    my_cm = MockAsyncContextClass()
    async with my_cm as ctx:
        assert ctx is my_cm
        assert ctx.async_entered_contexts == [mock_1]

    pre_mock.assert_called_once()
    post_mock.assert_called_once()
