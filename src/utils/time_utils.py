from datetime import datetime
import pytz


LONDON_TZ = pytz.timezone("Europe/London")


def get_london_time():
    """
    Always returns timezone-aware London time (DST-safe)
    """
    return datetime.now(LONDON_TZ)


def get_hour_index(offset_hours=2):
    """
    Safe hour calculation with wrap-around
    """
    now = get_london_time()
    return (now.hour + offset_hours) % 24


def format_hour_label(hour):
    return f"{hour:02d}:00 - {(hour + 1) % 24:02d}:00"

def should_run_now():
    """
    Centralized execution rule (45-minute logic)
    Prevents scheduler duplication bugs
    """
    now = get_london_time()
    return now.minute % 45 == 0