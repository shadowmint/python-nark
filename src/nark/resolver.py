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

      You can recursively resolve objects in this manner; resolve() is
      invoked on new instances:

      @implements(IOther)
      class Other(object):
        def thing(self):
          return 0

      @implements(IBlah)
      class Blah(object):
        def __init__(self):
          self.value = IOther

      class HasDeps(object):
        def __init__(self):
          self.blah = IBlah

      i = HasDeps()
      r.resolve(i)
      print(r.blah.value.thing())

      NB. That you can get cyclical dependencies using resolve.INSTANCE
      if you're not careful.
  """

  def __init__(self):
    self.bindings = {}

  def register(self, cls, resolution_type=resolve.SINGLETON):
    """ Register a specific class binding.
        Notice that calling this will replace an existing binding of the same type.
    """
    binding = Binding(cls, resolution_type, self)
    for k in binding.implements():
      self.bindings[k] = binding

  def resolve_children(self, instance):
    """ Resolve the children of this object.

        This is for when an object has various child objects
        that need to be resolved, and saves calling resolve
        on each of them manually.

        A class might do this:

          def __init__(self):
            self.blah = Blah()
            self.blahblah = Blah2()
            self.thing = IThing
            self.other = IOther
            resolve_children(self)  # <-- Blah and Blah2 are now resolved, but wait for parent to resolve interfaces
    """
    for key in instance.__dict__.keys():
      invalid = key[:1] == "_" or key[-1:] == "_"
      if not invalid:
        item = instance.__dict__[key]
        if not inspect.isclass(item):
          self.resolve(item)

  def resolve(self, instance):
    """ Resolve any public types that are attached to the given class """
    try:
      data = instance.__dict__
    except AttributeError:
      data = {}  # Probably wasn't an object
    for T in data.keys():
      cls = data[T]
      if inspect.isclass(cls):
        if cls in self.bindings.keys():
          impl = self.bindings[cls].get()
          data[T] = impl
        else:
          raise ResolutionException("Unable to resolve type '%s': No binding" % (instance.__name__), instance)


class Binding(object):
  """ Looks after a class binding instance """

  def __init__(self, cls, resolution_type, parent):
    self.cls = cls
    self.resolution_type = resolution_type
    self.parent = parent
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
      self.parent.resolve(rtn)
    except Exception:
      e = exception()
      raise ResolutionException("Unable to resolve type '%s': %s" % (self.cls.__name__, e), self.cls)
    return rtn


class ResolutionException(Exception):
  def __init__(self, msg, T):
    super(ResolutionException, self).__init__(msg)
    self.bad_type = T
