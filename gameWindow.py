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

        self.width = (self.cols*self.squareSize) + ((self.cols-1)*self.borderSize)
        self.height = (self.rows*self.squareSize) + ((self.rows-1)*self.borderSize)
    
    def initFormatting(self, title, showNumbers, useImage, extras):
        self.title = title
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.borderColor = (255, 255, 255)
        self.tileRects = []

        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(self.borderColor)
        self.showNumbers = showNumbers

        if self.showNumbers:
            fontName = extras[0]
            self.font = pygame.font.SysFont(fontName, int(self.squareSize / 3), bold=True)
        
        self.useImage = useImage
        if self.useImage:
            imagePath = extras[1]
            self.imageSurf = pygame.transform.scale(pygame.image.load(imagePath), 
            (self.squareSize * self.cols, self.squareSize * self.rows))

            self.tileSurfaces = []
            for r in range(self.rows):
                self.tileRects.append([])
                self.tileSurfaces.append([])
                for c in range(self.cols):
                    surf = pygame.Surface((self.squareSize, self.squareSize))
                    x = c * self.squareSize
                    y = r * self.squareSize
                    surf.blit(self.imageSurf, (0, 0), area=(x, y, self.squareSize, self.squareSize))
                    self.tileSurfaces[r].append(surf)
                    posX = c * (self.squareSize + self.borderSize)
                    posY = r * (self.squareSize + self.borderSize)

                    self.tileRects[r].append(pygame.Rect(posX, posY, 
                    self.squareSize, self.squareSize))
                    pygame.draw.rect(self.background, (0, 0, 0), self.tileRects[r][c])

        else:
            self.tileColor = extras[1]
            for r in range(self.rows):
                self.tileRects.append([])
                for c in range(self.cols):
                    posX = c * (self.squareSize + self.borderSize)
                    posY = r * (self.squareSize + self.borderSize)

                    self.tileRects[r].append(pygame.Rect(posX, posY,
                    self.squareSize, self.squareSize))
                    pygame.draw.rect(self.background, (0, 0, 0), self.tileRects[r][c])

    def initSpeed(self):
        self.fps = 60
        self.slideVel = int(self.squareSize / 5)
        self.shuffleVel = int(((self.rows+self.cols) / 2) * self.squareSize / 7)
        self.clock = pygame.time.Clock()

    def initGame(self):
        self.grid = Grid(self.rows, self.cols)
        self.shuffleMoves = (self.rows*self.cols) * 5
        self.shuffleAnimation()
        

    def updateDisplay(self):
        self.window.blit(self.background, (0, 0))
        blankR, blankC = self.grid.getBlank()
        pygame.draw.rect(self.window, (0, 0, 0), self.tileRects[blankR][blankC])

        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) == (blankR, blankC):
                    continue

                if self.useImage:
                    r1, c1 = self.grid.numToPos(self.grid.getCell(r, c))
                    self.window.blit(self.tileSurfaces[r1][c1], self.tileRects[r][c])

                else:
                    pygame.draw.rect(self.window, self.tileColor, self.tileRects[r][c])

                if self.showNumbers:
                    textSurf = self.font.render(str(self.grid.getCell(r, c)), True, (self.borderColor))
                    rect = self.tileRects[r][c]
                    self.window.blit(textSurf, (rect.x + 5, rect.y + 5))

        pygame.display.update()

    def slide(self, pos):
        moved = self.grid.move(pos)
        if moved:
            return self.grid.checkSolved()


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
        print(self.slide((row, col)))


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
                print(self.slide((pieceR, pieceC)))
                

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
            self.handleEvents()
