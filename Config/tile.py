# A tile can be represented by the orientations its road leads to
# For example, a straight horizontal road can only lead to either East or West
# It would be created like that : Tile(0,1,0,1)
class Tile:
	def __init__(self,N=0,E=0,S=0,W=0):
		self.N = N
		self.E = E
		self.S = S
		self.W = W