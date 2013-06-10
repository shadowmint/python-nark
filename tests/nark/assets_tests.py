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


class AssetsTests(unittest.TestCase):

  def test_can_create_instance(self):
    a = Assert()
    i = Assets()
    a.not_null(i, "Unable to create instance")

  def test_can_resolve_file(self):
    a = Assert()
    i = Assets()
    path = i.resolve("data", "sample1.py")
    a.not_null(path, "Unable to resolve file")

  def test_cannot_resolve_missing_file(self):
    a = Assert()
    i = Assets()
    failed = False
    try:
      path = i.resolve("data", "sample1.py", "xxx")
    except BadFileException:
      failed = True
    a.true(failed, "Able to resolve missing file")

  def test_can_find_a_file_that_exists(self):
    a = Assert()
    i = Assets()
    value = False
    if i.exists("data", "sample1.py"):
      value = True
    a.true(value, "Able to resolve missing file")

  def test_cannot_find_a_find_that_is_missing(self):
    a = Assert()
    i = Assets()
    value = False
    if not i.exists("data", "sample1.py", "xxx"):
      value = True
    a.true(value, "Able to resolve missing file")


if __name__ == "__main__":
  unittest.main()
