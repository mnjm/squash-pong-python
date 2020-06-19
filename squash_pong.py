import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, cv2
import numpy as np

class SquashPongConfig:
    SCREEN_SIZE = (700, 500)
    WALL_THICKNESS = 30
    BALL_RADIUS = 40
    PADDLE_SIZE = (15, 60)
    SCORE_CANVAS_HEIGHT = 80
    SCREEN_COLOR = (0, 0, 0)
    WALL_COLOR = (255, 255, 255)
    BALL_COLOR = (255, 0, 0)
    PADDLE_COLOR = (0, 255, 0)
    SCORE_COLOR = (0, 127, 127)
    BALL_SPEED = 5
    PADDLE_SPEED = 5
    FONT_SIZE = 32

class Ball:

    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(SquashPongConfig.SCREEN_SIZE[0]//2 - SquashPongConfig.BALL_RADIUS,
                SquashPongConfig.SCREEN_SIZE[1]//2 - SquashPongConfig.BALL_RADIUS,
                SquashPongConfig.BALL_RADIUS//2, SquashPongConfig.BALL_RADIUS//2)
        self.velocity_x = SquashPongConfig.BALL_SPEED * np.random.choice([-1,1])
        self.velocity_y = SquashPongConfig.BALL_SPEED * np.random.choice([-1,1])

    def update(self, paddle):
        point = 0
        # wall bounce
        if self.rect.x <= SquashPongConfig.WALL_THICKNESS:
            self.velocity_x *= -1
        if self.rect.y <= SquashPongConfig.WALL_THICKNESS or (self.rect.y + self.rect.height) >= (SquashPongConfig.SCREEN_SIZE[1] - SquashPongConfig.WALL_THICKNESS):
            self.velocity_y *= -1
        # paddle bounce
        if self.rect.colliderect(paddle.rect):
            self.velocity_x *= -1
            point = +1
        elif (self.rect.x + self.rect.width) >= SquashPongConfig.SCREEN_SIZE[0]:
            point = -1
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        return point
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, SquashPongConfig.BALL_COLOR, self.rect)

class Paddle:

    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(SquashPongConfig.SCREEN_SIZE[0] - SquashPongConfig.PADDLE_SIZE[0], SquashPongConfig.SCREEN_SIZE[1]//2 - SquashPongConfig.PADDLE_SIZE[1]//2,
                SquashPongConfig.PADDLE_SIZE[0], SquashPongConfig.PADDLE_SIZE[1])
        self.velocity = 0

    def update(self):
        self.rect.y += self.velocity
        if self.rect.y <= SquashPongConfig.WALL_THICKNESS:
            self.rect.y = SquashPongConfig.WALL_THICKNESS
        elif (self.rect.y + self.rect.height) >= (SquashPongConfig.SCREEN_SIZE[1] - SquashPongConfig.WALL_THICKNESS):
            self.rect.y = SquashPongConfig.SCREEN_SIZE[1] - SquashPongConfig.WALL_THICKNESS - SquashPongConfig.PADDLE_SIZE[1]

    def draw(self, screen):
        pygame.draw.rect(screen, SquashPongConfig.PADDLE_COLOR, self.rect)

class SquashPong:
    # Actions
    PADDLE_UP = 0
    PADDLE_DOWN = 1
    PADDLE_STAY = 2

    def __init__(self, display_live=False, render_score=False):
        pygame.init()
        self.display_live = display_live
        extra_height = SquashPongConfig.SCORE_CANVAS_HEIGHT if render_score else 0
        if display_live:
            self.screen = pygame.display.set_mode((SquashPongConfig.SCREEN_SIZE[0], SquashPongConfig.SCREEN_SIZE[1] + extra_height))
            pygame.display.set_caption("SquashPong")
        else:
            self.screen = pygame.Surface((SquashPongConfig.SCREEN_SIZE[0], SquashPongConfig.SCREEN_SIZE[1] + extra_height))
        self.render_score = render_score
        if self.render_score:
            self.font = pygame.font.Font("freesansbold.ttf", SquashPongConfig.FONT_SIZE)
        self.walls_rect = [pygame.Rect(0, 0, SquashPongConfig.SCREEN_SIZE[0], SquashPongConfig.WALL_THICKNESS),
            pygame.Rect(0, SquashPongConfig.SCREEN_SIZE[1] - SquashPongConfig.WALL_THICKNESS, SquashPongConfig.SCREEN_SIZE[0], SquashPongConfig.WALL_THICKNESS),
            pygame.Rect(0, SquashPongConfig.WALL_THICKNESS, SquashPongConfig.WALL_THICKNESS, SquashPongConfig.SCREEN_SIZE[1] - SquashPongConfig.WALL_THICKNESS)]
        self.ball = Ball()
        self.paddle = Paddle()
        self.score = 0

    def render_score_board(self):
        if self.render_score:
            text_render = self.font.render("Score: %d"%(self.score), True, SquashPongConfig.SCORE_COLOR)
            text_rect = text_render.get_rect()
            text_rect.center = (SquashPongConfig.SCREEN_SIZE[0]//2, SquashPongConfig.SCREEN_SIZE[1] + SquashPongConfig.SCORE_CANVAS_HEIGHT//2)
            self.screen.blit(text_render, text_rect)

    def update(self, action):
        # Update action and collect reward
        if action == SquashPong.PADDLE_UP:
            self.paddle.velocity = -SquashPongConfig.PADDLE_SPEED
        elif action == SquashPong.PADDLE_DOWN:
            self.paddle.velocity = +SquashPongConfig.PADDLE_SPEED
        elif action == SquashPong.PADDLE_STAY:
            self.paddle.velocity = 0
        self.paddle.update()
        reward = self.ball.update(self.paddle)
        self.score += reward
        # reset the game if lost
        if reward < 0:
            self.paddle.reset()
            self.ball.reset()
        # draw
        self.screen.fill(SquashPongConfig.SCREEN_COLOR)
        for rect in self.walls_rect:
            pygame.draw.rect(self.screen, SquashPongConfig.WALL_COLOR, rect)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        if self.render_score: self.render_score_board()
        # get image
        temp_buffer = pygame.surfarray.pixels3d(self.screen)
        img = temp_buffer.copy() # Deep copy
        del temp_buffer # Free the ref to redraw
        img = np.swapaxes(img, 0, 1)[:SquashPongConfig.SCREEN_SIZE[1],...] # get swap axes and remove score board if rendered
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return reward, img

    def quit(self):
        if self.display_live: pygame.quit()

if __name__ == '__main__':
    if True:
        squashpong = SquashPong(display_live=True, render_score=True)
        clock = pygame.time.Clock()
        exit_flag = False
        action = SquashPong.PADDLE_STAY
        while not exit_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        action = SquashPong.PADDLE_UP
                    elif event.key == pygame.K_DOWN:
                        action = SquashPong.PADDLE_DOWN
                elif event.type == pygame.KEYUP  and (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                    action = SquashPong.PADDLE_STAY
            if not exit_flag: reward, img = squashpong.update(action)
            pygame.display.flip()
            clock.tick(60)
        squashpong.quit()
    else:
        actions = [SquashPong.PADDLE_UP, SquashPong.PADDLE_DOWN, SquashPong.PADDLE_STAY]
        squashpong = SquashPong(display_live=False, render_score=True)
        while True:
            reward, img = squashpong.update(actions[np.random.randint(3)])
            cv2.imshow("Show", img)
            cv2.waitKey(100)
