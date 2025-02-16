from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, TypeDecorator


class DateTimeWithTimeZone(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        return value.replace(tzinfo=ZoneInfo("UTC"))
