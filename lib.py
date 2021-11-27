from collections import namedtuple

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])

def sum(v0, v1):
  x = v0.x + v1.x
  y = v0.y + v1.y
  z = v0.z + v1.z
  return V3(x, y, z)

def sub(v0, v1):
  x = v0.x - v1.x
  y = v0.y - v1.y
  z = v0.z - v1.z
  return V3(x, y, z)

def mul(v0, k):
  x = v0.x * k
  y = v0.y * k
  z = v0.z * k
  return V3(x, y, z)

def dot(v0, v1):
  x = v0.x * v1.x
  y = v0.y * v1.y
  z = v0.z * v1.z
  dotProd = x + y + z
  return dotProd

def cross(v0, v1):
  x = v0.y * v1.z - v0.z * v1.y
  y = v0.z * v1.x - v0.x * v1.z
  z = v0.x * v1.y - v0.y * v1.x  
  return V3(x, y, z)

def length(v0):
  vecLen = (v0.x**2 + v0.y**2 + v0.z**2)**0.5
  return vecLen

def norm(v0):
  l = length(v0)
  if l == 0:
    return V3(0, 0, 0)
  x = v0.x/l
  y = v0.y/l
  z = v0.z/l
  return V3(x, y, z)

def bbox(A, B, C):
    xs = [A.x, B.x, C.x]
    ys = [A.y, B.y, C.y]
    xs.sort()
    ys.sort()
    return round(xs[0]), round(xs[-1]), round(ys[0]), round(ys[-1])

def barycentric(A, B, C, P):
  cx, cy, cz = cross(
      V3(C.x - A.x, B.x - A.x, A.x - P.x),
      V3(C.y - A.y, B.y - A.y, A.y - P.y)
  )
  if cz == 0:
      return -1, -1, -1
  u = cx/cz
  v = cy/cz
  w = 1 - (u + v)

  return w, v, u