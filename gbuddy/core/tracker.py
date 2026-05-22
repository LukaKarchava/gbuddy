"""Network usage while laptop is on phone hotspot."""

import psutil


def format_amount(byte_count):
    """Readable amount with unit, e.g. '6.7 MB' or '3.0 GB'."""
    mb = byte_count / (1024 * 1024)
    if mb >= 1024:
        return f"{mb / 1024:.2f} GB"
    if mb >= 100:
        return f"{int(mb)} MB"
    return f"{mb:.1f} MB"


class UsageTracker:
    def __init__(self):
        net = psutil.net_io_counters()
        self._last_total = net.bytes_sent + net.bytes_recv

    def sample(self):
        net = psutil.net_io_counters()
        total = net.bytes_sent + net.bytes_recv
        delta = max(0, total - self._last_total)
        self._last_total = total
        return net, delta

    @staticmethod
    def session_split(net, sent_start, recv_start):
        up = max(0, net.bytes_sent - sent_start)
        down = max(0, net.bytes_recv - recv_start)
        return up + down, up, down
