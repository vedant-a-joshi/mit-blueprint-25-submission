import pygame, random, sys, time, threading
from interruptingcow import timeout
from dataclasses import dataclass

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

screenWidth = 640
screenHeight = 600

touching = [[0,-1],[1,0],[0,1],[-1,0]]

itcolor = black
runcolor = white
player1It = False

def randomiseTeams():
    global player1It
    filler = random.randint(0, 1)
    player1It = filler

# speed = int(input(print("input speed: ")))

@dataclass
class GameMap:
    player1_xpos: int
    player1_ypos: int
    player2_xpos: int
    player2_ypos: int
    mapdata: str

class Player(pygame.sprite.Sprite):
    def __init__(self, image1str, image2str, speed, isIt = False):
        self.isIt = isIt

        super().__init__()
        
        width = 32
        height = 32
        self.speed = speed
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
        self.changeY -= self.speed
    
    def goDown(self):
        self.changeY += self.speed
    
    def goLeft(self):
        self.changeX -= self.speed
    
    def goRight(self):
        self.changeX += self.speed
    
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
        self.image = pygame.transform.scale(self.image, (width, height))
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
    
    def reset(self):
        for i in self.wallList:
            i.kill()
        for i in self.decoList:
            i.kill()
    
    def loadMap(self, mapData):
        for i in self.wallList:
            i.kill()
        for i in self.decoList:
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
                    newWall = Wall(j * 32, i * 32 + 120, 32, 32, f"walls/sprite_{count:02d}.png")
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
                    newGrass = Wall(j * 32, i * 32 + 120, 32, 32, f"grass/sprite_{count:02d}.png")
                    self.decoList.add(newGrass)

def updateSprites(player1, player2):
    if not player1It:
        player1.image = pygame.image.load('Player1NotIt.png')
        player2.image = pygame.image.load('Player2It.png')
        player1.speed = 4
        player2.speed = 5
    else:
        player1.image = pygame.image.load('Player1It.png')
        player2.image = pygame.image.load('Player2NotIt.png')
        player1.speed = 5
        player2.speed = 4

def main():
    FIRST_TO = 3
    TIME_LIMIT = 30 * 1000

    pygame.font.init()
    font = pygame.font.Font("m6x11.ttf", 35)
    font2 = pygame.font.Font("m6x11.ttf", 60)
    font3 = pygame.font.Font("m6x11.ttf", 80)
    font4 = pygame.font.Font("m6x11.ttf", 120)
    global player1It
    global player1Color
    global player2Color
    global player1Score
    global player2Score
    pygame.init()

    crash_sound = pygame.mixer.Sound("get.mp3")

    pygame.mixer.music.load("bgm.mp3")
    pygame.mixer.music.play(-1)
    
    size = [screenWidth, screenHeight]
    screen = pygame.display.set_mode(size)
    screen.set_alpha(None)

    # bg = pygame.image.load("river.png")
    # bg = pygame.transform.scale(bg, (screenWidth, screenHeight))
    
    player1 = Player("Player1It.png", "Player1NotIt.png", 4, isIt = player1It)
    player2 = Player("Player2It.png", "Player2NotIt.png", 4, isIt = not player1It)

    game = Game(player1, player2)
    
    levels = [
    GameMap(1, 1, 18, 13,
"""WWWWWWWWWWWWWWWWWWWW
W                  W
W                  W
W                  W
W                  W
W                  W
W                  W
W                  W
W                  W
W                  W
W                  W
W                  W
W                  W
W                  W
WWWWWWWWWWWWWWWWWWWW"""),
    GameMap(1, 1, 18, 13,
"""WWWWWWWWWWWWWWWWWWWW
W                  W
W                  W
W                  W
W        WW        W
W        WW        W
W        WW        W
W        WW        W
W        WW        W
W        WW        W
W        WW        W
W                  W
W                  W
W                  W
WWWWWWWWWWWWWWWWWWWW"""),
    GameMap(1, 1, 18, 13,
"""WWWWWWWWWWWWWWWWWWWW
W                  W
W    W             W
W        W         W
W        WW        W
W        WWWWW W   W
W              W   W
W        WWWW  WWW W
W        WW        W
W        WW    WW  W
W     WWWWW        W
W                  W
W                  W
W                  W
WWWWWWWWWWWWWWWWWWWW"""),
    ]

    # currentLevelNumber = 0
    # currentLevel = levelList[currentLevelNumber]
    
    activeSpriteList = pygame.sprite.Group()
    player1.level = game
    player2.level = game
    
    activeSpriteList.add(player1)
    
    activeSpriteList.add(player2)
    
    done = False
    collisionOccurred = False

    # timeoutStart = time.time()
    # timeout = 5
    
    clock = pygame.time.Clock()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
    while (not done):
        player1Score = 0
        player2Score = 0
        game.reset()
        
        start = False

        playbtn = pygame.image.load("play.png")
        playbtn = pygame.transform.scale(playbtn, (400, 160))
        playrect = playbtn.get_rect()
        playrect.center = (320, 200)
        screen.blit(playbtn, playrect)

        exitbtn = pygame.image.load("exit.png")
        exitbtn = pygame.transform.scale(exitbtn, (300, 120))
        exitrect = exitbtn.get_rect()
        exitrect.center = (320, 500)
        screen.blit(exitbtn, exitrect)

        playtext = font4.render("Play", False, (255, 255, 255))
        playtextrect = playtext.get_rect(center=(320, 200))
        exittext = font3.render("Exit", False, (255, 255, 255))
        exittextrect = exittext.get_rect(center=(320, 500))

        screen.blit(playtext, playtextrect)
        screen.blit(exittext, exittextrect)
        while not start:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if exitrect.collidepoint(mouse):
                        pygame.quit()
                        return
                    if (playrect.collidepoint(mouse)):
                        start = True
            pygame.event.pump()
            clock.tick(30)
            pygame.display.flip()
        ctime = 0
        while (player1Score < FIRST_TO and player2Score < FIRST_TO):
            randomiseTeams()
            updateSprites(player1, player2)
            print(player1It)

            if player1It:
                player1.speed = 5
                player2.speed = 4
            else: 
                player1.speed = 4
                player2.speed = 5
            pygame.display.set_caption(f"FT{FIRST_TO}, {player1Score}:{player2Score}")
            ctime = 0
            chosen_map_id = random.randrange(0, len(levels))
            chosen_map = levels[chosen_map_id]
            game.loadMap(chosen_map.mapdata)
            player1.rect.x = chosen_map.player1_xpos * 32
            player1.rect.y = chosen_map.player1_ypos * 32 + 120
            player2.rect.x = chosen_map.player2_xpos * 32
            player2.rect.y = chosen_map.player2_ypos * 32 + 120
            textbg = Wall(0, 0, 640, 120, "scoreboard.png")
            game.decoList.add(textbg)
            while ctime < 3 * 1000:
                ctime += clock.get_time()
                timetext = font4.render(f"{ctime}", False, (0, 0, 255))
                timerect = timetext.get_rect(center=(320, 300))

                screen.blit(timetext, timerect)


            ctime = 0
            while (ctime < TIME_LIMIT):

                ctime += clock.get_time()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        pygame.quit()

                player1.changeX = 0
                player1.changeY = 0
                player2.changeX = 0
                player2.changeY = 0

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    player2.goLeft()
                if keys[pygame.K_RIGHT]:
                    player2.goRight()
                if keys[pygame.K_DOWN]:
                    player2.goDown()
                if keys[pygame.K_UP]:
                    player2.goUp()
                
                if keys[pygame.K_a]:
                    player1.goLeft()
                if keys[pygame.K_d]:
                    player1.goRight()
                if keys[pygame.K_s]:
                    player1.goDown()
                if keys[pygame.K_w]:
                    player1.goUp()
                
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
                    updateSprites(player1, player2)
                    crash_sound.play()
                    
                    collisionOccurred = True
                elif not player1.rect.colliderect(player2.rect):
                    collisionOccurred = False
                
                # drawing code shd be above
                
                clock.tick(60)

                ntime = TIME_LIMIT - ctime
                if (ntime < 0):
                    ntime = 0
                sec = ntime // 1000
                ms = ntime % 1000
                time_counter = font.render(f"Time remaining: {sec}.{ms:03d}", False, (255, 255, 255))
                tc_rect = time_counter.get_rect(center=(320, 25))
                p1score = font2.render(f"{player1Score}", False, (255, 0, 0))
                p1s_rect = p1score.get_rect(center=(252, 85))
                p2score = font2.render(f"{player2Score}", False, (0, 0, 255))
                p2s_rect = p1score.get_rect(midleft=(380, 85))

                screen.blit(time_counter, tc_rect)
                screen.blit(p1score, p1s_rect)
                screen.blit(p2score, p2s_rect)

                pygame.display.flip()
                # print(clock)
            
            player1Score += not player1It
            player2Score += player1It

        continue

    pygame.quit()

        
if __name__ == "__main__":
    main()        
