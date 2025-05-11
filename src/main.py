from application.Application import ApplicationRAG
import asyncio

APP = ApplicationRAG()

if __name__ == "__main__":
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        task = APP.run(input=input("Send me a message:"))
        tag = loop.run_until_complete(asyncio.gather(task))
