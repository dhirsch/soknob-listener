import asyncio
import time

from loguru import logger
from soknob import sonos
from soknob import config

class SoknobProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        logger.debug("Received data {}", data)
        msg = data.decode().rstrip() # remove any trailing newlines
        if msg == "up":
            change_volume(config.volume_up_delta)
        elif msg == "down":
            change_volume(config.volume_down_delta)
        elif msg == "techo":
            pass


def run():
    loop = asyncio.get_event_loop()
    logger.info("Starting UDP server")
    listen = loop.create_datagram_endpoint(SoknobProtocol, local_addr=('0.0.0.0', config.udp_port))
    transport, _ = loop.run_until_complete(listen)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Keyboard interruptus")

    transport.close()
    loop.close()
    logger.info("Closed out")

def change_volume(delta: int):
    start_time = time.perf_counter_ns()
    logger.debug("Changing volume by {}", delta)
    group = sonos.find_primary_group()
    if not group:
        logger.error("Could not find primary group")
        return
    resp = sonos.group_volume_delta(group, delta)
    if resp.status_code != 200:
        logger.warning("Error setting volume")
    logger.debug("Time spent: {}ms", (time.perf_counter_ns() - start_time) / 1000000)

