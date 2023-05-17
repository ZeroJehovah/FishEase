class RECT:
    def __init__(self, left, top, right, bottom):
        self.left: int = int(left) if left else 0
        self.top: int = int(top) if top else 0
        self.right: int = int(right) if right else 0
        self.bottom: int = int(bottom) if bottom else 0

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right and self.top == other.top and self.bottom == other.bottom
