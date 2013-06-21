# Copyright 2013 Douglas Linder
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import unittest
import bootstrap
from nark import *

class ResolverTests(unittest.TestCase):

  def test_can_resolve_decroated_class(self):

    class IPrinter(object):
      def prints(self, msg):
        pass

    class IValuer(object):
      def value(self, a, b):
        pass

    @implements(IPrinter)
    class Printer(object):
      def prints(self, msg):
        return "prints-" + str(msg)

    @implements(IValuer)
    class Valuer(object):
      def value(self, a, b):
        return a + b

    c = Scope()
    c.register(Printer)
    c.register(Valuer)

    @resolve(c)
    class HasDeps(object):
      def __init__(self, valuer=IValuer, printer=IPrinter):
        self.valuer = valuer
        self.printer = printer

    a = Assert()

    instance = HasDeps()

    output1 = instance.printer.prints("hello")
    output2 = instance.valuer.value(10, 10)

    a.equals(output1, "prints-hello", "Failed to resolve printer")
    a.equals(output2, 20, "Failed to resolve valuer")

  def test_can_resolve_decroated_class_from_array(self):

    class IPrinter(object):
      def prints(self, msg):
        pass

    class IValuer(object):
      def value(self, a, b):
        pass

    @implements(IPrinter)
    class Printer(object):
      def prints(self, msg):
        return "prints-" + str(msg)

    @implements(IValuer)
    class Valuer(object):
      def value(self, a, b):
        return a + b

    c = [ Printer, Valuer ]

    @resolve(c)
    class HasDeps(object):
      def __init__(self, valuer=IValuer, printer=IPrinter):
        self.valuer = valuer
        self.printer = printer

    a = Assert()

    instance = HasDeps()

    output1 = instance.printer.prints("hello")
    output2 = instance.valuer.value(10, 10)

    a.equals(output1, "prints-hello", "Failed to resolve printer")
    a.equals(output2, 20, "Failed to resolve valuer")

  def test_can_resolve_decroated_compound_class(self):

    class IPrinter(object):
      def prints(self, msg):
        pass

    class IValuer(object):
      def value(self, a, b):
        pass

    @implements(IValuer, IPrinter)
    class Crazy(object):
      def value(self, a, b):
        return a - b
      def prints(self, msg):
        return "hello-" + str(msg)

    c = [ Crazy ]

    @resolve(c)
    class HasDeps(object):
      def __init__(self, valuer=IValuer, printer=IPrinter):
        self.valuer = valuer
        self.printer = printer

    a = Assert()

    instance = HasDeps()

    output1 = instance.printer.prints("hello")
    output2 = instance.valuer.value(10, 10)

    a.equals(output1, "hello-hello", "Failed to resolve printer")
    a.equals(output2, 0, "Failed to resolve valuer")


  def test_can_resolve_instance(self):

    class IDb(object):
      def data(self):
        pass

    @implements(IDb)
    class Db(object):
      def __init__(self):
        self._data = {}
      def data(self):
        return self._data

    scope = Scope()
    scope.register(Db, per_call=True)

    @resolve(scope)
    class UsesDb(object):
      def __init__(self, db=IDb):
        self.db = db

    a = Assert()

    i1 = UsesDb()
    i2 = UsesDb()

    i1.db.data()["key"] = "value1"
    i2.db.data()["key"] = "value2"

    a.equals(i1.db.data()["key"], "value1", "Object was unexpectedly singleton")
    a.equals(i2.db.data()["key"], "value2", "Object was unexpectedly singleton")

  def test_cant_accidentally_resolve_instance(self):

    class IDb(object):
      def data(self):
        pass

    @implements(IDb)
    class Db(object):
      def __init__(self):
        self._data = {}
      def data(self):
        return self._data

    scope = [Db]

    @resolve(scope)
    class UsesDb(object):
      def __init__(self, db=IDb):
        self.db = db

    a = Assert()

    i1 = UsesDb()
    i2 = UsesDb()

    i1.db.data()["key"] = "value"
    a.equals(i2.db.data()["key"], "value", "Object was not a singleton")

    i2.db.data()["key"] = "value2"
    a.equals(i1.db.data()["key"], "value2", "Object was not a singleton")

  def test_can_resolve_deep_query(self):

    class IDb(object):
      def data(self):
        pass

    @implements(IDb)
    class Db(object):
      def data(self):
        return 10

    scope = [Db]

    @resolve(scope)
    class UsesDb(object):
      def __init__(self, db=IDb):
        self.db = db

    class HasDep(object):
      def __init__(self):
        self.service = UsesDb()

    a = Assert()

    i = HasDep()

    value = i.service.db.data()
    a.equals(value, 10, "Failed to resolve something with a resolvable child")

  def text_complex_init_flags_dont_screw_things_up(self):

    class IPrinter(object):
      def prints(self, msg):
        pass

    class IValuer(object):
      def value(self, a, b):
        pass

    @implements(IPrinter)
    class Printer(object):
      def prints(self, msg):
        return "prints-" + str(msg)

    @implements(IValuer)
    class Valuer(object):
      def value(self, a, b):
        return a + b

    c = Scope()
    c.register(Printer)
    c.register(Valuer)

    @resolve(c)
    class HasDeps(object):
      def __init__(self, x, y, valuer=IValuer, printer=IPrinter, *kargs, **kwargs):
        self.valuer = valuer
        self.printer = printer
        self.x = x
        self.y = y 
        self.other = kargs[0]
        self.left = kwargs["left"]

    a = Assert()

    instance = HasDeps(5, 10, 15, left="right")

    output1 = instance.printer.prints("hello")
    output2 = instance.valuer.value(10, 10)

    a.equals(output1, "prints-hello", "Failed to resolve printer")
    a.equals(output2, 20, "Failed to resolve valuer")
    a.equals(instance.x, 5, "Invalid x value")
    a.equals(instance.y, 10, "Invalid y value")
    a.equals(instance.other, 15, "Invalid kargs value")
    a.equals(instance.left, "right", "Invalid kwargs value")

  def test_passing_mock_as_argument_works(self):
    
    class IPrinter(object):
      def prints(self, msg):
        pass

    class IValuer(object):
      def value(self, a, b):
        pass

    @implements(IPrinter)
    class Printer(object):
      def prints(self, msg):
        return "prints-" + str(msg)

    @implements(IValuer)
    class Valuer(object):
      def value(self, a, b):
        return a + b

    c = Scope()
    c.register(Printer)
    c.register(Valuer)

    class MockPrinter(object):
      def prints(self, msg):
        return "blah"

    @resolve(c)
    class HasDeps(object):
      def __init__(self, x, y, valuer=IValuer, printer=IPrinter, **kwargs):
        self.valuer = valuer
        self.printer = printer
        self.x = x
        self.y = y 
<<<<<<< HEAD
        self.other = kwargs["other"]

    a = Assert()

    instance = HasDeps(5, 10, other=15)
=======
        self.left = kwargs["left"]

    a = Assert()

    instance = HasDeps(5, 10, left="right", printer=MockPrinter())
>>>>>>> aa0c54b... updated logging

    output1 = instance.printer.prints("hello")
    output2 = instance.valuer.value(10, 10)

    a.equals(output1, "prints-hello", "Failed to use mock printer")
    a.equals(output2, 20, "Failed to resolve valuer")
    a.equals(instance.x, 5, "Invalid x value")
    a.equals(instance.y, 10, "Invalid y value")
<<<<<<< HEAD
    a.equals(instance.other, 15, "Invalid kargs value")

  def test_inject_with_no_binding_fails(self):
    
    class IPrinter(object):
      def prints(self, msg):
        pass

    @implements(IPrinter)
    class Printer(object):
      def prints(self, msg):
        return "prints-" + str(msg)

    c = Scope()

    @resolve(c)
    class HasDeps(object):
      def __init__(self, printer=IPrinter):
        self.printer = printer

    a = Assert()

    failed = False
    try: 
      instance = HasDeps(5, 10, other=15)
    except ResolveFailedException:
      failed = True

    a.true(failed, "Resolved a missing type")

  def test_inject_with_stupid_type_fails(self):
    
    class IPrinter(object):
      def prints(self, msg):
        pass

    @implements(IPrinter)
    class Printer(object):
      def __init__(self, stupid):
        pass
      def prints(self, msg):
        return "prints-" + str(msg)

    c = Scope()
    c.register(Printer)

    @resolve(c)
    class HasDeps(object):
      def __init__(self, printer=IPrinter):
        self.printer = printer

    a = Assert()

    failed = False
    try: 
      instance = HasDeps(5, 10, other=15)
    except ResolveFailedException:
      e = exception()
      failed = True

    a.true(failed, "Resolved a bad type")
=======
    a.equals(instance.left, "right", "Invalid kwargs value")
>>>>>>> b08e720... updated and fixed resolve tests

  def test_passing_stupid_class_fails(self):
    
    class IPrinter(object):
      def prints(self, msg):
        pass

    class IValuer(object):
      def value(self, a, b):
        pass

    @implements(IPrinter)
    class Printer(object):
      def __init__(self, value):  # <-- Stupid, needs zero value constructor
        pass
      def prints(self, msg):
        return "prints-" + str(msg)

    @implements(IValuer)
    class Valuer(object):
      def value(self, a, b):
        return a + b

    c = Scope()
    c.register(Printer)
    c.register(Valuer)

    @resolve(c)
    class HasDeps(object):
      def __init__(self, valuer=IValuer, printer=IPrinter):
        self.valuer = valuer
        self.printer = printer

    a = Assert()

    failed = False
    try:
      instance = HasDeps()
    except ResolveFailedException:
      e = exception()
      failed = True
      print(e)
      a.equals(e.type, Printer, "Didnt set correct exception value")
    a.true(failed, "Didn't fail")

  def test_when_failing_to_resolve_type_exception_has_type_set(self):
    
    class IPrinter(object):
      def prints(self, msg):
        pass

    class IValuer(object):
      def value(self, a, b):
        pass

    @implements(IValuer)
    class Valuer(object):
      def value(self, a, b):
        return a + b

    c = Scope()
    c.register(Valuer)

    @resolve(c)
    class HasDeps(object):
      def __init__(self, valuer=IValuer, printer=IPrinter):
        self.valuer = valuer
        self.printer = printer

    a = Assert()

    failed = False
    try:
      instance = HasDeps()
    except ResolveFailedException:
      e = exception()
      failed = True
      print(e)
      a.equals(e.type, IPrinter, "Didnt set correct exception value")
    a.true(failed, "Didn't fail")


if __name__ == "__main__":
  unittest.main()
