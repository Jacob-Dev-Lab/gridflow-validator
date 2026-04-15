from datetime import datetime
import pytz


LONDON_TZ = pytz.timezone("Europe/London")


def get_london_time():
    return datetime.now(LONDON_TZ)


def get_hour_index(offset_hours: int = 2) -> int:
    """
    Your system logic uses T+1h or T+2h offset depending on business rule
    """
    now = get_london_time()
    return (now.hour + offset_hours) % 24


def format_hour_label(hour: int) -> str:
    start = hour
    end = (hour + 1) % 24
    return f"{start:02d}:00 - {end:02d}:00"