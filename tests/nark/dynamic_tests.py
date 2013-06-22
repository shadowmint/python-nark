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

import unittest
import bootstrap
import nark



class Dynamic(object):

  def __getattr__(self, key):
    if key not in self.__dict__.keys():
      self.__dict__[key] = Dynamic()
    return self.__dict__[key]

  def __setattr__(self, key, value):
    self.__dict__[key] = valueo

  # TODO: Make iterable
  # test if blah in dy
  # test for k in blah

  # TODO: Convert recursively into a dictionary:
  def import_dict(): 
    pass

  # TODO: Convert recursively from dictionary:
  def export_dict(self, source):
    pass


class DynamicTests(unittest.TestCase):

  def test_can_create_logger(self):
    a = nark.Assert()
    i = Dynamic()
    a.not_null(i, "Unable to create instance")

  def test_can_set_properties(self):
    a = nark.Assert()
    i = Dynamic()

    i.value = "value"
    i.thing = "thing"

    a.equals(i.value, "value", "Didn't set value right")
    a.equals(i.thing, "thing", "Didn't set value right")

  def test_can_set_chained_properties(self):
    a = nark.Assert()
    i = Dynamic()

    i.value.xxx = "value"
    i.value.yyy = "value2"

    a.equals(i.value.xxx, "value", "Didn't set value right")
    a.equals(i.value.yyy, "value2", "Didn't set value right")

  def test_cannot_resolve_missing_properties(self):
    a = nark.Assert()
    i = Dynamic()

    i.value.xxx = "value"
    i.value.yyy = "value2"

    failed = False
    try:
      k = i.value.zzz
    except AttributeError:
      e = exception()
      print(e)
      failed = True
    a.true(failed, "Failed to raise exception")


if __name__ == "__main__":
  unittest.main()
