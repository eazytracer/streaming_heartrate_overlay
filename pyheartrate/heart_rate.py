import asyncio
from bleak import discover
from bleak import BleakClient
HR_UUID = "0000180d-0000-1000-8000-00805f9b34fb"

def callback(sender: int, data: bytearray):
    print(data, str(data))
    print(f"Heart Rate: {int(data[1])}")


async def run(address):
    devices = await discover()
    print("devices")
    for d in devices:
        print(d)
    if not devices:
        print("no devices found")
    # async with BleakClient(address) as client:
    #     hr_service = None
    #     x = await client.is_connected()
    #     services = await client.get_services()
    #     for service in services:
    #         print(service)
    #         if "Heart Rate" in service.description:
    #             characteristics = service.characteristics
    #             for characteristic in characteristics:
    #                 if "Heart Rate Measurement" in characteristic.description:
    #                     hr_service = characteristic
    #                 break
    #     await client.start_notify(hr_service, callback)
    #     await asyncio.sleep(30)
# address = "40:4E:36:BE:1B:72"
SCOSCHE_MAC = "C9:EA:DD:2D:5C:86"

loop = asyncio.get_event_loop()
loop.run_until_complete(run(SCOSCHE_MAC))
#loop = asyncio.get_event_loop()
#loop.run_until_complete(run())