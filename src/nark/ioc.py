from __future__ import absolute_import
from implements import implements
import inspect
import sys

def ioc(scope):
  
  # index scope by type
  # notice we only do this once per class
  indexed_scope = {}
  for t in scope:
    for i in t.__identity:
      indexed_scope[i] = t
  print(indexed_scope)

  def inner(cls):
    old_init = cls.__init__
    spec = inspect.getargspec(old_init)
    print(spec)
    def __init__(self, *args, **kwargs):
      print("HELLLO")
      print(args)
      print(kwargs)
      kwargs_new = {}
      for key in kwargs.keys():
        # Add key
      # For items in defaults, move back through args
      # defaults(len-1) = args(len-1)
      # if key is not set:
        # if type of default is in scope_index
          # set value in kwargs
      for key in spec.args:

        print(key)
        arg = kwargs[key] 
        if arg in indexed_scope.keys():
          print("match %r" % arg)
          kwargs_new[key] = indexed_scope[arg]
        else:
          kwargs_new[key] = kwargs[key]
      print("hello")
      old_init(self, *args, **kwargs_new)
    cls.__init__ = __init__
    return cls
  return inner

class IT(object):
  def __init__(self):
    self.prop = None
  def func(self):
    pass

@implements(IT)
class T(object):
  def __init__(self):
    self.prop = 99
  def func(self):
    print("Hello World: %d" % self.prop)

# IOC scope
scope = [T]

@ioc(scope)
class HasDep(object):
  def __init__(self, value, thing=IT, other_thing=0, *args):
    self.value = value
    self.it = thing
  def run(self):
    self.it.func()


spec = inspect.getargspec(HasDep.__init__)
print(spec)
i = HasDep("kkk")
i.run()

