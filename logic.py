import random
class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = []

        i = 1
        for r in range(self.rows):
            self.grid.append([])
            for _ in range(self.cols):
                self.grid[r].append(i)
                i += 1

        self.grid[self.rows-1][self.cols-1] = 0


    def shuffle(self, moves):
        previous = (None, None)
        for _ in range(moves):
            blank = self.getBlank()
            piece = random.choice([i for i in self.getAdjacent(blank) if i != previous])
            previous = blank
            self.move(piece)

    def numToPos(self, num):
        posGrid = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        return posGrid[num-1]

    def getCell(self, r, c):
        return self.grid[r][c]

    def getBlank(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 0:
                    return (r, c)

        return (None, None)

    def getAdjacent(self, pos):
        r, c = pos
        adj = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        return [(r1, c1) for (r1, c1) in adj if (0 <= r1 < self.rows) and (0 <= c1 < self.cols)]

    def move(self, pos):
        blank = self.getBlank()
        if blank in self.getAdjacent(pos):
            r, c = pos
            r1, c1 = blank
            self.grid[r][c], self.grid[r1][c1] = self.grid[r1][c1], self.grid[r][c]
            return True

        return False

    def checkSolved(self):
        i = 1
        for r in range(self.rows):
            for c in range(self.cols):
                if r == self.rows-1 and c == self.cols-1 and (self.grid[r][c] == 0 or self.grid[r][c] == i):
                    return True

                elif self.grid[r][c] != i:
                    return False
                
                i += 1

        return True
