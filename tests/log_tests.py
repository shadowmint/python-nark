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


class LogTests(unittest.TestCase):

  def test_can_create_logger(self):
    a = nark.Assert()
    i = nark.LogManager.get_logger()
    a.not_null(i, "Unable to create log instance")

  def test_can_log_message(self):
    a = nark.Assert()
    i = nark.LogManager.get_logger()
    i.debug("Hello %s", "world")
    i.info("Hello %s", "world")
    i.warning("Hello %s", "world")
    i.error("Hello %s", "world")
    i.critical("Hello %s", "world")


if __name__ == "__main__":
  unittest.main()
