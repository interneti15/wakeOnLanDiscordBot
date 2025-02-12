from wakeonlan import send_magic_packet
from Config import *
import os


async def sendMagickPackage(config:Config):
    """Function to send the WOL magic packet to the specified MAC address."""
    print("Received message from specified user, sending Wake-on-LAN magic packet.")
    send_magic_packet(config.MAC_ADDRESS)
