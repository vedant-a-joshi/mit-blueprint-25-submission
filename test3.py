# webserver testing
import pygame

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

screenWidth = 800
screenHeight = 600

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        width = 60
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(red)
        
        self.rect = self.image.get_rect()
        
        self.changeX = 0
        self.changeY = 0
        
        self.level = None
        
    def update(self):
        
        # self.calcGrav()
        self.rect.x += self.changeX
        self.rect.y += self.changeY
        
        blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        for block in blockHitList:
            if self.changeX > 0:
                self.rect.right = block.rect.left
            elif self.changeX < 0:
                self.rect.left = block.rect.right
        
        self.rect.y += self.changeY
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
        
    def goUp(self):
        # self.rect.y += 2
        # platformHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        # self.rect.y -= 2
        
        # if len(platformHitList) > 0 or self.rect.bottom >= screenHeight:
        #     self.changeY -= 10
        self.changeY -= 6
    
    def goDown(self):
        self.changeY += 6
    
    def goLeft(self):
        self.changeX -= 6
    
    def goRight(self):
        self.changeX += 6
    
    def stop(self):
        self.changeY = 0
        self.changeX = 0
        
class Platform(pygame.sprite.Sprite):
    
    def __init__(self, width, height):
        super().__init__()
        
        self.image = pygame.Surface([width, height])
        self.image.fill(green)
        
        self.rect = self.image.get_rect()

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
        
        # width, height, x, y
        level = [[210, 70, 500, 500],
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 ]
        
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platformList.add(block)

def main():
    pygame.init()
    
    size = [screenWidth, screenHeight]
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("Game")
    
    player = Player()
    
    levelList = []
    levelList.append(levelOne(player))
    
    currentLevelNumber = 0
    currentLevel = levelList[currentLevelNumber]
    
    activeSpriteList = pygame.sprite.Group()
    player.level = currentLevel
    
    player.rect.x = 80
    player.rect.y = screenHeight - player.rect.height
    activeSpriteList.add(player)
    
    done = False
    
    clock = pygame.time.Clock()
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.goLeft()
                if event.key == pygame.K_RIGHT:
                    player.goRight()
                if event.key == pygame.K_UP:
                    player.goUp()
                if event.key == pygame.K_DOWN:
                    player.goDown()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.changeX < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.changeX > 0:
                    player.stop()
                if event.key == pygame.K_UP and player.changeY < 0:
                    player.stop()
                if event.key == pygame.K_DOWN and player.changeY > 0:
                    player.stop()
        
        activeSpriteList.update()
        currentLevel.update()
        
        if player.rect.right > screenWidth:
            player.rect.right = screenWidth
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.bottom > screenHeight:
            player.rect.bottom = screenHeight
        if player.rect.top < 0:
            player.rect.top = 0
        
        # other drawing code below
        currentLevel.draw(screen)
        activeSpriteList.draw(screen)
        # drawing code shd be above
        
        clock.tick(60)
        
        pygame.display.flip()
        
    pygame.quit()

        
if __name__ == "__main__":
    main()