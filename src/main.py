from application.Application import ApplicationRAG
from log.setup import setup_logging
from uuid import uuid4
import asyncio

APP = ApplicationRAG()
setup_logging()

if __name__ == "__main__":
    session = str(uuid4())
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        task = APP.run(input=input("Send me a message:"), session_id=session)
        response = loop.run_until_complete(asyncio.gather(task))
        print(response)
