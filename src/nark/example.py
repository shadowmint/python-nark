def hello():
  def inner(cls):
    old_init = cls.__init__
    def __init__(self, *args, **kwargs):
      print("hello")
      old_init(self, *args, **kwargs)
    cls.__init__ = __init__
    return cls
  return inner

@hello()
class TypeA(object):
  def __init__(self, *args, **kwargs):
    self.value = args[0]

a = TypeA(10)
print(a.value)

@hello()
class TypeB(object):
  def __init__(self, v1, v2, *args, **kwargs):
    self.value = v1 + v2

b = TypeB(10, 20)
print(b.value)

