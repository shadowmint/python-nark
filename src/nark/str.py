def as_str(value):
  """Convert an arbitrary object into a str value """
  if value is None:
    return 'None'
  try:
    return str(value)
  except:
    try:
      tmp = unicode(value).encode('utf-8')
      return tmp.decode('ascii', 'ignore')
    except:
      return "[{}] could not to converted to a string".format(value.__class__)
