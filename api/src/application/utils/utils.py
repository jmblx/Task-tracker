from datetime import datetime
from typing import Any

from pytz import timezone


def get_cur_date() -> dict[str, Any]:
    tz = timezone("Europe/Moscow")
    now = datetime.now(tz)
    return {
        "current_day": now.day,
        "current_month": now.month,
        "current_year": now.year,
    }
