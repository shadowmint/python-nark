# Copyright 2012 Douglas Linder
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import importlib
from nark import Dynamic, Logging
logging = Logging.get()


class RequiredConfigError(Exception):
  """ Specific error for missing config keys """
  pass


class Extension(object):
  """ A helper module for writing pyramid extensions

  You can easily use it like this:

      from nark.pyramid import Extension

      class Config(Extension):
        def __init__(self, config):
          super(Config, self).__init__(config)
          self.keys.ROOT = 'pyramid_admin.root'
          self.keys.OVERRIDE = 'pyramid_admin.override'
          self.defaults.ROOT = 'home'

  Then invoke this from the extension like:

      def includeme(config):
        ext = Config(config)
        root = ext.resolve(ext.keys.ROOT, required=True)
        config.add_route(...)

        module = ext.resolve(ext.keys.PERMISSIONS, as_module=True)
        if module is not None:
          ...
  """

  def __init__(self, config):
    self.keys = Dynamic()
    self.defaults = Dynamic()
    self.config = config
    self.settings = config.get_settings()

  def _default(self, key):
    """Override this function to provide defaults for types """
    for v in self.keys.keys():
      if key == self.keys[v]:
        key = v
    if key in self.defaults:
      return self.defaults[key]
    return None

  def resolve(self, key, as_module=False, required=False):
    """Import a named type or fallback to the default """
    def fail(msg, failure=None):
      if required:
        raise RequiredConfigError(msg)
      elif failure is not None:
        logging.warn(msg)
        logging.warn(failure)
    if as_module:
      try:
        key = self.settings[key]
        mod, func = key.rsplit('.', 1)
        loaded = importlib.import_module(mod)
        return getattr(loaded, func)
      except ImportError as e:
        fail('Failed to import binding for {}'.format(key), e)
      except ValueError as e:
        fail('Invalid binding for {}'.format(key), e)
      except KeyError:
        fail('No config binding for {}'.format(key))
    else:
      try:
        return self.settings[key]
      except KeyError:
        fail('No config binding for {}'.format(key))
    return self._default(key)