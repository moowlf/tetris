# width x height

class IPiece:
    data = [(0,-1), (0,0), (0,1), (0,2)]

class JPiece:
    data = [(0,-1), (0,0), (0,1), (-1,1)]

class LPiece:
    data = [ (0,0), (-1,0), (0,1), (1,1)]

class SquarePiece:
    data = [(0,0),(0,-1), (0,1), (1,1)]

class SPiece:
    data = [(0,0), (0,-1), (1,-1), (-1,0)]

class TPiece:
    data = [(0,0), (-1,0), (1,0), (0,-1)]

class ZPiece:
    data = [ (0,0), (0,-1),(-1,-1), (1,0)]