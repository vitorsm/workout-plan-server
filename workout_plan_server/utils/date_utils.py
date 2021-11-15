import re
from datetime import datetime, timedelta
from typing import Optional


def check_if_str_date_has_time(date_str: str) -> bool:
    if not date_str:
        return False

    result = re.findall("([0-1]?[0-9]|2[0-3]):[0-5][0-9]", date_str)

    return len(result) > 0


def from_str_to_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None

    microseconds = None
    if '.' in date_str:
        microseconds_str = date_str.split('.')[1]
        if microseconds_str and not microseconds_str[-1].isnumeric():
            microseconds_str = microseconds_str[:-1]

        microseconds = int(microseconds_str)
        date_str = date_str.split('.')[0]

    date_format = "%Y-%m-%d"
    if check_if_str_date_has_time(date_str):
        date_format = "%Y-%m-%dT%H:%M:%S"

    dt = datetime.strptime(date_str, date_format)

    return dt + timedelta(microseconds=microseconds) if microseconds else dt

