import inspect
import sys


class ImplementsException(Exception):
  def __init__(self, msg, signature):
    super(ImplementsException, self).__init__()
    self.signature = signature


def implements(*T):
  def inner(cls):
    cls.__identity = []
    for t in T:
      t_methods = inspect.getmembers(t, predicate=lambda x: inspect.isfunction(x) or inspect.ismethod(x))
      c_methods = inspect.getmembers(cls, predicate=lambda x: inspect.isfunction(x) or inspect.ismethod(x))
      sig = {}
      for i in t_methods:
        name = i[0]
        if name[:2] != "__":
          sig[name] = False
      for i in c_methods:
        name = i[0]
        if name in sig.keys():
          sig[name] = True
      missing = False
      for i in sig.keys():
        if not sig[i]:
          missing = True
      if missing:
        raise ImplementsException("Invalid @implements decorator on '%s': %r" % (t.__name__, sig), sig)
      cls.__identity.append(t)
    return cls
  return inner
