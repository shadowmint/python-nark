import sqlalchemy
from nark import DateTime, Timestamp


class UTCDateTime(sqlalchemy.types.TypeDecorator):
    """Store this DateTime object as a UTC timestamp """
    impl = sqlalchemy.types.Integer

    def process_bind_param(self, value, dialect):
        return DateTime.as_timestamp(value)

    def process_result_value(self, value, dialect):
        return Timestamp.as_datetime(value)


class UTCTime(sqlalchemy.types.TypeDecorator):
    """Store this Time object as a UTC timestamp """
    impl = sqlalchemy.types.Integer

    def process_bind_param(self, value, dialect):
        return DateTime.as_timestamp(value)

    def process_result_value(self, value, dialect):
        return Timestamp.as_datetime(value)