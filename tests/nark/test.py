from inspect import *

class X(object):
  def y(self):
    pass

methods = getmembers(X, predicate=ismethod)
functions = getmembers(X, predicate=isfunction)

print("%r" % methods)
print("%r" % functions)
