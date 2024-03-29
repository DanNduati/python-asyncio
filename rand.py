import asyncio
import random
import time

#ANSI colors
c =(
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)

#main coroutine
async def makerandom(idx:int,threshold:int =6)-> int:
    print(c[idx + 1] + f"Initiated makerandom({idx}).")
    rn = random.randint(0,10)
    while rn < threshold:
        print(c[idx+1]+f"makerandom({idx})=={rn} too low; retrying")
        await asyncio.sleep(idx+1)
        rn = random.randint(0,10)
    print(c[idx+1]+f"Finished: makerandom({idx})=={rn}"+c[0])
    return rn

async def main():
    res = await asyncio.gather(*(makerandom(i,10-i)for i in range(3)))
    return res

if __name__ == "__main__":
    random.seed(time.time())
    r1,r2,r3 = asyncio.run(main())
    print()
    print(f"r1:{r1}, r2:{r2}, r3:{r3}")