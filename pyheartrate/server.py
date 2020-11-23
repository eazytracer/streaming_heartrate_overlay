import asyncio
import websockets

async def setup_websocket_server(websocket, path):
        message_test = await websocket.recv()
        print(message_test)

start_server = websockets.serve(setup_websocket_server, "localhost", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
