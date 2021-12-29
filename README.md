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

## Async IO Design Patterns
### Chaining coroutines
Coroutines can be chained together. (Remember, a coroutine object is awaitable, so another coroutine can await it.) This allows you to break programs into smaller, manageable, recyclable coroutines:


## The Event loop and `asyncio.run`
You can think of an event loop as something like a while True loop that monitors coroutines, taking feedback on what’s idle, and looking around for things that can be executed in the meantime. It is able to wake up an idle coroutine when whatever that coroutine is waiting on becomes available.
Thus far, the entire management of the event loop has been implicitly handled by one function call:
```python
asyncio.run(main())  # Python 3.7+
```
`asyncio.run()` is responsible for getting the event loop running tasks until they are marked as complete and closing the event loop.
coroutines don't do much on their own until they are tied to the event loop:

```python
>>> import asyncio

>>> async def main():
...     print("Hello ...")
...     await asyncio.sleep(1)
...     print("World!")

>>> routine = main()
>>> routine
<coroutine object main at 0x1027a6150>
```
Remember to use asyncio.run() to actually force execution by scheduling the main() coroutine (future object) for execution on the event loop:
```python
>>> asyncio.run(routine)
Hello ...
World!
```