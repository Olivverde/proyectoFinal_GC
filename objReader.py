class Obj(object):
  def __init__(self, filename):
    with open(filename) as f:
      self.lines = f.read().splitlines()

    self.v = []
    self.vt = []
    self.f = []
    self.vn = []
    self.read()

  def read(self):
    for line in self.lines:
      if line:
        prefix, value = line.split(' ', 1)

        if prefix == 'v':
          self.v.append(
            list(map(float, value.split(' ')))
          )
        elif prefix == 'vt':
          if (len(self.vt) < len(self.v)):
            textures = list(map(float, value.split(' ')))
            if (len(textures) == 2):
              textures.append(0)
            
            self.vt.append(textures)
        elif prefix == 'vn':
          self.vn.append(
            list(map(float, value.split(' ')))
          )
        elif prefix == 'f':
          getF = [list(map(int, face.split('/'))) for face in value.split(' ')]

          if (len(getF) == 3):
            self.f.append(getF)
          else:
            self.f.append(getF[0:3])
            self.f.append([getF[0], getF[2], getF[3]])