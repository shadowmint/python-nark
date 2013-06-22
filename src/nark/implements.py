import inspect
import sys


class ImplementsException(Exception):
  def __init__(self, msg, signature):
    super(ImplementsException, self).__init__()
    self.signature = signature


def implements(*T):
  def inner(cls):
    cls.__implements = []
    for t in T:

      # Look for required methods
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

      # Look for required properties
      t_props = [i for i in inspect.getmembers(t) if i not in t_methods]
      c_props = [i for i in inspect.getmembers(cls) if i not in c_methods]
      for i in t_props:
        name = i[0]
        if name[:2] != "__":
          sig[name] = False
      for i in c_props:
        name = i[0]
        if name in sig.keys():
          sig[name] = True
      missing = False

      for i in sig.keys():
        if not sig[i]:
          missing = True
      if missing:
        raise ImplementsException("Invalid @implements decorator on '%s': %r" % (t.__name__, sig), sig)
      cls.__implements.append(t)
    return cls
  return inner
