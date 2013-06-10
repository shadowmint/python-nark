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

    class HasDeps(object):
      def __init__(self):
        self.valuer = IValuer
        self.printer = IPrinter

    c = Resolver()
    c.register(Printer)
    c.register(Valuer)

    a = Assert()

    c = Resolver()
    c.register(Printer)
    c.register(Valuer)

    instance = HasDeps()
    c.resolve(instance)

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

    class HasDeps(object):
      def __init__(self):
        self.valuer = IValuer
        self.printer = IPrinter

    @implements(IValuer, IPrinter)
    class Crazy(object):
      def value(self, a, b):
        return a - b
      def prints(self, msg):
        return "hello-" + str(msg)

    c = Resolver()
    c.register(Crazy)

    a = Assert()

    instance = HasDeps()
    c.resolve(instance)

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

    class UsesDb(object):
      def __init__(self):
        self.db = IDb

    c = Resolver()
    c.register(Db, resolve.INSTANCE)

    a = Assert()

    i1 = UsesDb()
    c.resolve(i1)

    i2 = UsesDb()
    c.resolve(i2)

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

    class UsesDb(object):
      def __init__(self):
        self.db = IDb

    c = Resolver()
    c.register(Db)

    a = Assert()

    i1 = UsesDb()
    c.resolve(i1)

    i2 = UsesDb()
    c.resolve(i2)

    i1.db.data()["key"] = "value"
    a.equals(i2.db.data()["key"], "value", "Object was not a singleton")

    i2.db.data()["key"] = "value2"
    a.equals(i1.db.data()["key"], "value2", "Object was not a singleton")


if __name__ == "__main__":
  unittest.main()
