#!/usr/bin/env python

import bootstrap
from multiprocessing import Process, Pipe
import unittest
import time
import unittest
from nark import *


class MessengerTests(unittest.TestCase):

  def test_can_create_instances(self):
    a, lm, rm = self.setup()
    
    a.not_null(lm, "Failed to create local messenger")
    a.not_null(rm, "Failed to create remote messenger")
    
    self.teardown(lm, rm)
    
  def test_can_trigger_event(self):
    a, lm, rm = self.setup()
    
    # Setup
    self.check = False
    def callback(data):
      self.check = True
    rm.listen(1, callback)
    
    # Act
    lm.trigger(1, "Hello World")
    rm.poll()
    
    # Check
    a.true(self.check, "Callback was not invoked")
    
    self.teardown(lm, rm)
    
  def test_can_trigger_multiple_events(self):
    a, lm, rm = self.setup()
    
    # Setup
    self.c1 = 0
    self.c2 = 0
    def callback1(data):
      self.c1 += 1
    def callback2(data):
      self.c2 += 1
    rm.listen(1, callback1)
    rm.listen(2, callback2)
    
    # Act
    lm.trigger(1, "Hello World")
    lm.trigger(2, "Hello World")
    lm.trigger(1, "Hello World")
    lm.trigger(2, "Hello World")
    rm.poll(2)
    
    # Check
    a.equals(self.c1, 1, "Callback callback wrong number of times")
    a.equals(self.c2, 1, "Callback callback wrong number of times")
    
    # Act
    rm.poll(2)
    
    # Check
    a.equals(self.c1, 2, "Callback callback wrong number of times")
    a.equals(self.c2, 2, "Callback callback wrong number of times")
    
    # Act
    lm.trigger(1, "Hello World")
    lm.trigger(2, "Hello World")
    rm.poll()
    
    # Check
    a.equals(self.c1, 3, "Callback callback wrong number of times")
    a.equals(self.c2, 3, "Callback callback wrong number of times")
    
    self.teardown(lm, rm)
    
  def test_can_talk_between_processes(self):
    
    a, lm, rm = self.setup()
    
    # ID codes
    EVENTS = enum (
      "REQUEST", 
      "RESPONSE",
      "KILL",
    )
    
    # Worker: Send response on request
    class Remote:
      
      def __init__(self, messenger):  
        self._dead = False
        self.msg = messenger
        self.msg.listen(EVENTS.REQUEST, self.handle_request)
        self.msg.listen(EVENTS.KILL, self.handle_kill)
        
      def handle_request(self, data):
        self.msg.trigger(EVENTS.RESPONSE, "Hello World")
        a.trace("Got request, sent response")
      
      def handle_kill(self):
        self._dead = True
        a.trace("Got kill, stopping")
        
      def run(self):
        while not self._dead:
          self.msg.poll()
          time.sleep(0.05)
        
    # Spawn the process with this
    def remote_process(messenger):
      worker = Remote(messenger)
      worker.run()
        
    # Local handler
    self.resp_msg = ""
    def local_callback(data):
      a.trace("Got local response!")
      self.resp_msg = data
    lm.listen(EVENTS.RESPONSE, local_callback)
    
    # Spawn process
    p = Process(target=remote_process, args=(rm,))
    p.start()
    
    # Trigger event that should generate a callback
    lm.trigger(EVENTS.REQUEST, "HI")
    while self.resp_msg == "":
      time.sleep(0.05)
      lm.poll()
      
    # Wait for exit
    lm.trigger(EVENTS.KILL)
    p.join()
    print("Thread stopped, we're good")
    
    self.teardown(lm, rm)
    
  def test_can_talk_between_processes_without_spamming(self):
    
    a, lm, rm = self.setup()
    
    # ID codes
    EVENTS = enum (
      "REQUEST", 
      "RESPONSE",
      "KILL",
    )
    
    # Worker: Send response on request
    class Remote:
      
      def __init__(self, messenger):  
        self._dead = False
        self.msg = messenger
        self.msg.listen(EVENTS.REQUEST, self.handle_request)
        self.msg.listen(EVENTS.KILL, self.handle_kill)
        
      def handle_request(self, data):
        self.msg.trigger(EVENTS.RESPONSE, "Hello World " + str(data))
        a.trace("Got request (%d), sent response" % data)
      
      def handle_kill(self):
        self._dead = True
        a.trace("Got kill, stopping")
        
      def run(self):
        while not self._dead:
          self.msg.poll(3)
          time.sleep(0.05)
        
    # Spawn the process with this
    def remote_process(messenger):
      worker = Remote(messenger)
      worker.run()
        
    # Local handler
    self.resp_msg = 0
    def local_callback(data):
      a.trace("Response: %s" % data)
      self.resp_msg += 1
      for i in range(5):
        a.trace("Sending request in row %d!" % self.resp_msg)
        lm.trigger(EVENTS.REQUEST, self.resp_msg + i)
    lm.listen(EVENTS.RESPONSE, local_callback)
    
    # Spawn process
    p = Process(target=remote_process, args=(rm,))
    p.start()
    
    # Trigger event that should generate a callback
    lm.trigger(EVENTS.REQUEST, 0)
    while self.resp_msg < 20:
      time.sleep(0.05)
      lm.poll(3)
      a.trace("Current status: %d" % self.resp_msg)
      
    # Wait for exit
    lm.trigger(EVENTS.KILL)
    p.join()
    print("Thread stopped, we're good")
    
    self.teardown(lm, rm)
 
  def setup(self):
    local, remote = Pipe()
    lm = process.Messenger(local)
    rm = process.Messenger(remote)
    a = Assert()
    return a, lm, rm
    
  def teardown(self, m1, m2):
    m1.close()
    m2.close()
    
if __name__ == "__main__":
  unittest.main()
