import os
import subprocess

class BadCommandException(Exception):
  pass

def run(program, *kargs, **kwargs):
  """ Run a program on the path, with arguments.

      Use it like this:

      run("ls", "/home/")

      Or, if you just want to check IF the command can run, 
      without actually running it, pass 'check_only' like this:

      run(
  """
  resolved = which(program)
  if "check_only" in kwargs:
    return resolved is not None
  else:
    if resolved is not None:
      prog = [resolved]
      prog.extend(kargs)
      p = subprocess.call(prog)
    else:
      raise BadCommandException("Missing command: '%s'" % program)
  return True
    
def is_exe(fpath):
  """ Check file exists and is executable.
      TODO: Better way to do this maybe?
  """
  return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def which(program):
  """ Resolve a program from the PATH if possible """
  fpath, fname = os.path.split(program)
  if fpath:
    if is_exe(program):
      return program
  else:
    for path in os.environ["PATH"].split(os.pathsep):
      path = path.strip('"')
      exe_file = os.path.join(path, program)
      if is_exe(exe_file):
        return exe_file
  return None
