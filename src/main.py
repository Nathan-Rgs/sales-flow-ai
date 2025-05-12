from application.Application import ApplicationRAG
from uuid import uuid4
import asyncio

APP = ApplicationRAG()

if __name__ == "__main__":
    session = str(uuid4())
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        task = APP.run(input=input("Send me a message:"), session_id=session)
        tag = loop.run_until_complete(asyncio.gather(task))
