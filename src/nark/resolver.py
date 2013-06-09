from __future__ import absolute_import
from .implements import implements

class Resolver(object):

  def __init__(self):
    self.bindings = {}

  def register(self, cls):
    print("%r" % (cls.__dict__))
    keys = cls.__dict__["__identity"]
    for k in keys:
      self.bindings[k] = cls

  def resolve(self, instance):
    for T in instance.__dict__.keys():
      cls = instance.__dict__[T]
      if cls in self.bindings.keys():
        impl = self.bindings[cls]
        try:
          real_instance = impl()
        except Exception:
          # TODO: Raise an create-instance-exception
          pass
        instance.__dict__[T] = real_instance
          

class IPrinter(object):
  def prints(self, msg):
    pass

class IValuer(object):
  def value(self, a, b):
    pass

@implements(IPrinter)
class Printer(object):
  def prints(self, msg):
    print(msg)

@implements(IValuer)
class Valuer(object):
  def value(self, a, b):
    return a + b

@implements(IValuer, IPrinter)
class Crazy(object):
  def value(self, a, b):
    return a + b
  def prints(self, msg):
    print(msg)

class HasDeps(object):
  def __init__(self):
    self.valuer = IValuer
    self.printer = IPrinter

c = Resolver()
c.register(Printer)
c.register(Valuer)

instance = HasDeps()
c.resolve(instance)
instance.printer.prints(instance.valuer.value(10, 10))

c = Resolver()
c.register(Crazy)

instance = HasDeps()
c.resolve(instance)
instance.printer.prints(instance.valuer.value(10, 10))
