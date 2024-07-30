import pendulum
from pendulum import duration
from datetime import datetime
from datetime import timedelta
from typing import Union

import strawberry


class DateTime:
    """
    This class is used to convert the pendulum.DateTime type to a string
    and back to a pendulum.DateTime type
    """

    @staticmethod
    def serialize(dt: Union[pendulum.DateTime, datetime]) -> str:  # type: ignore
        try:
            return dt.isoformat()
        except ValueError:
            return dt.to_iso8601_string()  # type: ignore

    @staticmethod
    def parse_value(value: str) -> Union[pendulum.DateTime, datetime]:  # type: ignore
        return pendulum.parse(value)  # type: ignore


DateTime = strawberry.scalar(
    Union[pendulum.DateTime, datetime],  # type: ignore
    name="datetime",
    description="A date and time",
    serialize=DateTime.serialize,
    parse_value=DateTime.parse_value,
)


class Duration:
    @staticmethod
    def serialize(value: timedelta) -> int:
        return int(value.total_seconds())

    @staticmethod
    def parse_value(value: int) -> timedelta:
        return timedelta(seconds=value)


Duration = strawberry.scalar(
    timedelta,
    name="Duration",
    description="A time duration in seconds",
    serialize=Duration.serialize,
    parse_value=Duration.parse_value,
)
