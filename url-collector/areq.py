import asyncio
import logging
import re
import sys
from typing import IO
import urllib.error
import urllib.parse

import aiofiles
import aiohttp
from aiohttp import ClientSession

'''
Goal: Asynchronously get links embedded in multiple othrer links
'''
logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
#disable automatic character encoding detections from requests
logging.getLogger("chardet.charsetprober").disabled = True
#regular expression to extract url from a html link
HREF_RE = re.compile(r'href="(.*?)"')

async def fetch_html(url:str,session:ClientSession,**kwargs) -> str:
    '''GET request wrapper to fetch page HTML.
    kwargs are passed to `session.request()`
    '''
    resp = await session.request(method="GET", url=url,**kwargs)
    resp.raise_for_status()
    logger.info(f"Got response {resp.status} for url {url}")
    html = await resp.text()
    return html

async def parse(url:str,session:ClientSession,**kwargs) -> set:
    '''Find HREFS in HTML of the `url`'''
    found = set()
    try:
        html = await fetch_html(url=url,session=session,**kwargs)
    except(
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(f"aiohttp exception for {url} [{getattr(e,'status',None)}] [{getattr(e,'message',None)}]")
        return found
    except Exception as e:
        logger.exception(f"Non-aiohttp exception occured: {getattr(e,'__dict__',{})}")
        return found
    else:
        for link in HREF_RE.findall(html):
            try:
                abslink = urllib.parse.urljoin(url,link)
            except(urllib.error.URLError, ValueError):
                logger.exception(f"Error parsing url {link}")
            else:
                found.add(abslink)
        logger.info(f"Found {len(found)} links for {url}")
        return found

async def write_one(file: IO, url:str, **kwargs) -> None:
    '''Write the found HREFs from `url` to file.'''
    res = await parse(url=url,**kwargs)
    if not res:
        return None
    async with aiofiles.open(file,"a") as f:
        for p in res:
            await f.write(f"{url}\t{p}\n")
        logger.info(f"Wrote results for source url: {url}")

async def bulk_crawl_and_write(file: IO,urls: set, **kwargs):
    '''Crawl & write concurrently to file for multiple urls'''
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(write_one(file=file,url=url,session=session,**kwargs)))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import pathlib
    import sys
    # ensure python version >= 3.7
    assert sys.version_info >= (3,7)
    here = pathlib.Path(__file__).parent

    with open(here.joinpath("urls.txt")) as infile:
        urls = set(map(str.strip,infile))
    
    outpath = here.joinpath("foundurls.txt")
    with open(outpath,"w") as outfile:
        outfile.write("source_url\tparsed_url\n")
    asyncio.run(bulk_crawl_and_write(file=outpath,urls=urls))