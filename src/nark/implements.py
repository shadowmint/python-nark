import inspect

class ImplementsException(Exception):
  pass

def implements(*T):
  def inner(cls):
    cls.__identity = []
    for t in T:
      t_methods = inspect.getmembers(t, predicate=inspect.ismethod)
      c_methods = inspect.getmembers(cls, predicate=inspect.ismethod)
      sig = {}
      for i in t_methods:
        name = i[0]
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
        raise ImplementsException("Invalid @implements decorator on '%s': %r" % (t.__name__, sig))
      cls.__identity.append(t)
    return cls
  return inner

class IType(object):
  def xxx(self):
    pass
  def yyy(self):
    pass
  def zzz(self):
    pass

@implements(IType)
class ImplBad(object):
  def xxx(self):
    pass
  def yyy(self):
    pass
  def zzz(self):
    pass

@implements(IType)
class ImplOk(object):
  def xxx(self):
    pass
  def yyy(self):
    pass
  def zzz(self):
    pass
  
