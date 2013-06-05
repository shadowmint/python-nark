#!/usr/bin/env python
import unittest
import bootstrap
import nark

class EnumTests(unittest.TestCase):

  def test_can_create_enum(self):
    a = nark.Assert()
    i = nark.Enum("ONE", "TWO")
    a.not_null(i, "Enum instance returned null")
    a.not_equal(i.ONE, i.TWO, "Enum values are not unique")
    a.trace("ONE = %r" % i.ONE)
    a.trace("TWO = %r" % i.TWO)

if __name__ == "__main__":
  unittest.main()
