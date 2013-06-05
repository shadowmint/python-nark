# Copyright 2012 Douglas Linder
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

from log import Log

class Assert:
  """ Test helper """
  
  def __init__(self):
    self._logger = Log()
    #if self._logger is None:
      #instance = nark.Log()
      #instance.setLogWriter(nark.log.CliWriter())
      #nark.Register.get().bind(instance)
    #self._logger = nark.Log.get()
    
  def true(self, value, message):
    if not value:
      self._fail("%s (value was not True)" % (message))
  
  def false(self, value, message):
    if value:
      self._fail("%s (value was True)" % (message))
      
  def not_equal(self, v1, v2, message):
    if v1 == v2:
      self._fail("%s (%s != %s)" % (message, str(v1), str(v2)))
      
  def equal(self, v1, v2, message):
    if not v1 == v2:
      self._fail("%s (%s != %s)" % (message, str(v1), str(v2)))
      
  def null(self, value, message):
    if not value is None:
      self._fail("%s (%s was not None)" % (message, str(value)))
      
  def not_null(self, value, message):
    if value is None:
      self._fail("%s (value was None)" % (message, str(value)))
      
  def trace(self, message):
    self._logger.trace(message)
      
  def _fail(self, message):
    try:
      assert False
    except Exception, e:
      self._logger.error(message, e)
    assert False
