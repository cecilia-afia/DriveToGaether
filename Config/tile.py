# A tile can be represented by the orientations its road leads to
# For example, a straight horizontal road can only lead to either East or West
# It would be created like that : Tile(0,1,0,1)
class Tile:
    def __init__(self,N=0,E=0,S=0,W=0):
        self.N = N
        self.E = E
        self.S = S
        self.W = W


    def getIndex(self) -> int:
        """
        Returns the tile number for current tile.
        :return: 0 if the tile is empty, 1 to 10 according to convention given in editeurConfig.py if tile matches,
        11 by default for all other cases.
        """
        s = f"{self.N}{self.E}{self.S}{self.W}"
        if s == "0000":
            return 0
        elif s == "0101":
            return 1
        elif s == "1010":
            return 2
        elif s == "1100":
            return 3
        elif s == "1001":
            return 4
        elif s == "0110":
            return 5
        elif s == "0011":
            return 6
        elif s == "1101":
            return 7
        elif s == "1110":
            return 8
        elif s == "0111":
            return 9
        elif s == "1011":
            return 10
        else:
            return 11

    def getValue(self, direction: str) -> int:
        """
        Get value specified by direction in input.
        :param direction: string representing the direction, must be one of the following: N, E, S, W
        :return: the corresponding attribute.
        """
        if direction == "N":
            return self.N
        elif direction == "E":
            return self.E
        elif direction == "S":
            return self.S
        elif direction == "W":
            return self.W
        else:
            raise ValueError("getValue: value for string s is invalid, must be one of the following: N, E, S, W.")


    def setValue(self, direction: str, value: int) -> None:
        """
        Sets value corresponding to direction.
        :param direction: string representing the direction, must be one of the following: N, E, S, W.
        :param value: the value to store, must be either 0 or 1.
        """
        if value not in [0,1]:
            raise ValueError("setValue: value must be either 0 or 1.")
        if direction == "N":
            self.N = value
        elif direction == "E":
            self.E = value
        elif direction == "S":
            self.S = value
        elif direction == "W":
            self.W = value
        else:
            raise ValueError("getValue: value for string s is invalid, must be one of the following: N, E, S, W.")
