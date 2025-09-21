import psutil
import platform
import os

def cpu():
    """Get CPU usage information"""
    usage = psutil.cpu_percent(interval=1)
    count = psutil.cpu_count()
    freq = psutil.cpu_freq()
    return f"CPU Usage: {usage}%\nCores: {count}\nFrequency: {freq.current:.0f}MHz"

def mem():
    """Get memory usage information"""
    mem = psutil.virtual_memory()
    return f"Memory: {mem.percent}% used\nUsed: {mem.used // (1024**3):.1f}GB\nTotal: {mem.total // (1024**3):.1f}GB\nAvailable: {mem.available // (1024**3):.1f}GB"

def ps():
    """List running processes"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            processes.append(f"{info['pid']}: {info['name']} (CPU: {info['cpu_percent']:.1f}%, MEM: {info['memory_percent']:.1f}%)")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return '\n'.join(processes[:20])  # Limit to first 20 processes

def disk():
    """Get disk usage information"""
    usage = psutil.disk_usage('/')
    return f"Disk: {usage.percent}% used\nUsed: {usage.used // (1024**3):.1f}GB\nTotal: {usage.total // (1024**3):.1f}GB\nFree: {usage.free // (1024**3):.1f}GB"

def network():
    """Get network information"""
    net = psutil.net_io_counters()
    return f"Network:\nSent: {net.bytes_sent // (1024**2):.1f}MB\nReceived: {net.bytes_recv // (1024**2):.1f}MB"

def system_info():
    """Get system information"""
    return f"OS: {platform.system()} {platform.release()}\nPython: {platform.python_version()}\nHostname: {platform.node()}"

def uptime():
    """Get system uptime"""
    boot_time = psutil.boot_time()
    import time
    uptime_seconds = time.time() - boot_time
    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    return f"Uptime: {days}d {hours}h {minutes}m"
