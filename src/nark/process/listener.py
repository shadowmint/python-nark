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

from nark import *


class Listener:
  """ Event type passed by the messenger """
  
  id = 0
  """ The id of the event; nb. this should be an int, use enum """
  
  callback = None
  """ The callback itself """
  
  def __init__(self, id, callback):
    self.id = id
    self.callback = callback
    
  def invoke(self, listener):
    try:
      cb = self.callback
      if listener.data is None:
        cb()
      else:
        cb(listener.data)
    except Exception:
      e = exception()
      log.error("Failed to invoke callback: %s" % e)
      
  def matches(self, event):
    return event.id == self.id
      
  def __repr__(self):
    return "%d --> %r" % (self.id, self.callback)


# Logging
log = Logging.get()
