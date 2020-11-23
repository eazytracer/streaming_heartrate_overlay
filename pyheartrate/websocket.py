import asyncio
import functools
import json
import websockets
import signal

from bleak import discover
from bleak import BleakClient

SCOSCHE_MAC = "C9:EA:DD:2D:5C:86"
# SCOSCHE_MAC = "CD:D9:DD:DB:2B:71"
QUEUE = asyncio.Queue()

# TODO pass in QUEUE
async def websocket_sender(websocket, path):
    print("started websocket")
    while True:
        msg = await QUEUE.get()
        print("Found message", msg)
        await websocket.send(json.dumps(msg))
        QUEUE.task_done()

class HeartRateMonitor(object):
    def __init__(self, mac_address, queue):
        self.mac_address = mac_address
        self.queue = queue
        
    def _callback(self, sender: int, data: bytearray):
        try:
            rate = int(data[1])
            print(f"Heart Rate: {rate}")
            response = {'message': {'heart_rate': rate}}
            self.queue.put_nowait(response)
        except:
            print("It broke")

    async def heart_rate(self, event):
        print("Starting Heart Rate Monitor")
        async with BleakClient(self.mac_address) as client:
        # try:
            hr_service = None
            x = await client.is_connected()
            print("Connected to device")
            services = await client.get_services()
            for service in services:
                if "Heart Rate" in service.description:
                    characteristics = service.characteristics
                    for characteristic in characteristics:
                        if "Heart Rate Measurement" in characteristic.description:
                            hr_service = characteristic
                            print("found characteristic: ", hr_service)
                        break
            started = await client.start_notify(hr_service, self._callback)
            print("started: {}".format(started))
            await event.wait()
            print("got event")
        # finally:
            await client.stop_notify(hr_service)
            print("stopped heart rate monitor")

async def main(queue, event):
    print("Creating Server")
    monitor = HeartRateMonitor(SCOSCHE_MAC, queue)
    await monitor.heart_rate(event)

def ask_exit(signame, loop, event):
    print("got signal %s: exit" % signame)
    loop.stop()

def start():
    shutdown_event = asyncio.Event()
    loop = asyncio.get_event_loop()
    start_server = websockets.serve(websocket_sender, "localhost", 5000)
    loop.run_until_complete(start_server)
    loop.create_task(main(QUEUE, shutdown_event))
    loop.run_forever()


if __name__ == "__main__":
    asyncio.run(start())
    loop = asyncio.get_running_loop()
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
        functools.partial(ask_exit, signame, loop))

