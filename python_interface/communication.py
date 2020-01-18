

@pytalk_method('test')
def whatever(garbage):
  original_garbage = garbage;
  garbage = "somebody once told me the world was gonna roll me"
  return original_garbage, garbage