from datetime import datetime, timedelta

import pendulum
import strawberry


class DateTime:
    """
    This class is used to convert the pendulum.DateTime type to a string
    and back to a pendulum.DateTime type
    """

    @staticmethod
    def serialize(dt: pendulum.DateTime | datetime) -> str:
        try:
            return dt.isoformat()
        except ValueError:
            return dt.to_iso8601_string()

    @staticmethod
    def parse_value(value: str) -> pendulum.DateTime | datetime:
        return pendulum.parse(value)


DateTime = strawberry.scalar(
    pendulum.DateTime | datetime,
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
