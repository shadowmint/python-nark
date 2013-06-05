class Log(object):
  def trace(self, msg, *kargs):
    print(msg % kargs)
