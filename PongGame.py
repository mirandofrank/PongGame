#Frank Mirando
#CPSC 386
#Pong (w/ no walls) vs AI
#This game represents the classic pong game
#3 paddles for both players, with no walls
#Must win 3/5 games to win match; must win by 11 points and be ahead by at least 1 point

import pygame
import sys
import random
pygame.init()

#Settings
window_width = 900
window_height = 400
paddleLong = 120
paddleShort = 10
fps = 120
clock = pygame.time.Clock()

#Colors; may or may not need?
c_white = (255, 255, 255)
c_black = (0, 0, 0)
c_gold = (255, 215, 0)
c_purple = (191, 62, 255)

#Images
bg = pygame.image.load('dottedResized.png')

#Audio
ballHit = pygame.mixer.Sound('ball_hit.wav')
winGame = pygame.mixer.Sound('winGame.wav')
loseGame = pygame.mixer.Sound('lost.wav')
#winMatch = pygame.mixer.Sound()

#Game window
win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Pong Game')
win.blit(bg, (0, 0))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PLAYER CLASSES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Player's vertical paddle
class PlayerVertical(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((paddleShort, paddleLong))
        self.image = pygame.image.load('paddle_vertical.png')
        self.rect = self.image.get_rect()
        self.rect.right = window_width
        self.rect.centery = window_height / 2
        self.dy = 0

    def update(self):
        self.dy = 0
        # Movement
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_UP]:
            self.dy = -10
        if key_state[pygame.K_DOWN]:
            self.dy = 10
        self.rect.y += self.dy  # Adds change to position in y

        # Constrain sprites
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > window_height:
            self.rect.bottom = window_height

#Player's top paddle
class PlayerPaddleTop(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((paddleLong, paddleShort))
        self.image = pygame.image.load('paddle_horizon.png')
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.centerx = window_width - (window_width / 4)
        self.dx = 0

    def update(self):
        self.dx = 0
        # Movement
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.dx = -10
        if key_state[pygame.K_RIGHT]:
            self.dx = 10
        self.rect.x += self.dx  # Adds change to position in x

        # Constrain sprites
        if self.rect.left < window_width / 2:
            self.rect.left = window_width / 2
        if self.rect.right > window_width - 10:
            self.rect.right = window_width - 10

#Player's bottom paddle
class PlayerPaddleBot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((paddleLong, paddleShort))
        #self.image.fill(c_white)
        self.image = pygame.image.load('paddle_horizon.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = window_height
        self.rect.centerx = window_width - (window_width / 4)
        self.dx = 0

    def update(self):
        self.dx = 0
        # Movement
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.dx = -10
        if key_state[pygame.K_RIGHT]:
            self.dx = 10
        self.rect.x += self.dx  # Adds change to position in x

        # Constrain sprites
        if self.rect.left < window_width / 2:
            self.rect.left = window_width / 2
        if self.rect.right > window_width - 10:
            self.rect.right = window_width - 10

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~AI CLASSES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Tracks movement of ball in order to move 3 paddles
#AI's vertical paddle
class AIVerticalPad(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((paddleShort, paddleLong))
        self.image = pygame.image.load('AI_verticalPaddle.jpeg')
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.centery = window_height / 2
        self.speed = 4
        self.dy = 0

    def update(self):
        self.dy = 0
        # Movement; track the y position of the ball
        if ball.rect.centery < self.rect.centery:
            self.dy -= self.speed
        if ball.rect.centery > self.rect.centery:
            self.dy += self.speed
        self.rect.y += self.dy
        # Constrain sprites
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > window_height:
            self.rect.bottom = window_height

#AI's top paddle
class AITopPad(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((paddleLong, paddleShort))
        self.image = pygame.image.load('AI_horizonPaddle.jpeg')
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.centerx = window_width / 4
        self.speed = 4
        self.dx = 0

    def update(self):
        self.dx = 0
        # Movement; track the x position of the ball
        if ball.rect.centerx > self.rect.centerx:
            self.dx += self.speed
        if ball.rect.centerx < self.rect.centerx:
            self.dx -= self.speed
        self.rect.x += self.dx
        # Constrain sprites
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > window_width / 2:
            self.rect.right = window_width / 2

#AI's bottom paddle
class AIBotPad(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((paddleLong, paddleShort))
        self.image = pygame.image.load('AI_horizonPaddle.jpeg')
        self.rect = self.image.get_rect()
        self.rect.bottom = window_height
        self.rect.centerx = window_width / 4
        self.speed = 4
        self.dx = 0

    def update(self):
        self.dx = 0
        # Movement; track the x position of the ball
        if ball.rect.centerx > self.rect.centerx:
            self.dx += self.speed
        if ball.rect.centerx < self.rect.centerx:
            self.dx -= self.speed
        self.rect.x += self.dx
        # Constrain sprites
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > window_width / 2:
            self.rect.right = window_width / 2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~BALL CLASS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(c_gold)
        self.rect = self.image.get_rect()
        self.rect.center = (window_width / 2, window_height / 2)
        # Added default values for vector values so ball isn't so slow at the start
        self.dx = 4.5
        self.dy = 4.5
        #Randomizes direction ball starts
        self.dx *= random.choice([-1, 1])
        self.dy *= random.choice([-1, 1])

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Collision with paddles
        collision = pygame.sprite.spritecollideany(ball, all_sprites)
        if collision:
            ballHit.play()
            #Collisions with player's paddles
            if collision == player_vert:
                self.rect.x -= self.dx
                self.dx *= -1
                self.dx += random.choice([0, 1])  # Random: ball will stay same speed or speed up
            if collision == player_top:
                self.rect.y -= self.dy
                self.dy *= -1
                self.dy += random.choice([0, 1])
            if collision == player_bot:
                self.rect.y -= self.dy
                self.dy *= -1
                self.dy += random.choice([0, 1])

            #Collision with AI paddles
            if collision == AI_vert:
                self.rect.x -= self.dx
                self.dx *= -1
                self.dx += random.choice([0, 1])
            if collision == AI_top:
                self.rect.y -= self.dy
                self.dy *= -1
                self.dy += random.choice([0, 1])
            if collision == AI_bot:
                self.rect.y -= self.dy
                self.dy *= -1
                self.dy += random.choice([0, 1])
            #If ball gets stuck vertically
            if self.dy == 0:
                self.dy = random.choice([-1, 1])
            if self.dy <= 0:
                self.dy += random.choice([-1, 0, 1])
            if self.dy >= 0:
                self.dy += random.choice([-1, 0, 1])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SCORE CLASS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Score(object):
    def __init__(self):
        self.scoreP = 0
        self.scoreAI = 0
        self.score_font = pygame.font.SysFont(None, 100)
        self.win_font = pygame.font.SysFont(None, 70)
        self.pointsN = pygame.font.SysFont(None, 20)
        self.player_win = self.win_font.render('You Win!', True, c_white)
        self.playerAI_win = self.win_font.render('AI Wins!', True, c_white)
        self.pointsNeeded = self.pointsN.render('First player to score 11 points wins!', True, c_white)
        self.player_score = 0
        self.playerAI_score = 0

    def update(self):
        #If a player scores
        if ball.rect.right < 0:
            self.scoreP += 1
            ball.__init__()
        if ball.rect.left > window_width:
            self.scoreAI += 1
            ball.__init__()
        self.player_score = self.score_font.render(str(self.scoreP), True, c_white, c_black)
        self.playerAI_score = self.score_font.render(str(self.scoreAI), True, c_white, c_black)

    def draw(self):
        win.blit(self.playerAI_score, (window_width / 4, window_height / 8))
        win.blit(self.player_score, (window_width * 3 / 4, window_height / 8))
        win.blit(self.pointsNeeded, (window_width / 2 - 100, window_height - 350))

        #If player wins
        if self.scoreP == 11:
            winGame.play()
            win.blit(self.player_win, (505, window_height / 3))
            ball.dx = 0
            ball.dy = 0
        #If AI wins
        if self.scoreAI == 11:
            loseGame.play()
            win.blit(self.playerAI_win, (55, window_height / 3))
            ball.dx = 0
            ball.dy = 0


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SPRITE GROUPS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
all_sprites = pygame.sprite.Group()
ball_sprite = pygame.sprite.GroupSingle()

#Player paddle objects
player_vert = PlayerVertical()
all_sprites.add(player_vert)
player_top = PlayerPaddleTop()
all_sprites.add(player_top)
player_bot = PlayerPaddleBot()
all_sprites.add(player_bot)

#AI paddles objects
AI_vert = AIVerticalPad()
all_sprites.add(AI_vert)
AI_top = AITopPad()
all_sprites.add(AI_top)
AI_bot = AIBotPad()
all_sprites.add(AI_bot)

#Ball sprite
ball = Ball()
ball_sprite.add(ball)

#Score
score = Score()
score.__init__()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GAME LOOP~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
while True:
    clock.tick(fps)

    #Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #Update
    all_sprites.update()
    ball_sprite.update()
    score.update()

    #Draw
    win.blit(bg, [0, 0])
    pygame.draw.circle(win, c_white, (window_width // 2 - 5, window_height // 2), 80, 1)
    score.draw()
    all_sprites.draw(win)
    ball_sprite.draw(win)

    #Flip
    pygame.display.flip()
#pygame.quit()
