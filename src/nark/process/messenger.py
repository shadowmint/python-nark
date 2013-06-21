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

from __future__ import absolute_import
from .event import Event
from .listener import Listener
from nark import Logging, exception


class Messenger(object):
  """ Messenger is a event handler / trigger to pass between processes.
  
      To use messenger, you would typically do something like this:
      
      pc, cc = Pipe(True)
      pm = Messenger(pc)
      cc = Messenger(cc)
      p = Process(target=blah, args=(cc,))
      p.start()
      
      running = True
      while running:
        # do normal app loop things, and then periodically call:
        pm.poll()
        
      Basically messenger wraps Pipe and lets messages get sent back
      and forth between processes. 
      
      Every message sent is wrapped in an event type container, which
      messenger uses to dispatch to listening callbacks.
      
      You can register callbacks using listen(), eg:
      
      pm.listen(EVENT_ID, my_callback)
      
      ...and trigger events *on the remote side of the pipe* using:
      
      pm.trigger(EVENT_ID, event)
      
      Notice specifically that unless both sides of the pipe are in the
      same process (in which case, why are you even using this?) calling
      trigger() will NOT trigger events attached to the local listener,
      regardless of event id.
  """
  
  _pipe = None
  """ Pipe for this messenger """
    
  _listeners = {} 
  """ Set of listeners which have been attached """
  
  def __init__(self, pipe):
    self._pipe = pipe
    self._listeners = {}
    
  def listen(self, uid, callback):
    """ Listen to specific event id and invoke callback when it occurs.
    
        The callback should match the signature:
        
        def callback(event):
          ...
          
        Or for class methods, use:
        
        def callback(self, event):
          ...
    """
    l = Listener(uid, callback)
    if not uid in self._listeners:
      self._listeners[uid] = []
    self._listeners[uid].append(l)
    
    # Helpful in debugging things
    #items = ""
    #for l in self._listeners.keys():
    #  for v in self._listeners[l]:
    #    if not items == "":
    #      items += ", "
    #    items += str(v)
    #log.info("Listeners: %s" % items)
 
  def trigger(self, uid, event=None):
    """ Trigger an event on the remote messenger 
    
        Actually all this function does is wrap the id and event and pass
        it to the pipe. The remote side must handle the event to dispatch it
        
        If the pipe is closed, trigger does nothing. It's up to the user
        to make sure the client thread terminates nicely.
    """
    item = Event(uid, event)
    try:
      self._pipe.send(item)
    except Exception:
      e = exception()
      log.error("Failed to trigger event: %d: %s" % (uid, e))

  def poll(self, limit=0):
    """ Listen on the pipe for any pending events and then return 
    
        This is not a blocking operation, at most 'limit' events will
        be processed (prevent recursive spam).

        Returns False if the pipe is dead.
    """
    count = 0
    while limit == 0 or count < limit:
      if self._pipe.poll():
        try:
          data = self._pipe.recv()
        except Exception:
          e = exception()
          log.info("Messenger: Remote process terminated")
          return False
        processed = 0
        for _, v in self._listeners.items():
          for i in v:
            if i.matches(data):
                try:
                  i.invoke(data)
                except Exception:
                  e = exception()
                  log.error("Failed to invoked bound trigger: %s" % e)
                processed += 1
        if processed == 0:
          log.warn("Warning! Failed to dispatch unbound event id: %d" % data.id)
      else:
        break
      if limit > 0:
        count += 1
    return True
  
  def close(self):      
    """ Stop this messenger """
    self._pipe.close()
      

# Logging
log = Logging.get()
