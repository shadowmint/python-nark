import pytz
import datetime as pytm


class DateTime(object):
  """DateTime methods """

  @staticmethod
  def now():
    """Return now as a UTC time """
    return pytz.UTC.localize(pytm.datetime.now())

  @staticmethod
  def as_timestamp(dt):
    """Convert a datetime into a timestamp """
    epoch = pytm.datetime.utcfromtimestamp(0)
    epoch = epoch.replace(tzinfo=pytz.UTC)
    return (dt - epoch).total_seconds()


class Timestamp(object):
  """Timestamp functions """

  @staticmethod
  def as_datetime(timestamp):
    """Convert a timestamp into a datetime """
    try:
      timestamp = float(timestamp)
    except Exception:
      timestamp = 0
    value = pytz.utc.localize(pytm.datetime.utcfromtimestamp(timestamp))
    return value.astimezone(pytz.UTC)