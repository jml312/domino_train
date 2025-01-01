from enum import Enum

DominoValue = Enum(
    'DominoValue',
    {f'{i}_{j}': (i, j) for i in range(13) for j in range(i, 13)},
)
DominoValue.__repr__ = lambda self: f"[{self.value[0]}|{self.value[1]}]"

class Domino:
    def __init__(self, left: int, right: int):
      self.left, self.right = sorted((left, right))
        
      if (left, right) not in DominoValue._value2member_map_ and (right, left) not in DominoValue._value2member_map_:
        raise ValueError(f"Invalid domino {self}. Must match one of: \n{list(DominoValue._value2member_map_.values())}")

    def __repr__(self):
      return f"Domino({self.left}, {self.right})"

    def __str__(self):
      return f"[{self.left}|{self.right}]"

    def is_double(self):
      return self.left == self.right

    def matches(self, other_domino):
      return self.left in (other_domino.left, other_domino.right) or self.right in (other_domino.left, other_domino.right)
  