import pygame

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

screenWidth = 800
screenHeight = 600

class player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(red)
        
        self.rect = self.image.get_rect()
        
        self.changeX = 0
        self.changeY = 0
        
        self.level = None
        
    def update(self):
        
        self.calcGrav()
        self.rect.x += self.changeX
        
        blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        for block in blockHitList:
            if self.changeX > 0:
                self.rect.right = block.rect.left
            elif self.changeX < 0:
                self.rect.left = block.rect.right
        
        self.rect.y += self.change.y
        blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        for block in blockHitList:
            if self.changeY > 0:
                self.rect.bottom = block.rect.top
            elif self.changeY < 0:
                self.rect.top = block.rect.bottom
            
            self.change = 0
    
    def calcGrav(self):
        if self.changeY == 0:
            self.changeY = 1
        else:
            self.changeY += 0.35
    
        if self.rect.y >= screenHeight - self.rect.height and self.changeY >= 0:
            self.changeY = 0
            self.rect.y = screenHeight - self.rect.height
        
    def jump(self):
        self.rect.y += 2
        platformHitList = pygame.sprite.spritecollide(self, self.level.platformList)
        self.rect.y -= 2
        
        if len(platformHitList) > 0 or self.rect.bottom >= screenHeight:
            self.changeY -= 10
    
    def goLeft(self):
        self.changeX -= 6
    
    def goRight(self):
        self.changeX += 6
    
    def stop(self):
        self.changeX = 0

class Level(object):
    
    def __init__(self, player):
        self.platformList = pygame.sprite.Group()
        self.enemyList = pygame.sprite.Group()
        self.player = player
        
        self.background = None
        
    def update(self):
        self.platformList.update()
        self.enemyList.update()
        
    def draw(self, screen):
        screen.fill(blue)
        
        self.platformList.draw(screen)
        self.enemyList.draw(screen)
        
class levelOne(Level):
    
    def __init__(self, player):
        
        Level.__init__(self, player)
        
        level = [[210, 70, 500, 500],
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 ]
        
        for platform in level:
            block = Platform(platform[0], platform[1])
        