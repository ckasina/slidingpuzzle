import pygame
import random
from logic import Grid

class gameWindow:
    def __init__(self, title, rows, cols, showNumbers, useImage, previousWindow, extras=[]):
        pygame.init()
        self.previousWindow = previousWindow
        self.running = True
        self.sliding = False

        self.initSizes(rows, cols)
        self.initFormatting(title, showNumbers, useImage, extras)
        self.initSpeed()
        self.initGame()
        self.mainloop()
        
    def initSizes(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.squareSize = 75
        self.borderSize = 3

        self.gridWidth = (self.cols*self.squareSize) + ((self.cols-1)*self.borderSize)
        self.gridHeight = (self.rows*self.squareSize) + ((self.rows-1)*self.borderSize)

        self.width = self.gridWidth
        self.height = self.gridHeight + self.squareSize + (self.borderSize * 2)
    
    def initFormatting(self, title, showNumbers, useImage, extras):
        self.title = title
        self.borderColor = (255, 255, 255)
        
        self.background = pygame.Surface((self.gridWidth, self.gridHeight))
        self.background.fill(self.borderColor)
        self.gridSurf = pygame.Surface((self.gridWidth, self.gridHeight))
        self.statusSurf = pygame.Surface((self.gridWidth, self.height - self.gridHeight))
        self.window = pygame.display.set_mode((self.width, self.height))
        
        pygame.display.set_caption(self.title)

        self.tileRects = []

        self.showNumbers = showNumbers

        if self.showNumbers:
            fontName = extras[0]
            self.font = pygame.font.SysFont(fontName, int(self.squareSize / 3), bold=True)

        else:
            self.font = pygame.font.SysFont("Comic Sans MS", int(self.squareSize / 3), bold=True)

        
        self.useImage = useImage
        if self.useImage:
            imagePath = extras[1]
            self.imageSurf = pygame.transform.scale(pygame.image.load(imagePath), 
            (self.squareSize * self.cols, self.squareSize * self.rows))

            self.tileSurfaces = []

        else:
            self.tileColor = extras[1]

        for r in range(self.rows):
            self.tileRects.append([])
            if self.useImage:
                self.tileSurfaces.append([])

            for c in range(self.cols):
                posX = c * (self.squareSize + self.borderSize)
                posY = r * (self.squareSize + self.borderSize)

                self.tileRects[r].append(pygame.Rect(posX, posY,
                self.squareSize, self.squareSize))
                pygame.draw.rect(self.background, (0, 0, 0), self.tileRects[r][c])

                if self.useImage:
                    surf = pygame.Surface((self.squareSize, self.squareSize))
                    x = c * self.squareSize
                    y = r * self.squareSize
                    surf.blit(self.imageSurf, (0, 0), area=(x, y, self.squareSize, self.squareSize))
                    self.tileSurfaces[r].append(surf)

    def initSpeed(self):
        self.fps = 60
        self.slideVel = int(self.squareSize / 5)
        self.shuffleVel = int(((self.rows+self.cols) / 2) * self.squareSize / 7)
        self.clock = pygame.time.Clock()

    def initGame(self):
        self.grid = Grid(self.rows, self.cols)
        self.won = False
        self.moves = 0
        self.shuffleMoves = (self.rows*self.cols) * 5
        self.shuffleAnimation()
        
    def updateDisplay(self):
        self.updateGridSurf()
        self.updateStatusSurf()
        self.window.blit(self.gridSurf, (0, 0))
        self.window.blit(self.statusSurf, (0, self.gridHeight))
        pygame.display.update()

    def updateStatusSurf(self):
        self.statusSurf.fill((0, 0, 0))
        pygame.draw.rect(self.statusSurf, self.borderColor, (0, 0, self.gridWidth, self.height - self.gridHeight), self.borderSize)
        
        text = {False: f"Moves: {self.moves}", True: f"Finished in {self.moves} moves!"}[self.won]
        textSurf = self.font.render(text, True, self.borderColor)
        textX = (self.statusSurf.get_width() - textSurf.get_width()) // 2
        textY = (self.statusSurf.get_height() - textSurf.get_height()) // 2

        self.statusSurf.blit(textSurf, (textX, textY))

    def updateGridSurf(self):
        self.gridSurf.blit(self.background, (0, 0))
        blankR, blankC = self.grid.getBlank()
        if (blankR, blankC) != (None, None):
            pygame.draw.rect(self.gridSurf, (0, 0, 0), self.tileRects[blankR][blankC])

        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) == (blankR, blankC):
                    continue

                if self.useImage:
                    r1, c1 = self.grid.numToPos(self.grid.getCell(r, c))
                    self.gridSurf.blit(self.tileSurfaces[r1][c1], self.tileRects[r][c])

                else:
                    pygame.draw.rect(self.gridSurf, self.tileColor, self.tileRects[r][c])

                if self.showNumbers:
                    textSurf = self.font.render(str(self.grid.getCell(r, c)), True, self.borderColor)
                    rect = self.tileRects[r][c]
                    self.gridSurf.blit(textSurf, (rect.x + 5, rect.y + 5))


    def slide(self, pos):
        moved = self.grid.move(pos)
        if moved:
            self.moves += 1
            return self.grid.checkSolved()

        else:
            return False

    def shuffleAnimation(self):
        previous = (None, None)
        for _ in range(self.shuffleMoves):
            blank = self.grid.getBlank()
            piece = random.choice([i for i in self.grid.getAdjacent(blank) if i != previous])
            previous = blank
            self.slideAnimation(piece, self.shuffleVel)
            self.grid.move(piece)

    def slideAnimation(self, pos, vel):
        self.sliding = True
        blank = self.grid.getBlank()
        adj = self.grid.getAdjacent(blank)
        if pos not in adj:
            self.sliding = False
            return

        posR, posC = pos
        blankR, blankC = blank
        originalRect = pygame.Rect.copy(self.tileRects[posR][posC])
        directionX = blankC - posC
        directionY = blankR - posR
        passedOverX = False
        passedOverY = False

        while (not (passedOverX or passedOverY)) and self.running:
            self.tileRects[posR][posC].x += directionX * vel
            self.tileRects[posR][posC].y += directionY * vel
            self.clock.tick(self.fps)
            self.updateDisplay()

            xDifference = self.tileRects[blankR][blankC].x - self.tileRects[posR][posC].x
            if xDifference != 0:
                passedOverX = xDifference / abs(xDifference) == directionX * -1

            yDifference = self.tileRects[blankR][blankC].y - self.tileRects[posR][posC].y
            if yDifference != 0:
                passedOverY = yDifference / abs(yDifference) == directionY * -1

            self.handleEvents()

        self.tileRects[posR][posC] = pygame.Rect.copy(originalRect)
        self.sliding = False

    def mouseDown(self):
        pos = pygame.mouse.get_pos()
        row, col = -1, -1
        for r in range(self.rows):
            for c in range(self.cols):
                if self.tileRects[r][c].collidepoint(pos):
                    row = r
                    col = c

        if (row, col) == (-1, -1):
            return

        self.slideAnimation((row, col), self.slideVel)
        self.won = self.slide((row, col))


    def keyDown(self, key):
        direction = {pygame.K_LEFT: (0, 1), pygame.K_RIGHT: (0, -1),
        pygame.K_UP: (1, 0), pygame.K_DOWN: (-1, 0)}

        if key not in list(direction.keys()):
            return

        else:
            blankR, blankC = self.grid.getBlank()
            pieceR, pieceC = blankR + direction[key][0], blankC + direction[key][1]
            if (0 <= pieceR < self.rows) and (0 <= pieceC < self.cols):
                self.slideAnimation((pieceR, pieceC), self.slideVel)
                self.won = self.slide((pieceR, pieceC))
                

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.previousWindow.__showWindow__()
                self.running = False
            elif not self.sliding:
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    self.mouseDown()

                elif event.type == pygame.KEYDOWN:
                    self.keyDown(event.key)

    def mainloop(self):
        while self.running:
            self.clock.tick(self.fps)
            self.updateDisplay()
            if self.won:
                blankR = self.rows-1
                blankC = self.cols - 1
                self.grid.grid[blankR][blankC] = self.rows*self.cols
                self.updateDisplay()
                pygame.time.wait(1500)
                if self.useImage:
                    newImage = pygame.transform.scale(self.imageSurf, (self.gridWidth, self.gridHeight))
                    self.gridSurf.blit(newImage, (0, 0))
                    self.window.blit(self.gridSurf, (0, 0))
                    pygame.display.update()
                    pygame.time.wait(1500)

                self.initGame()

            self.handleEvents()
