#!/usr/bin/env python

import bootstrap
from nark import *
import nark.process
import unittest
import time
import random


class WorkerTests(unittest.TestCase):

  def callback(self):
    log.info("Callback invoked")

  def test_can_run_simple_job(self):
    j = Job()
    j.start()

  def test_can_run_callback_worker(self):
    j = JobCallback()
    j.callback = self.callback
    j.start()
    log.info("Doing the thing")
    time.sleep(0.5)

  def test_can_run_talky_worker(self):
    j = JobTalk()
    j.start()
    for i in range(10):
      time.sleep(0.1)
      log.info("FG process tick: %d" % i)
    log.info("Done")


# Test event code
RANDOM_ACTION = 0x0ff


class Job(nark.process.Worker):
  def remote(self, data):
    time.sleep(0.1)
    log.info("Did action")

  def local(self, data):
    self.api.event_loop()


class JobCallback(nark.process.Worker):
  def remote(self, data):
    time.sleep(0.1)

  def local(self, data):
    self.api.listen(nark.process.WorkerEvents.TERMINATE, self.callback)
    self.api.event_loop()


class JobTalk(nark.process.Worker):
  def trace(self, msg):
    log.info("%s: %s" % (self.ident, msg))

  def random_action(self, action):
    self.trace("Got action: %s" % action)
    if action == "DIE":
      self.trace("Stop")
      self.api.stop()
    else:
      actions = ["ONE", "TWO", "THREE", "FOUR", "DIE"]
      action = actions[random.randint(0, len(actions) - 1)]
      self.api.trigger(RANDOM_ACTION, action)
      self.trace("Sending: %s" % action)
    time.sleep(0.1)

  def remote(self, data):
    self.ident = "REMOTE"
    self.api.listen(RANDOM_ACTION, self.random_action)
    self.api.event_loop()

  def local(self, data):
    self.ident = "LOCAL"
    self.api.listen(RANDOM_ACTION, self.random_action)
    self.random_action("ONE")
    self.api.event_loop(False)


log = LogManager.get_logger()
if __name__ == "__main__":
    unittest.main()
