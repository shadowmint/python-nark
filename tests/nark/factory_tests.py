#!/usr/bin/env python
import bootstrap
import unittest
import time
import nark


class Tests(unittest.TestCase):

  def setup(self):
    return nark.Assert(), nark.Assets(), nark.Factory()
  
  def test_can_create_instance(self):
    t, _, i = self.setup()
    t.not_null(i, "Failed to create Factory instance")
    
  def test_can_load_file(self):
    t, a, i = self.setup()
    path = a.resolve("data", "sample1.py")

    fp = open(path, "w")
    fp.write("text = \"Hello World\"")
    fp.close()

    i.load(path)
    value = i.prop("text")

    t.equals(value, "Hello World", "Failed to read module value")

  def test_does_not_update_file_if_not_watching(self):
    t, a, i = self.setup()
    path = a.resolve("data", "sample1.py")

    fp = open(path, "w")
    fp.write("text = \"Hello World\"")
    fp.close()

    time.sleep(0.5)

    i.load(path)
    value = i.prop("text")

    t.equals(value, "Hello World", "Failed to read module value")

    time.sleep(0.5)

    fp = open(path, "w")
    fp.write("text = \"Hello WORLD\"")
    fp.close()

    value = i.prop("text")
    
    t.equals(value, "Hello World", "Failed to read module value")

  def test_can_update_file(self):
    t, a, i = self.setup()
    path = a.resolve("data", "sample1.py")

    fp = open(path, "w")
    fp.write("text = \"Hello World\"")
    fp.close()

    i.load(path)
    i.watch(True)  # Notice watching now
    value = i.prop("text")

    t.equals(value, "Hello World", "Failed to read module value")

    time.sleep(0.5)

    fp = open(path, "w")
    fp.write("text = \"Hello WORLD\"")
    fp.close()

    value = i.prop("text")
    
    t.equals(value, "Hello WORLD", "Failed to read module value")


if __name__ == "__main__":
  unittest.main()
