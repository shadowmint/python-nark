Helpful python utils.

### enum
    value = enum("X", "Y")
    x = value.X
    y = value.Y

### bitflags
    value = bitflags("X", "Y")
    compound = value.X | value.Y

### Logging
    log = Logging.get()
    log.info("Common logging format for all files")

### Factory
    factory = Factory()
    factory.load("blah.py")
    try:
      value = factory.prop("module_property")
    except Exception:
      e = exception()  # python2.x and python3.x supported

### Assets
    assets = Assets("basepath/static")
    if assets.exists("dir", "dir", "file"):
      path = assets.resolve("dir", "dir", "file")

### implements, resolve, Scope
    class IType(object):
      prop1 = None
      def call(self):
        pass

    @implements(IType)
    class ImplType(object):
      prop1 = "Value"
      def call(self):
        pass

    scope = Scope()
    scope.register(ImplType)

    @resolve(scope)
    class UsesType(object):
      def __init__(self, t=IType):
        self.t = t

    i = UsesType()
    i.t.call()

### Dynamic
    d = Dynamic()
    d.x.y.value = "Hello World"
    as_dict = dict(iter(d))
    d2 = Dynamic(as_dict)

### run
    run("ls", "-al")
