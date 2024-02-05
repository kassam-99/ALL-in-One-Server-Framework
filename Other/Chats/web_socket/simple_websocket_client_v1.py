import asyncio
import websockets




async def chat_client():
    user_port = int(input("Enter a port: "))
    uri = f"ws://localhost:{user_port}"
    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Enter message: ")
            if message:
                await websocket.send(message)
            
            response = await websocket.recv()
            if response:
                print(f"\nReceived: {response}\n")


asyncio.run(chat_client())
