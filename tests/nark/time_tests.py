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

class TimeTests(unittest.TestCase):

  def test_convert_to_timestamp_and_back(self):
    a = Assert()
    now = DateTime.now()
    timestamp = DateTime.as_timestamp(now)
    datetime = Timestamp.as_datetime(timestamp)
    a.true(datetime == now, "Failed to convert timestamp back")


if __name__ == "__main__":
  unittest.main()
