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

import logging


class LogManager(object):
  """ Convenience helper to get a named logger """
  
  @staticmethod
  def _new_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s: %(message)s (%(levelname)s)')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

  @classmethod
  def _logger(cls, name):
    try:
      cache = cls.__loggers 
    except AttributeError:
      cls.__loggers = {}
    if not name in cls.__loggers:
      cls.__loggers[name] = LogManager._new_logger(name)
    return cls.__loggers[name]

  @classmethod
  def get_logger(cls, depth=1):
    import inspect
    frame = inspect.stack()[depth]
    target = frame[1]
    return LogManager._logger(target)
