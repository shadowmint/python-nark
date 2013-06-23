from __future__ import absolute_import
from .exception import exception
import threading
import inspect
import sys


def resolve(scope):
  """ A decorator to perform IOC in python.
      
      You use it like this:

      # Create service that implements a given api
      @implements(DbType)
      class Blah():
        def xxx():
          pass

      # scope used for all singleton resolutions; register classes here.
      scope = [ Blah ]

      # Register a class as getting injected
      @resolve(scope)
      class MyThing():
        def __init__(self, value1, thing2, service=DbType):
          # On this line, service will be a Blah instance.
          pass

      Note that only kwargs are parsed for injectable classes, and that
      using @resolve means that you *cannot* pass a non-resolvable class 
      in as a kwarg, or an exception will be thrown.

      If you want to have singleton and instance behaviour, use the Scope
      class and pass that instead of an array:

      scope = Scope()
      scope.register(Blah)
      scope.register(OtherThing, instance=True)

      @resolve(scope)
      class MyThing():
        pass
  """

  # create scope if this isn't one
  if not isinstance(scope, Scope):
    tmp = scope
    scope = Scope()
    for t in tmp:
      scope.register(t)

  def inner(cls):
    old_init = cls.__init__
    spec = inspect.getargspec(old_init)
    def __init__(self, *args, **kwargs):
      kwargs_new = {}
      if spec.defaults is not None and len(spec.defaults) > 0:
        for i in reversed(range(len(spec.defaults))):
          offset = len(spec.defaults) - i - 1
          value = spec.defaults[i]
          key = spec.args[len(spec.args) - 1 - offset]
          if key not in kwargs.keys():
            if inspect.isclass(value):
              I = scope.resolve(value)
              kwargs_new[key] = I
      for key in kwargs.keys():
        if key not in kwargs_new.keys():
          kwargs_new[key] = kwargs[key]
      old_init(self, *args, **kwargs_new)
    cls.__init__ = __init__
    return cls
  return inner


class Scope(object):
  """ Handles scope binding in a more complex manner """

  def __init__(self):
    self.__bindings = {}

  def register(self, T, per_call=False, per_thread=False):
    """ Register a type.

        The type must be bound to some class interface, using:

        @implements(T)
        class Blah(object):
          pass

        The default behaviour is a single instance per scope
        which is returned for all injection requests.

        If 'per_call' is set to True, the behaviour is changed
        to return a new instance per injection request.

        If 'per_thread' is set to True, the behaviour is changed 
        to return a new instance per thread id. Thread ids are 
        notoriously finky; the logic used is:

        threading.current_thread().name

        and NOT:

        threading.current_thread().ident

        Which means that common threads can be used to share the
        same scope if required.
    """
    b = Binding(T, per_call, per_thread)
    for i in T.__dict__["__implements"]:
      self.__bindings[i] = b

  def resolve(self, T):
    """ Resolve the given type into an instance """
    if T not in self.__bindings.keys():
      raise ResolveFailedException(T)
    return self.__bindings[T].resolve()

  def clear(self):
    """ Clear all held instances, but not bindings """
    for i in self.__bindings.keys():
      self.__bindings[i].clear()

  def __repr__(self):
    display = {}
    for i in self.__bindings.keys():
      display[i.__name__] = "%r" % self.__bindings[i]
    return "<Scope([%r]) at 0x%x" % (display, id(self))  


class Binding(object):
  """ Binding of a single instance type """

  def __init__(self, T, per_call, per_thread):
    self.__type = T
    self.__per_call = per_call
    self.__per_thread = per_thread
    self.__instances = {}

  def clear(self):
    """ Clear held instances """
    self.__instances = {}

  def resolve(self):
    """ Resolve the given type into an instance """
    if self.__per_call:
      return self.instance()
    else:
      return self.singleton()

  def singleton(self):
    """ Return a singleton instance for the given type """
    key = "main"
    if self.__per_thread:
      key = threading.current_thread().name
    if key not in self.__instances.keys():
      self.__instances[key] = self.instance()
    return self.__instances[key]

  def instance(self):
    """ Return a new instance for the given type """
    try:
      rtn = self.__type()
    except Exception:
      e = exception()
      raise ResolveFailedException(self.__type, e)
    return rtn

  def __repr__(self):
    count = len(self.__instances.keys())
    return "<Binding(type=%s, per_call=%s, per_thread=%s, instances=%d)" % (self.__type.__name__, self.__per_call, self.__per_thread, count)


class ResolveFailedException(Exception):
  def __init__(self, T, e=None):
    if e is None:
      msg = "Failed to resolve type '%s': no binding registered in this scope." % T
    else:
      msg = "Failed to create type '%s' instance: %s." % (T, e)
    super(ResolveFailedException, self).__init__(msg)
    self.type = T
