import pygame, random, time
from interruptingcow import timeout

 

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

screenWidth = 640
screenHeight = 480

touching = [[0,-1],[1,0],[0,1],[-1,0]]

itcolor = black
runcolor = white
player1It = False
filler = random.randint(0, 1)%2
if filler == 1:
    player1Color = itcolor
    player2Color = runcolor
    player1It = True
else:
    player1Color = itcolor
    player2Color = runcolor
    player1It = False

# speed = int(input(print("input speed: ")))
speed = 4

class Player(pygame.sprite.Sprite):
    def __init__(self, image1str, image2str, isIt = False):
        self.isIt = isIt

        super().__init__()
        
        width = 32
        height = 32
        self.image = pygame.Surface([width, height])
        
        if (isIt):
            self.image = pygame.image.load(image1str)
        else:
            self.image = pygame.image.load(image2str)
        
        self.rect = self.image.get_rect()
        
        self.changeX = 0
        self.changeY = 0
        
        self.level = None
        
    def update(self):
        
        # self.calcGrav()
        
        self.rect.x += self.changeX
        blockHitList = pygame.sprite.spritecollide(self, self.level.wallList, False)
        for block in blockHitList:
            if self.changeX > 0:
                self.rect.right = block.rect.left
            elif self.changeX < 0:
                self.rect.left = block.rect.right
                
            self.changeX = 0
        
        self.rect.y += self.changeY
        blockHitList = pygame.sprite.spritecollide(self, self.level.wallList, False)
        for block in blockHitList:
            if self.changeY > 0:
                self.rect.bottom = block.rect.top
            elif self.changeY < 0:
                self.rect.top = block.rect.bottom
            
            self.changeY = 0
    
    # def calcGrav(self):
    #     if self.changeY == 0:
    #         self.changeY = 1
    #     else:
    #         self.changeY += 0.35
    
    #     if self.rect.y >= screenHeight - self.rect.height and self.changeY >= 0:
    #         self.changeY = 0
    #         self.rect.y = screenHeight - self.rect.height
        
    def goUp(self):
        # self.rect.y += 2
        # platformHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        # self.rect.y -= 2
        
        # if len(platformHitList) > 0 or self.rect.bottom >= screenHeight:
        #     self.changeY -= 10
        self.changeY -= speed
    
    def goDown(self):
        self.changeY += speed
    
    def goLeft(self):
        self.changeX -= speed
    
    def goRight(self):
        self.changeX += speed
    
    def stopHorizontal(self):
        self.changeX = 0
    
    def stopVertical(self):
        self.changeY = 0
        
    # def stop(self):
    #     self.changeY = 0
    #     self.changeX = 0

class Wall(pygame.sprite.Sprite):
    
    def __init__(self, xpos, ypos, width, height, image):
        super().__init__()
        
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
    

class Game(object):
    
    def __init__(self, player1, player2):
        self.wallList = pygame.sprite.Group()
        self.decoList = pygame.sprite.Group()
        self.player1 = player1
        self.player2 = player2
            
    def update(self):
        self.wallList.update()
        self.decoList.update()
        
    def draw(self, screen):
        self.wallList.draw(screen)
        self.decoList.draw(screen)
    
    def loadMap(self, mapData):
        for i in self.wallList:
            i.kill()
        mapArr = mapData.split("\n")
        for i in range(15):
            for j in range(20):
                if (mapArr[i][j] == 'W'):
                    count = 0
                    for k in range(4):
                        newXPos = i + touching[k][0]
                        newYPos = j + touching[k][1]
                        try:
                            if mapArr[newXPos][newYPos] != 'W':
                                count += 2 ** k
                        except:
                            count += 2 ** k
                    print(f"({i},{j})=>{count}")
                    newWall = Wall(j * 32, i * 32, 32, 32, f"walls/sprite_{count:02d}.png")
                    self.wallList.add(newWall)
                elif (mapArr[i][j] == ' '):
                    count = 0
                    for k in range(4):
                        newXPos = i + touching[k][0]
                        newYPos = j + touching[k][1]
                        try:
                            if mapArr[newXPos][newYPos] != ' ':
                                count += 2 ** k
                        except:
                            count += 2 ** k
                    newGrass = Wall(j * 32, i * 32, 32, 32, f"grass/sprite_{count:02d}.png")
                    self.decoList.add(newGrass)


def main():

    global player1It
    global player1Color
    global player2Color
    pygame.init()

    crash_sound = pygame.mixer.Sound("get.mp3")


    pygame.mixer.music.load('bgm.mp3')
    pygame.mixer.music.play(-1)
    
    size = [screenWidth, screenHeight]
    screen = pygame.display.set_mode(size)
    screen.set_alpha(None)

    # bg = pygame.image.load("river.png")
    # bg = pygame.transform.scale(bg, (screenWidth, screenHeight))

    
    pygame.display.set_caption("Tag")
    
    player1 = Player("Player1It.png", "Player1NotIt.png", isIt = player1It)
    player2 = Player("Player2It.png", "Player2NotIt.png", isIt = not player1It)

    game = Game(player1, player2)
    
    levels = [
        """WWWWWWWWWWWWWWWWWWWW
W                  W
W  W W             W
W  W W             W
W  W WWW           W
W  W               W
W  WWWWWW          W
W                  W
W                  W
W                  W
W          WWWWWWW W
W          WWWWWWW W
W          WWWWWWW W
W                  W
WWWWWWWWWWWWWWWWWWWW"""
    ]

    game.loadMap(levels[0])

    # currentLevelNumber = 0
    # currentLevel = levelList[currentLevelNumber]
    
    activeSpriteList = pygame.sprite.Group()
    player1.level = game
    player2.level = game
    
    player1.rect.x = 80
    player1.rect.y = 80
    activeSpriteList.add(player1)
    
    player2.rect.x = 400
    player2.rect.y = 400
    activeSpriteList.add(player2)
    
    done = False
    collisionOccurred = False
    timeoutStart = time.time()
    timeout = 5
    
    clock = pygame.time.Clock()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
    
    while (not done or time.time() < timeout + timeoutStart):
        
        # screen.blit(bg, (0, 0))

        # events = pygame.event.get()
        # for event in events:
        #     if event.type == pygame.QUIT:
        #         done = True
                
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_x:
        #             levelOne.loadMap()
                
        #         if event.key == pygame.K_LEFT:
        #             player1.goLeft()
        #         elif event.key == pygame.K_RIGHT:
        #             player1.goRight()
        #         if event.key == pygame.K_UP:
        #             player1.goUp()
        #         elif event.key == pygame.K_DOWN:
        #             player1.goDown()
                    
        #         if event.key == pygame.K_a:
        #             player2.goLeft()
        #         elif event.key == pygame.K_d:
        #             player2.goRight()
        #         if event.key == pygame.K_w:
        #             player2.goUp()
        #         elif event.key == pygame.K_s:
        #             player2.goDown()
            
        #     if event.type == pygame.KEYUP:
        #         if event.key == pygame.K_LEFT:
        #             player1.stopHorizontal()
        #         if event.key == pygame.K_RIGHT:  
        #             player1.stopHorizontal()
        #         if event.key == pygame.K_UP:
        #             player1.stopVertical()
        #         if event.key == pygame.K_DOWN:
        #             player1.stopVertical()
                
        #         if event.key == pygame.K_a:
        #             player2.stopHorizontal()
        #         if event.key == pygame.K_d:  
        #             player2.stopHorizontal()
        #         if event.key == pygame.K_w:
        #             player2.stopVertical()
        #         if event.key == pygame.K_s:
        #             player2.stopVertical()

        player1.changeX = 0
        player1.changeY = 0
        player2.changeX = 0
        player2.changeY = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player1.goLeft()
        if keys[pygame.K_RIGHT]:
            player1.goRight()
        if keys[pygame.K_DOWN]:
            player1.goDown()
        if keys[pygame.K_UP]:
            player1.goUp()
        
        if keys[pygame.K_a]:
            player2.goLeft()
        if keys[pygame.K_d]:
            player2.goRight()
        if keys[pygame.K_s]:
            player2.goDown()
        if keys[pygame.K_w]:
            player2.goUp()
        
        pygame.event.pump()
        
        # player1.update()
        # player2.update()
        activeSpriteList.update()
        # currentLevel.update()
        game.update()
        
        if player1.rect.right > screenWidth:
            player1.rect.right = screenWidth
        if player1.rect.left < 0:
            player1.rect.left = 0
        if player1.rect.bottom > screenHeight:
            player1.rect.bottom = screenHeight
        if player1.rect.top < 0:
            player1.rect.top = 0
            
        if player2.rect.right > screenWidth:
            player2.rect.right = screenWidth
        if player2.rect.left < 0:
            player2.rect.left = 0
        if player2.rect.bottom > screenHeight:
            player2.rect.bottom = screenHeight
        if player2.rect.top < 0:
            player2.rect.top = 0
        
        # other drawing code below
        game.draw(screen)
        activeSpriteList.draw(screen)
        
        if player1.rect.colliderect(player2.rect) and not collisionOccurred:
            crash_sound.play()
            if player1It:
                player1It = False
                player1.image = pygame.image.load('Player1NotIt.png')
                player2.image = pygame.image.load('Player2It.png')
                # player1.image.fill(runcolor)
                # player2.image.fill(itcolor)
            else:
                player1It = True
                player1.image = pygame.image.load('Player1It.png')
                player2.image = pygame.image.load('Player2NotIt.png')
                # player1.image.fill(itcolor)
                # player2.image.fill(runcolor)
            
            collisionOccurred = True
        elif not player1.rect.colliderect(player2.rect):
            collisionOccurred = False
        
        # drawing code shd be above
        
        clock.tick(60)
        pygame.display.flip()
        # print(clock)
        
    pygame.quit()

        
if __name__ == "__main__":
    main()        
