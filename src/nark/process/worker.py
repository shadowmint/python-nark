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
from multiprocessing import Pipe, Process
from .messenger import Messenger
from nark import enum
import time
import threading


# Special signal from either side to mark the other as dead.
WorkerEvents = enum(TERMINATE=0xfffffff1)


class Worker(object):
  """ Helper class to run things in other processes.

      Use self.api in remote() and local() to do things.
      To handle events in a sub-thread, use api.event_loop()
      To poll once and then do other things, use api.poll(),
      or api.event_loop(False)

      Notice that for a 1-time job where all you need to
      do on the client side is wait for the process to
      complete and then continue, you can do this:

      class MyWorker(Worker):
        def local(self, data):
          self.api.event_loop()
        def remote(self, data):
          # Do stuff here...

      If you need to go and do other things, and just want a
      callback on completion, use:

      class MyWorker(Worker):
        def completed(self):
          # Do callback...
        def local(self, data):
          self.api.listen(WorkerEvents.TERMINATE, self.completed)
          self.api.event_loop(False)  # <--- Don't wait
        def remote(self, data):
          # Do stuff here...

      Obviously for a more complex back-and-forth behaviour, bind
      event listeners on each side.

      Notice that passing between threads involves serializing the
      objects and can incur a performance penalty for large sets.
  """

  def remote(self, data):
    """ This function is invoked in the remote process when it starts. """
    pass
  
  def local(self, data):
    """ This function is invoked in the local process after the process is spawned """
    pass

  def context(self):
    """ If an event loop thread is started, this is run in it first.
        Use this for any thread specific init. eg. Database handles
    """
    pass

  def start(self, data=None):
    """ Start a new process and run the worker in it """

    local, remote = Pipe()
    lmsg = Messenger(local)
    rmsg = Messenger(remote)

    # Remote init
    self._process = Process(target=self._spawn, args=(rmsg, data))
    self._process.start()

    # Local init
    self.api = WorkerApi(self, lmsg)
    self.api.listen(WorkerEvents.TERMINATE, self.api.stop)
    self.local(data)

  def _spawn(self, rmsg, data):
    """ Spawn handler goes here, because windows can't pickle local functions """
    self.api = WorkerApi(self, rmsg, True)
    self.api.listen(WorkerEvents.TERMINATE, self.api.stop)
    self.remote(data)
    self.api.trigger(WorkerEvents.TERMINATE)


class WorkerApi(object):
  """ This is the api that the worker itself has access to. """

  def __init__(self, worker, messenger, remote=False):
    self.__remote = remote
    self.__messenger = messenger
    self.__dead = False
    self.__thread_init = False
    self.__worker = worker

  def listen(self, signal, callback):
    self.__messenger.listen(signal, callback)

  def trigger(self, signal, data=None):
    self.__messenger.trigger(signal, data)

  def kill(self):
    """ On the remote side, does nothing. On the local side, send a kill notice """
    if not self.__remote:
      self.__messenger.trigger(WorkerEvents.TERMINATE)

  def stop(self):
    """ On either side, stop the event loop, send a terminate message to the remote side """
    self.__messenger.trigger(WorkerEvents.TERMINATE)
    self.__dead = True

  def alive(self):
    """ Check if this side is currently alive """
    return not self.__dead

  def ident(self):
    """ Named version of if this is a remote process or not """
    if self.__remote:
      return "remote"
    else:
      return "local"

  def poll(self):
    """ For manually running an event loop """
    return self.__messenger.poll()

  def event_loop(self, wait=True):
    """ For running the event loop forever, depending on 'wait' """
    self.__event_loop = WorkerEventThread(self)
    self.__event_loop.start()
    if wait:
      self.__event_loop.join()

  def context(self):
    """ Invoke context on the parent """
    if not self.__thread_init:
      self.__thread_init = True
      self.__worker.context()


class WorkerEventThread(threading.Thread):
  """ Runs the event loop in its own thread """

  def __init__(self, api):
    super(WorkerEventThread, self).__init__()
    self.api = api

  def run(self):
    self.api.context()
    while self.api.alive():
      if not self.api.poll():
        break
      time.sleep(0.1)  # Don't spam
