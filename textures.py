import struct

def color (b, g, r):
    if 0 <= b <= 1 and 0 <= g <= 1 and 0 <= r <= 1:    
        return bytes([int(b*255), int(g*255), int(r*255)])
    else:
        return bytes([int(b), int(g), int(r)])

class Texture(object):
    def __init__(self, path):
        self.path = path
    
    def getColor(self, tx, ty):
        x = int(tx * self.width) - 1
        y = int(ty * self.height) - 1

        return self.pixels[y][x]

    def read(self):
        image = open(self.path, 'rb')

        image.seek(10)
        header = struct.unpack("=l", image.read(4))[0]

        image.seek(18)
        self.width = struct.unpack("=l", image.read(4))[0]
        self.height = struct.unpack("=l", image.read(4))[0]
        self.pixels = []
        image.seek(header)

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                r = ord(image.read(1))
                g = ord(image.read(1))
                self.pixels[y].append(int.from_bytes(color(b, r, g), 'big'))
        image.close()
        return self.pixels