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
import bootstrap
import unittest
from nark import *

class LogTests(unittest.TestCase):

  def test_all_the_things(self):

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


if __name__ == "__main__":
  unittest.main()
