<center>
<h1><b>Web url collector</b></h1>
</center>

## Introduction
Learning assyncronous python project: Asynchronous http requests in python with aiohttp and asyncio
The high-level program structure will look like this:
1. Read a sequence of URLs from a local file, `urls.txt`.
2. Send GET requests for the URLs and decode the resulting content. If this fails, stop there for a URL.
3. Search for the URLs within href tags in the HTML of the responses.
4. Write the results to `foundurls.txt`.

Do all of the above as asynchronously and concurrently as possible. (Use aiohttp for the requests, and aiofiles for the file-appends. These are two primary examples of IO that are well-suited for the async IO model.)
