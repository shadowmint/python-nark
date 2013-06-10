from __future__ import absolute_import
from .implements import implements
from .exception import exception
from .enum import enum
import inspect


# Possible resolution methods for constructed objects
resolve = enum("INSTANCE", "SINGLETON")


class Resolver(object):
  """ Resolves properties on an object from class types into instances.

      Use this with @implements to perform dynamic binding:

      class IMyInterface():
        def func(self):
          pass

      @implements(IMyInterface) # <---- Check class and mark it.
      class MyImpl():
        def func(self): # <---- Matching named function required.
          pass

      class DependsOn():
        def __init__(self):
          self._service = IMyInterface # <---- Notice using interface type.

      Then resolve the type once one exists:

      r = Resolver()
      r.register(MyImpl)

      instance = DependsOn()
      r.resolve(instance)

      Notice that this means that the concrete interface implementation is
      generally not available for use in the constructor. That is simply a
      limitation of the resolver.

      The argument signature of the type is also not specifically checked;
      we assume that if a type quacks, it is a duck. The @implements decorator
      is simply there for type saftey and instance binding.
  """

  def __init__(self):
    self.bindings = {}

  def register(self, cls, resolution_type=resolve.SINGLETON):
    binding = Binding(cls, resolution_type)
    for k in binding.implements():
      self.bindings[k] = binding

  def resolve(self, instance):
    for T in instance.__dict__.keys():
      cls = instance.__dict__[T]
      if inspect.isclass(cls):
        if cls in self.bindings.keys():
          impl = self.bindings[cls].get()
          instance.__dict__[T] = impl
        else:
          raise ResolutionException("Unable to resolve type '%s': No binding" % (instance.__name__), instance)


class Binding(object):
  """ Looks after a class binding instance """

  def __init__(self, cls, resolution_type):
    self.cls = cls
    self.resolution_type = resolution_type
    self.__singleton = None

  def implements(self):
    """ Returns a list of type this implements """
    return self.cls.__dict__['__identity']

  def get(self):
    """ Return the appropraite type of instance """
    if self.resolution_type == resolve.INSTANCE:
      return self.instance()
    elif self.resolution_type == resolve.SINGLETON:
      return self.singleton()
    else:
      raise ResolutionException("Unable to resolve type '%s': Invalid resolution_type '%s'" % (self.cls.__name__), self.cls)

  def singleton(self):
    """ Returns a singleton instance for this type """
    if self.__singleton is None:
      self.__singleton = self.instance()
    return self.__singleton

  def instance(self):
    """ Creates an instance and returns it """
    try:
      rtn = self.cls()
    except Exception:
      e = exception()
      raise ResolutionException("Unable to resolve type '%s': %s" % (self.cls.__name__, e), self.cls)
    return rtn


class ResolutionException(Exception):
  def __init__(self, msg, T):
    super(self, ResolutionException).__init__()
    self.bad_type = T
