# Python asyncio
Writting 'concurrent' code in python

## Rules
The syntax async def introduces either a `native coroutine` or an `asynchronous generator`. The expressions async with and async for are also valid, and you’ll see them later on.
* A function that you introduce with async def is a coroutine. It may use await, return, or yield, but all of these are optional. Declaring async def noop(): pass is valid:
	* Using await and/or return creates a coroutine function. To call a coroutine function, you must await it to get its results.
	* It is less common (and only recently legal in Python) to use yield in an async def block. This creates an `asynchronous generator`, which you iterate over with async for.
	* Anything defined with async def may not use `yield from`, which will raise a `SyntaxError`.
* Just like it’s a SyntaxError to use yield outside of a def function, it is a SyntaxError to use await outside of an async def coroutine. You can only use await in the body of coroutines.

### `generator-based` and `native` coroutines
```python
import asyncio

@asyncio.coroutine
def py34_coro():
    """Generator-based coroutine, older syntax"""
    yield from stuff()

async def py35_coro():
    """Native coroutine, modern syntax"""
    await stuff()
```