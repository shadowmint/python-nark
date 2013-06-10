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


class EnumTests(unittest.TestCase):

  def test_can_create_enum(self):
    a = nark.Assert()
    i = nark.enum("ONE", "TWO")
    a.not_null(i, "Enum instance returned null")
    a.not_equal(i.ONE, i.TWO, "Enum values are not unique")

  def test_can_create_bitflags(self):
    a = nark.Assert()
    i = nark.bitflags("ONE", "TWO")
    a.not_null(i, "Enum instance returned null")
    a.not_equal(i.ONE, i.TWO, "Enum values are not unique")

  def test_bitflags_really_are_bitflags(self):
    a = nark.Assert()
    i = nark.bitflags("ONE", "TWO", "THREE", "FOUR")
    value1 = i.ONE | i.TWO
    value2 = i.TWO | i.THREE | i.FOUR
    a.true(value1 & i.ONE, "Bitflags don't merge correctly (&)")
    a.false(value1 & i.THREE, "Bitflags don't merge correctly (!&)")
    a.false(value2 & i.THREE & i.FOUR, "Bitflags don't merge correctly (&&)")
    a.true(value2 & (i.THREE | i.FOUR), "Bitflags don't merge correctly (&|)")


if __name__ == "__main__":
  unittest.main()
