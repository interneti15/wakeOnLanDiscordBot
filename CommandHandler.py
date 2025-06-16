import os
import platform
import asyncio
import psutil
import time
import subprocess

from Config import *
from WakeOnLan import *

async def commandHandler(command: str, config:Config) -> str:
    command = command.strip().lower()
    if command == "":
        return "Unknown command. Use -h to see available commands."

    if command == "status":
        return await system_status()

    elif command == "wol":
        return await wake_system(config)

    elif command == "disk":
        return await disk_status()

    elif command == "shutdown":
        system_platform = platform.system().lower()
        if system_platform == 'windows':
            os.system('shutdown /s /t 1')  # Windows shutdown command
        elif system_platform == 'linux' or system_platform == 'darwin':
            os.system('shutdown now')  # Linux/Mac shutdown command
        return "System is shutting down..."

    elif command == "-h":
        return await help()

    elif command == "myip":
        return await get_public_ip()

    else:
        return "Unknown command. Use -h to see available commands."


async def help():
    return ("Available commands:\n"
            "status - Show system status (CPU, memory, and temperature)\n"
            "wol - Send a Wake-on-LAN magic packet\n"
            "disk - Show disk usage details\n"
            "shutdown - Shutdown the system\n"
            "myip - show current public ipv4\n"
            "upnp-refresh - restart vital upnp tunels (disabled) \n"
            "-h - Show this help message")

async def get_public_ip():
    # Run the curl command asynchronously and capture the output
    process = await asyncio.create_subprocess_shell(
        'curl ifconfig.me',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    
    # Decode and return the stdout as a string
    return stdout.decode().strip()


async def disk_status():
    disk = psutil.disk_usage('/')
    total = disk.total / (1024 ** 3)
    used = disk.used / (1024 ** 3)
    free = disk.free / (1024 ** 3)
    return (f"Disk Status:\n"
            f"Total: {total:.2f} GB\n"
            f"Used: {used:.2f} GB\n"
            f"Free: {free:.2f} GB")


async def wake_system(config):
    await sendMagickPackage(config)
    return "Magic Package sent!"


async def system_status():
    cpu_info = platform.processor()
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    total_memory = memory.total / (1024 ** 3)
    available_memory = memory.available / (1024 ** 3)
    # Fetching CPU temperature (if available)
    cpu_temp = "N/A"
    try:
        temp_info = psutil.sensors_temperatures()
        if "coretemp" in temp_info:  # On some systems (e.g., Linux), the temperature is under "coretemp"
            cpu_temp = temp_info["coretemp"][0].current if temp_info["coretemp"] else "N/A"
    except AttributeError:
        cpu_temp = "N/A"  # If sensors_temperatures is not available, set temp to "N/A"
    # Calculate uptime (CPU runtime)
    boot_time = psutil.boot_time()
    current_time = time.time()
    uptime_seconds = current_time - boot_time
    # Calculate days, hours, minutes, and seconds
    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    # Format uptime with days, hours, minutes, seconds
    uptime = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
    return (f"System Status:\n"
            f"CPU: {cpu_info} (Usage: {cpu_percent:.2f}%)\n"
            f"CPU Temperature: {cpu_temp}°C\n"
            f"Memory: Total: {total_memory:.2f} GB, Available: {available_memory:.2f} GB\n"
            f"CPU Runtime (Uptime): {uptime}")


async def main():
    string = await commandHandler("myip", None)
    print(string)

if __name__ == "__main__":
    pass
    #asyncio.run(main())
