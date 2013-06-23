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
from nark import *


class DynamicTests(unittest.TestCase):

  def test_can_create_logger(self):
    a = Assert()
    i = Dynamic()
    a.not_null(i, "Unable to create instance")

  def test_can_iterate_over_properties(self):
    a = Assert()
    i = Dynamic()
    i.x = "Y"
    i.y = "Z"
    i.z = "Q"

    count = 0
    for k, v in i:
      count += 1

    a.equals(count, 3, "Didn't find all keys")

  def test_can_turn_into_dict(self):
    a = Assert()
    i = Dynamic()
    i.x = "Y"
    i.y = "Z"
    i.z = "Q"
    i.sub.x = "Y"
    i.sub.y = "X"

    d = dict(iter(i))

    a.equals(d["x"], "Y", "Failed to convert to dict")
    a.equals(d["z"], "Q", "Failed to convert to dict")
    a.equals(d["sub"]["x"], "Y", "Failed to convert to dict")

  def test_can_load_from_dict(self):
    a = Assert()
    src = {"A" : "B", "C" : "D", "E" : {"F" : "G"}}
    i = Dynamic(src)

    a.equals(i.A, "B", "Didn't convert from dict successfully")
    a.equals(i.C, "D", "Didn't convert from dict successfully")
    a.equals(i.E.F, "G", "Didn't convert from dict successfully")

  def test_can_set_properties(self):
    a = Assert()
    i = Dynamic()

    i.value = "value"
    i.thing = "thing"

    a.equals(i.value, "value", "Didn't set value right")
    a.equals(i.thing, "thing", "Didn't set value right")

  def test_can_set_chained_properties(self):
    a = Assert()
    i = Dynamic()

    i.value.xxx = "value"
    i.value.yyy = "value2"

    a.equals(i.value.xxx, "value", "Didn't set value right")
    a.equals(i.value.yyy, "value2", "Didn't set value right")

  def test_in_behaviour_is_not_stupid(self):
    a = Assert()
    i = Dynamic()

    i.value.xxx = "value"
    i.value.yyy = "value2"

    found = "xxx" in i.value.keys()
    a.true(found, "Couldn't find key")

    found = "yyy" in i.value
    a.true(found, "Couldn't find key")

    found = "yyy" in i.value.values()
    a.false(found, "Found key as value")

    found = "value" in i.value.values()
    a.true(found, "Couldn't find value")

    found = "value" in i.value.keys()
    a.false(found, "Found value as key")

    found = "value" in i.value
    a.false(found, "Found value as key")


if __name__ == "__main__":
  unittest.main()
